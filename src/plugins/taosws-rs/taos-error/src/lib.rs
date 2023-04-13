#![cfg_attr(nightly, feature(backtrace))]

use std::{
    borrow::Cow,
    fmt::{self, Debug, Display},
    ops::{Deref, DerefMut},
    str::FromStr,
};

#[cfg(nightly)]
use std::backtrace::Backtrace;

use mdsn::DsnError;
use thiserror::Error;

macro_rules! _impl_fmt {
    ($fmt:ident) => {
        impl fmt::$fmt for Code {
            fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
                fmt::$fmt::fmt(&self.0, f)
            }
        }
    };
}

_impl_fmt!(LowerHex);
_impl_fmt!(UpperHex);

/// TDengine error code.
#[derive(Clone, Copy, Eq, PartialEq, Hash, Default)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[repr(transparent)]
pub struct Code(i32);

impl Code {
    pub const COLUMN_EXISTS: Code = Code(0x036B);
    pub const COLUMN_NOT_EXIST: Code = Code(0x036C);
    pub const TAG_ALREADY_EXIST: Code = Code(0x0369);
    pub const TAG_NOT_EXIST: Code = Code(0x036A);
    pub const MODIFIED_ALREADY: Code = Code(0x264B);
    pub const INVALID_COLUMN_NAME: Code = Code(0x2602);
    pub const TABLE_NOT_EXIST: Code = Code(0x2603);
    pub const STABLE_NOT_EXIST: Code = Code(0x0362);
    pub const INVALID_ROW_BYTES: Code = Code(0x036F);
    pub const DUPLICATED_COLUMN_NAMES: Code = Code(0x263C);
    pub const NO_COLUMN_CAN_BE_DROPPED: Code = Code(0x2651);
}

impl Display for Code {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_fmt(format_args!("{:#06X}", *self))
    }
}

impl Debug for Code {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_fmt(format_args!(
            "Code([{:#06X}] {})",
            self.0,
            self.as_error_str()
        ))
    }
}

macro_rules! _impl_from {
    ($($from:ty) *) => {
        $(
            impl From<$from> for Code {
                #[inline]
                fn from(c: $from) -> Self {
                    Self(c as i32 & 0xFFFF)
                }
            }
            impl From<Code> for $from {
                #[inline]
                fn from(c: Code) -> Self {
                    c.0 as _
                }
            }
        )*
    };
}

_impl_from!(i8 u8 i16 i32 u16 u32 i64 u64);

impl Deref for Code {
    type Target = i32;

    fn deref(&self) -> &i32 {
        &self.0
    }
}

impl DerefMut for Code {
    fn deref_mut(&mut self) -> &mut i32 {
        &mut self.0
    }
}

impl Code {
    /// Code from raw primitive type.
    pub const fn new(code: i32) -> Self {
        Code(code)
    }
}

#[allow(non_upper_case_globals, non_snake_case)]
mod code {
    include!(concat!(env!("OUT_DIR"), "/code.rs"));
}

#[derive(Debug, Error)]
pub struct Error {
    code: Code,
    err: Cow<'static, str>,
    #[cfg(nightly)]
    backtrace: Backtrace,
}

impl From<DsnError> for Error {
    fn from(dsn: DsnError) -> Self {
        Self::new(Code::Failed, dsn.to_string())
    }
}

pub type Result<T> = std::result::Result<T, Error>;

impl Error {
    #[inline]
    pub fn new(code: impl Into<Code>, err: impl Into<Cow<'static, str>>) -> Self {
        Self {
            code: code.into(),
            err: err.into(),
            #[cfg(nightly)]
            backtrace: Backtrace::capture(),
        }
    }

    #[inline]
    pub fn errno(&self) -> Code {
        self.code
    }

    #[inline]
    pub const fn code(&self) -> Code {
        self.code
    }
    #[inline]
    pub fn message(&self) -> &str {
        &self.err
    }

    #[inline]
    pub fn from_code(code: impl Into<Code>) -> Self {
        Self::new(code, "")
    }

    #[inline]
    pub fn from_string(err: impl Into<Cow<'static, str>>) -> Self {
        Self::new(Code::Failed, err)
    }

    #[inline]
    pub fn from_any(err: impl Display) -> Self {
        Self::new(Code::Failed, err.to_string())
    }
}

impl FromStr for Error {
    type Err = ();

    #[inline]
    fn from_str(s: &str) -> std::result::Result<Self, Self::Err> {
        Ok(Self::from_string(s.to_string()))
    }
}

// impl<T: std::error::Error> From<T> for Error {
//     fn from(_: T) -> Self {
//         todo!()
//     }
// }

impl Display for Error {
    #[inline]
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        if self.code == Code::Failed {
            write!(f, "{}", self.err)
        } else {
            write!(f, "[{:#06X}] {}", self.code, self.err)
        }
    }
}

#[cfg(feature = "serde")]
impl serde::de::Error for Error {
    #[inline]
    fn custom<T: fmt::Display>(msg: T) -> Error {
        Error::from_string(format!("{}", msg))
    }
}

#[test]
fn test_code() {
    let c: i32 = Code::new(0).into();
    assert_eq!(c, 0);
    let c = Code::from(0).to_string();
    assert_eq!(c, "0x0000");
    dbg!(Code::from(0x200));
}

#[test]
fn test_display() {
    let err = Error::new(Code::Success, "Success");
    assert_eq!(format!("{err}"), "[0x0000] Success");
}
