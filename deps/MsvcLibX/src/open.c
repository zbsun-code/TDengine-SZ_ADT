﻿/*****************************************************************************\
*                                                                             *
*   Filename	    open.c						      *
*									      *
*   Description:    WIN32 UTF-8 version of open				      *
*                                                                             *
*   Notes:	    							      *
*		    							      *
*   History:								      *
*    2017-02-16 JFL Created this module.				      *
*                                                                             *
*         Copyright 2017 Hewlett Packard Enterprise Development LP          *
* Licensed under the Apache 2.0 license - www.apache.org/licenses/LICENSE-2.0 *
\*****************************************************************************/

#define _UTF8_SOURCE /* Generate the UTF-8 version of printf routines */

#define _CRT_SECURE_NO_WARNINGS 1 /* Avoid Visual C++ security warnings */

#include <errno.h>
#include "msvclibx.h"
#include "msvcFcntl.h"
#include "msvcDebugm.h"
#include "msvcLimits.h"

#ifdef _WIN32

#include <windows.h>

/*---------------------------------------------------------------------------*\
*                                                                             *
|   Function        open	                                              |
|                                                                             |
|   Description     UTF-8 or ANSI file name open(), with long path support    |
|                                                                             |
|   Parameters      char *pszName	File name			      |
|                   int iFlags		Opening mode			      |
|                   int iPerm		Permission mode for file creation     |
|                                                                             |
|   Returns         File number						      |
|                                                                             |
|   Notes           Prefixes long names with "\\?\" to enable long path suppt.|
|                                                                             |
|   History								      |
|    2017-02-16 JFL Created this routine.                      		      |
*                                                                             *
\*---------------------------------------------------------------------------*/

int openM(UINT cp, const char *pszName, int iFlags, int iPerm) {
  WCHAR wszName[UNICODE_PATH_MAX];
  int n;
  int iFile;

  /* Convert the pathname to a unicode string, with the proper extension prefixes if it's longer than 260 bytes */
  n = MultiByteToWidePath(cp,			/* CodePage, (CP_ACP, CP_OEMCP, CP_UTF8, ...) */
    			  pszName,		/* lpMultiByteStr, */
			  wszName,		/* lpWideCharStr, */
			  COUNTOF(wszName)	/* cchWideChar, */
			  );
  if (!n) {
    errno = Win32ErrorToErrno();
    return -1;
  }

/*  return _wopen(wszName, iFlags, iPerm); */
  DEBUG_PRINTF(("_wopen(\"%s\", 0x%X, 0x%X);\n", pszName, iFlags, iPerm));
  iFile = _wopen(wszName, iFlags, iPerm);
  DEBUG_PRINTF(("  return %d;\n", iFile));
  return iFile;
}

#pragma warning(disable:4212) /* Ignore the "nonstandard extension used : function declaration used ellipsis" warning */

int openA(const char *pszName, int iFlags, int iPerm) {
  return openM(CP_ACP, pszName, iFlags, iPerm);
}

int openU(const char *pszName, int iFlags, int iPerm) {
  return openM(CP_UTF8, pszName, iFlags, iPerm);
}

#pragma warning(default:4212) /* Restore the "nonstandard extension used : function declaration used ellipsis" warning */

#endif /* defined(_WIN32) */
