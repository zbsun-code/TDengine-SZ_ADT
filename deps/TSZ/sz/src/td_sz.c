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

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "td_sz.h"
#include "sz.h"
#include "conf.h"

//
// Init  success return 1 else 0
//
void tdszInit(double fPrecision, double dPrecision, unsigned int maxIntervals, unsigned int intervals, int entropyType, int huffman_force, const char* compressor)
{
	// need malloc
	if(confparams_cpr == NULL)
	   confparams_cpr = (sz_params*)malloc(sizeof(sz_params));    
	if(exe_params == NULL)
       exe_params = (sz_exedata*)malloc(sizeof(sz_exedata));
	 
	// set default
	setDefaulParams(exe_params, confparams_cpr);

    // overwrite with args
	confparams_cpr->absErrBound = fPrecision;
	confparams_cpr->absErrBoundDouble = dPrecision;
	confparams_cpr->max_quant_intervals = maxIntervals;
	confparams_cpr->quantization_intervals = intervals;
	confparams_cpr->entropy_type = entropyType;
	confparams_cpr->huffman_force = huffman_force;
	
	confparams_cpr->maxRangeRadius = confparams_cpr->max_quant_intervals/2;		
	exe_params->intvCapacity = confparams_cpr->maxRangeRadius*2;
	exe_params->intvRadius   = confparams_cpr->maxRangeRadius;

	if(strcmp(compressor, "GZIP_COMPRESSOR")==0)
		confparams_cpr->losslessCompressor = GZIP_COMPRESSOR;
	else if(strcmp(compressor, "ZSTD_COMPRESSOR")==0)
		confparams_cpr->losslessCompressor = ZSTD_COMPRESSOR;
	
	return ;
}


//
// compress interface to tdengine return value is count of output with bytes
//
int tdszCompress(int type, const char * input, const int nelements, const char * output)
{
	// check valid
	sz_params comp_params = *confparams_cpr;
	
	size_t outSize = SZ_compress_args(type, (void*)input, (size_t)nelements, (unsigned char*)output, &comp_params);	
    return (int)outSize;
}

//
// decompress interface to tdengine return value is count of output with bytes
//
#include "tlog.h"
// #define DECOMPRESS_TRACE
#define vInfo(...) { taosPrintLog("VND ", 255, __VA_ARGS__); }

int tdszDecompress(int type, const char * input, int compressedSize, const int nelements, const char * output)
{
#ifdef DECOMPRESS_TRACE
  vInfo("entering %s", __func__);
#endif

	size_t outSize = SZ_decompress(type, (void*)input, compressedSize, (size_t)nelements, (unsigned char*)output);

#ifdef DECOMPRESS_TRACE
  vInfo("exiting %s", __func__);
#endif
    return (int)outSize;
}

//
//  tdszExit
//
void tdszExit()
{
	if(confparams_cpr!=NULL)
	{
		free(confparams_cpr);
		confparams_cpr = NULL;
	}	
	if(exe_params!=NULL)
	{
		free(exe_params);
		exe_params = NULL;
	}
}