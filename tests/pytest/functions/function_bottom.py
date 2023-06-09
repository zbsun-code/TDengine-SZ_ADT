###################################################################
#           Copyright (c) 2016 by TAOS Technologies, Inc.
#                     All rights reserved.
#
#  This file is proprietary and confidential to TAOS Technologies.
#  No part of this file may be reproduced, stored, transmitted,
#  disclosed or used in any form or by any means other than as
#  expressly provided by the written permission from Jianhui Tao
#
###################################################################

# -*- coding: utf-8 -*-

import sys
import taos
from util.log import *
from util.cases import *
from util.sql import *
import numpy as np


class TDTestCase:
    def init(self, conn, logSql):
        tdLog.debug("start to execute %s" % __file__)
        tdSql.init(conn.cursor())

        self.rowNum = 10
        self.ts = 1537146000000
        
    def run(self):
        tdSql.prepare()    

        tdSql.execute('''create table test(ts timestamp, col1 tinyint, col2 smallint, col3 int, col4 bigint, col5 float, col6 double, 
                    col7 bool, col8 binary(20), col9 nchar(20), col11 tinyint unsigned, col12 smallint unsigned, col13 int unsigned, col14 bigint unsigned) tags(loc nchar(20))''')
        tdSql.execute("create table test1 using test tags('beijing')")
        for i in range(self.rowNum):
            tdSql.execute("insert into test1 values(%d, %d, %d, %d, %d, %f, %f, %d, 'taosdata%d', '涛思数据%d', %d, %d, %d, %d)" 
                        % (self.ts + i, i + 1, i + 1, i + 1, i + 1, i + 0.1, i + 0.1, i % 2, i + 1, i + 1, i + 1, i + 1, i + 1, i + 1))                            

        # bottom verifacation 
        tdSql.error("select bottom(ts, 10) from test")
        tdSql.error("select bottom(col1, 0) from test")
        tdSql.error("select bottom(col1, 101) from test")
        tdSql.error("select bottom(col2, 0) from test")
        tdSql.error("select bottom(col2, 101) from test")
        tdSql.error("select bottom(col3, 0) from test")
        tdSql.error("select bottom(col3, 101) from test")
        tdSql.error("select bottom(col4, 0) from test")
        tdSql.error("select bottom(col4, 101) from test")
        tdSql.error("select bottom(col5, 0) from test")
        tdSql.error("select bottom(col5, 101) from test")
        tdSql.error("select bottom(col6, 0) from test")
        tdSql.error("select bottom(col6, 101) from test")        
        tdSql.error("select bottom(col7, 10) from test")        
        tdSql.error("select bottom(col8, 10) from test")
        tdSql.error("select bottom(col9, 10) from test")

        tdSql.query("select bottom(col1, 2) from test")
        tdSql.checkRows(2)
        tdSql.checkData(0, 1, 1)
        tdSql.checkData(1, 1, 2)

        tdSql.query("select bottom(col2, 2) from test")
        tdSql.checkRows(2)
        tdSql.checkData(0, 1, 1)
        tdSql.checkData(1, 1, 2)

        tdSql.query("select bottom(col3, 2) from test")
        tdSql.checkRows(2)
        tdSql.checkData(0, 1, 1)
        tdSql.checkData(1, 1, 2)

        tdSql.query("select bottom(col4, 2) from test")
        tdSql.checkRows(2)
        tdSql.checkData(0, 1, 1)
        tdSql.checkData(1, 1, 2)

        tdSql.query("select bottom(col5, 2) from test")
        tdSql.checkRows(2)
        tdSql.checkData(0, 1, 0.1)
        tdSql.checkData(1, 1, 1.1)

        tdSql.query("select bottom(col6, 2) from test")
        tdSql.checkRows(2)
        tdSql.checkData(0, 1, 0.1)
        tdSql.checkData(1, 1, 1.1)

        tdSql.query("select bottom(col11, 2) from test")
        tdSql.checkRows(2)
        tdSql.checkData(0, 1, 1)
        tdSql.checkData(1, 1, 2)

        tdSql.query("select bottom(col12, 2) from test")
        tdSql.checkRows(2)
        tdSql.checkData(0, 1, 1)
        tdSql.checkData(1, 1, 2)

        tdSql.query("select bottom(col13, 2) from test")
        tdSql.checkRows(2)
        tdSql.checkData(0, 1, 1)
        tdSql.checkData(1, 1, 2)

        tdSql.query("select bottom(col14, 2) from test")
        tdSql.checkRows(2)
        tdSql.checkData(0, 1, 1)
        tdSql.checkData(1, 1, 2)

        tdSql.query("select ts,bottom(col1, 2),ts from test1")
        tdSql.checkRows(2)
        tdSql.checkData(0, 0, "2018-09-17 09:00:00.000")
        tdSql.checkData(0, 1, "2018-09-17 09:00:00.000")
        tdSql.checkData(1, 0, "2018-09-17 09:00:00.001")
        tdSql.checkData(1, 3, "2018-09-17 09:00:00.001")


        tdSql.query("select ts,bottom(col1, 2),ts from test group by tbname")
        tdSql.checkRows(2)
        tdSql.checkData(0, 0, "2018-09-17 09:00:00.000")
        tdSql.checkData(0, 1, "2018-09-17 09:00:00.000")
        tdSql.checkData(1, 0, "2018-09-17 09:00:00.001")
        tdSql.checkData(1, 3, "2018-09-17 09:00:00.001")
                   
        #TD-2457 bottom + interval + order by
        tdSql.error('select top(col2,1) from test interval(1y) order by col2;')

        #TD-2563 top + super_table + interval 
        tdSql.execute("create table meters(ts timestamp, c int) tags (d int)") 
        tdSql.execute("create table t1 using meters tags (1)") 
        sql = 'insert into t1 values '       
        for i in range(20000):
            sql = sql + '(%d, %d)' % (self.ts + i , i % 47)
            if i % 2000 == 0:
                tdSql.execute(sql)
                sql = 'insert into t1 values ' 
        tdSql.execute(sql)
        tdSql.query('select bottom(c,1) from meters interval(10a)')
        tdSql.checkData(0,1,0)
        
        # TD-15187 test case
        tdSql.execute("create database dd keep 36500")
        tdSql.execute("use dd")
        tdSql.execute("create table table_1(ts timestamp , q_int int,q_bool bool)")
        tdSql.execute("insert into table_1 (ts , q_int,q_bool) values(1630000000000, 1,0)")
        tdSql.execute("insert into table_1 (ts , q_int,q_bool) values(1630000010000, 2,0)")
        tdSql.execute("insert into table_1 (ts , q_int,q_bool) values(1630000020000, 3,0)")
        tdSql.execute("insert into table_1 (ts , q_int,q_bool) values(1630000100000, 3,0)")
        tdSql.execute("insert into table_1 (ts , q_int,q_bool) values(1630000110000, 2,0)")
        tdSql.execute("insert into table_1 (ts , q_int,q_bool) values(1630000120000, 1,0)")
        
        tdSql.query("select BOTTOM(q_int,40) from table_1 SESSION(ts,10m) order by ts")
        tdSql.checkData(0, 1, 1)
        tdSql.checkData(1, 1, 2)
        tdSql.checkData(2, 1, 3)
        tdSql.checkData(3, 1, 3)
        tdSql.checkData(4, 1, 2)
        tdSql.checkData(5, 1, 1)
        
        tdSql.query("select BOTTOM(q_int,40) from table_1 SESSION(ts,10m) order by ts desc;")
        tdSql.checkData(0, 1, 1)
        tdSql.checkData(1, 1, 2)
        tdSql.checkData(2, 1, 3)
        tdSql.checkData(3, 1, 3)
        tdSql.checkData(4, 1, 2)
        tdSql.checkData(5, 1, 1)

    def stop(self):
        tdSql.close()
        tdLog.success("%s successfully executed" % __file__)

tdCases.addWindows(__file__, TDTestCase())
tdCases.addLinux(__file__, TDTestCase())
