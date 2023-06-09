/*
 * Copyright (c) 2019 TAOS Data, Inc. <jhtao@taosdata.com>
 *
 * This program is free software: you can use, redistribute, and/or modify
 * it under the terms of the GNU Affero General Public License, version 3
 * or later ("AGPL"), as published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef TDENGINE_VNODE_H
#define TDENGINE_VNODE_H

#ifdef __cplusplus
extern "C" {
#endif
#include "trpc.h"
#include "twal.h"

typedef struct {
  int64_t submitReqSucNum;
  int64_t submitRowNum;
  int64_t submitRowSucNum;
} SVnodeStatisInfo;

typedef struct {
  int32_t len;
  void *  rsp;
  void *  qhandle;  // used by query and retrieve msg
  tsem_t* psem;  // if it is not zero, need wait result with async 
} SRspRet;

typedef struct {
  int32_t code;
  int32_t contLen;
  void *  rpcHandle;
  void *  rpcAhandle;
  void *  qhandle;
  void *  pVnode;
  int8_t  qtype;
  int8_t  msgType;
  SRspRet rspRet;
  char    pCont[];
} SVReadMsg;

typedef struct {
  int32_t  code;
  int32_t  processedCount;
  int32_t  qtype;
  void *   pVnode;
  SRpcMsg  rpcMsg;
  SRspRet  rspRet;
  char     reserveForSync[24];
  SWalHead walHead;
} SVWriteMsg;

typedef struct {
  int32_t     startTime;
  pthread_t * pthread;
  tsem_t *    psem;
  void *      param;
} SWaitThread;

// vnodeStatus
extern char *vnodeStatus[];

// vnodeMain
int32_t vnodeCreate(SCreateVnodeMsg *pVnodeCfg);
int32_t vnodeDrop(int32_t vgId);
int32_t vnodeOpen(int32_t vgId);
int32_t vnodeAlter(void *pVnode, SCreateVnodeMsg *pVnodeCfg);
int32_t vnodeSync(int32_t vgId);
int32_t vnodeClose(int32_t vgId);
int32_t vnodeCompact(int32_t vgId);

// vnodeMgmt
int32_t vnodeInitMgmt();
void    vnodeCleanupMgmt();
void*   vnodeAcquire(int32_t vgId);
void    vnodeRelease(void *pVnode);
void*   vnodeAcquireNotClose(int32_t vgId);
void*   vnodeGetWal(void *pVnode);
int32_t vnodeGetVnodeList(int32_t vnodeList[], int32_t *numOfVnodes);
void    vnodeBuildStatusMsg(void *pStatus);
void    vnodeSetAccess(SVgroupAccess *pAccess, int32_t numOfVnodes);

// vnodeWrite
int32_t vnodeWriteToWQueue(void *pVnode, void *pHead, int32_t qtype, void *pRpcMsg);
void    vnodeFreeFromWQueue(void *pVnode, SVWriteMsg *pWrite);
int32_t vnodeProcessWrite(void *pVnode, void *pHead, int32_t qtype, void *pRspRet);

SVnodeStatisInfo vnodeGetStatisInfo();

// vnodeSync
void    vnodeConfirmForward(void *pVnode, uint64_t version, int32_t code, bool force);

// vnodeRead
int32_t vnodeWriteToRQueue(void *pVnode, void *pCont, int32_t contLen, int8_t qtype, void *rparam);
void    vnodeFreeFromRQueue(void *pVnode, SVReadMsg *pRead);
int32_t vnodeProcessRead(void *pVnode, SVReadMsg *pRead);

// wait thread
void vnodeAddWait(void* pVnode, pthread_t* pthread, tsem_t* psem, void* param);
void vnodeRemoveWait(void* pVnode, void* param);
// get wait thread count
bool vnodeWaitTooMany(void* vparam);
tsem_t* vnodeSemWait(void* vparam);

#ifdef __cplusplus
}
#endif

#endif
