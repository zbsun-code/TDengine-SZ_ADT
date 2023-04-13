###################################################################
#           Copyright (c) 2021 by TAOS Technologies, Inc.
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
from util.log import *
from util.cases import *
from util.sql import *


class TDTestCase:
    def caseDescription(self):
        '''
        case1<Ganlin Zhao>: [TD-11222]<feature>: Histogram function
        '''
        return

    def init(self, conn, logSql):
        tdLog.debug("start to execute %s" % __file__)
        tdSql.init(conn.cursor(), logSql)

    def getBuildPath(self):
        selfPath = os.path.dirname(os.path.realpath(__file__))

        if ("community" in selfPath):
            projPath = selfPath[:selfPath.find("community")]
        else:
            projPath = selfPath[:selfPath.find("tests")]

        for root, dirs, files in os.walk(projPath):
            if ("taosd" in files):
                rootRealPath = os.path.dirname(os.path.realpath(root))
                if ("packaging" not in rootRealPath):
                    buildPath = root[:len(root) - len("/build/bin")]
                    break
        return buildPath

    def run(self):
        print("running {}".format(__file__))
        tdSql.execute("drop database if exists db")
        tdSql.execute("create database if not exists db")
        tdSql.execute('use db')

        #Prepare data
        tdSql.execute("create stable stb (col_timestamp timestamp, col_tinyint tinyint, col_smallint smallint, col_int int, col_bigint bigint, col_float float, col_double double, col_bool bool, col_binary binary(10), col_nchar nchar(10)) \
                       tags(tag_timestamp timestamp, tag_tinyint tinyint, tag_smallint smallint, tag_int int, tag_bigint bigint, tag_float float, tag_double double, tag_bool bool, tag_binary binary(10), tag_nchar nchar(10));")
        tdSql.execute("create table ctb using stb tags (now, 1, 1, 1, 1, 1.0, 1.0, true, 'abc', 'abc');")
        tdSql.execute("create table tb (col_timestamp timestamp, col_tinyint tinyint, col_smallint smallint, col_int int, col_bigint bigint, col_float float, col_double double, col_bool bool, col_binary binary(10), col_nchar nchar(10));")

        tdSql.execute("insert into ctb values (now, -9, -9, -9, -9, -9.5, -9.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb values (now + 1s, -1, -1, -1, -1, -1.5, -1.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb values (now + 2s, 1, 1, 1, 1, 1.5, 1.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb values (now + 3s, 2, 2, 2, 2, 2.5, 2.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb values (now + 4s, 3, 3, 3, 3, 3.5, 3.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb values (now + 5s, 4, 4, 4, 4, 4.5, 4.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb values (now + 6s, 5, 5, 5, 5, 5.5, 5.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb values (now + 7s, 6, 6, 6, 6, 6.5, 6.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb values (now + 8s, 7, 7, 7, 7, 7.5, 7.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb values (now + 9s, 8, 8, 8, 8, 8.5, 8.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb values (now + 10s, 9, 9, 9, 9, 9.5, 9.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb values (now + 11s, 10, 10, 10, 10, 10.5, 10.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb values (now + 12s, 15, 15, 15, 15, 15.5, 15.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb values (now + 13s, 20, 20, 20, 20, 20.5, 20.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb values (now + 14s, 99, 99, 99, 99, 99.5, 99.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb values (now + 15s, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);")

        tdSql.execute("insert into tb values (now, -9, -9, -9, -9, -9.5, -9.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb values (now + 1s, -1, -1, -1, -1, -1.5, -1.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb values (now + 2s, 1, 1, 1, 1, 1.5, 1.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb values (now + 3s, 2, 2, 2, 2, 2.5, 2.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb values (now + 4s, 3, 3, 3, 3, 3.5, 3.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb values (now + 5s, 4, 4, 4, 4, 4.5, 4.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb values (now + 6s, 5, 5, 5, 5, 5.5, 5.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb values (now + 7s, 6, 6, 6, 6, 6.5, 6.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb values (now + 8s, 7, 7, 7, 7, 7.5, 7.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb values (now + 9s, 8, 8, 8, 8, 8.5, 8.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb values (now + 10s, 9, 9, 9, 9, 9.5, 9.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb values (now + 11s, 10, 10, 10, 10, 10.5, 10.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb values (now + 12s, 15, 15, 15, 15, 15.5, 15.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb values (now + 13s, 20, 20, 20, 20, 20.5, 20.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb values (now + 14s, 99, 99, 99, 99, 99.5, 99.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb values (now + 15s, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);")

        #execute query
        print("============== STEP 1: column types  ================== ")
        #Supported column types
        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5,7]", 0) from tb;')
        tdSql.checkRows(3);

        tdSql.query('select histogram(col_smallint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.query('select histogram(col_smallint, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.query('select histogram(col_smallint, "user_input", "[1,3,5,7]", 0) from tb;')
        tdSql.checkRows(3);

        tdSql.query('select histogram(col_int, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.query('select histogram(col_int, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.query('select histogram(col_int, "user_input", "[1,3,5,7]", 0) from tb;')
        tdSql.checkRows(3);

        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7]", 0) from tb;')
        tdSql.checkRows(3);

        tdSql.query('select histogram(col_float, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.query('select histogram(col_float, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.query('select histogram(col_float, "user_input", "[1,3,5,7]", 0) from tb;')
        tdSql.checkRows(3);

        tdSql.query('select histogram(col_double, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.query('select histogram(col_double, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.query('select histogram(col_double, "user_input", "[1,3,5,7]", 0) from tb;')
        tdSql.checkRows(3);

        #Unsupported column types
        tdSql.error('select histogram(col_timestamp, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_timestamp, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.error('select histogram(col_timestamp, "user_input", "[1,3,5,7]", 0) from tb;')

        tdSql.error('select histogram(col_bool, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_bool, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.error('select histogram(col_bool, "user_input", "[1,3,5,7]", 0) from tb;')

        tdSql.error('select histogram(col_binary, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_binary, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.error('select histogram(col_binary, "user_input", "[1,3,5,7]", 0) from tb;')

        tdSql.error('select histogram(col_nchar, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_nchar, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.error('select histogram(col_nchar, "user_input", "[1,3,5,7]", 0) from tb;')

        tdSql.error('select histogram(col, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.error('select histogram(col, "user_input", "[1,3,5,7]", 0) from tb;')

        #Unsupported tags
        tdSql.error('select histogram(tag_timestamp, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(tag_timestamp, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.error('select histogram(tag_timestamp, "user_input", "[1,3,5,7]", 0) from tb;')

        tdSql.error('select histogram(tag_tinyint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(tag_tinyint, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.error('select histogram(tag_tinyint, "user_input", "[1,3,5,7]", 0) from tb;')

        tdSql.error('select histogram(tag_smallint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(tag_smallint, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.error('select histogram(tag_smallint, "user_input", "[1,3,5,7]", 0) from tb;')

        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0) from tb;')

        tdSql.error('select histogram(tag_bigint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(tag_bigint, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.error('select histogram(tag_bigint, "user_input", "[1,3,5,7]", 0) from tb;')

        tdSql.error('select histogram(tag_float, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(tag_float, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.error('select histogram(tag_float, "user_input", "[1,3,5,7]", 0) from tb;')

        tdSql.error('select histogram(tag_double, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(tag_double, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.error('select histogram(tag_double, "user_input", "[1,3,5,7]", 0) from tb;')

        tdSql.error('select histogram(tag_bool, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(tag_bool, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.error('select histogram(tag_bool, "user_input", "[1,3,5,7]", 0) from tb;')

        tdSql.error('select histogram(tag_binary, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(tag_binary, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.error('select histogram(tag_binary, "user_input", "[1,3,5,7]", 0) from tb;')

        tdSql.error('select histogram(tag_nchar, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(tag_nchar, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.error('select histogram(tag_nchar, "user_input", "[1,3,5,7]", 0) from tb;')


        print("============== STEP 2: bin types  ================== ")
        ## user_input ##
        #TINYINT
        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5]", 0) from stb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5]", 0) from ctb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5]", 0) from tb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');


        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5,7]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');

        tdSql.query('select histogram(col_tinyint, "user_input", "[0,10,20,100]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":10, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[0,10,20,100]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":10, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[0,10,20,100]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":10, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');

        tdSql.query('select histogram(col_tinyint, "user_input", "[-10,10,20,100]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":10, "count":12}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[-10,10,20,100]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":10, "count":12}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[-10,10,20,100]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":10, "count":12}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');

        tdSql.query('select histogram(col_tinyint, "user_input", "[-8.9,9.9,19.9,99.9]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-8.9, "upper_bin":9.9, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":99.9, "count":2}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[-8.9,9.9,19.9,99.9]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-8.9, "upper_bin":9.9, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":99.9, "count":2}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[-8.9,9.9,19.9,99.9]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-8.9, "upper_bin":9.9, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":99.9, "count":2}');

        tdSql.query('select histogram(col_tinyint, "user_input", "[-99999999999999,9.9,19.9,99999999999999]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-1e+14, "upper_bin":9.9, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":1e+14, "count":2}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[-99999999999999,9.9,19.9,99999999999999]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-1e+14, "upper_bin":9.9, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":1e+14, "count":2}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[-99999999999999,9.9,19.9,99999999999999]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-1e+14, "upper_bin":9.9, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":1e+14, "count":2}');

        #SMALLINT
        tdSql.query('select histogram(col_smallint, "user_input", "[1,3,5]", 0) from stb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.query('select histogram(col_smallint, "user_input", "[1,3,5]", 0) from ctb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.query('select histogram(col_smallint, "user_input", "[1,3,5]", 0) from tb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');

        tdSql.query('select histogram(col_smallint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.query('select histogram(col_smallint, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.query('select histogram(col_smallint, "user_input", "[1,3,5,7]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');

        tdSql.query('select histogram(col_smallint, "user_input", "[0,10,20,100]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":10, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');
        tdSql.query('select histogram(col_smallint, "user_input", "[0,10,20,100]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":10, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');
        tdSql.query('select histogram(col_smallint, "user_input", "[0,10,20,100]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":10, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');

        tdSql.query('select histogram(col_smallint, "user_input", "[-10,10,20,100]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":10, "count":12}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');
        tdSql.query('select histogram(col_smallint, "user_input", "[-10,10,20,100]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":10, "count":12}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');
        tdSql.query('select histogram(col_smallint, "user_input", "[-10,10,20,100]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":10, "count":12}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');

        tdSql.query('select histogram(col_smallint, "user_input", "[-8.9,9.9,19.9,99.9]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-8.9, "upper_bin":9.9, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":99.9, "count":2}');
        tdSql.query('select histogram(col_smallint, "user_input", "[-8.9,9.9,19.9,99.9]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-8.9, "upper_bin":9.9, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":99.9, "count":2}');
        tdSql.query('select histogram(col_smallint, "user_input", "[-8.9,9.9,19.9,99.9]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-8.9, "upper_bin":9.9, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":99.9, "count":2}');

        tdSql.query('select histogram(col_smallint, "user_input", "[-99999999999999,9.9,19.9,99999999999999]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-1e+14, "upper_bin":9.9, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":1e+14, "count":2}');
        tdSql.query('select histogram(col_smallint, "user_input", "[-99999999999999,9.9,19.9,99999999999999]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-1e+14, "upper_bin":9.9, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":1e+14, "count":2}');
        tdSql.query('select histogram(col_smallint, "user_input", "[-99999999999999,9.9,19.9,99999999999999]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-1e+14, "upper_bin":9.9, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":1e+14, "count":2}');

        #INT
        tdSql.query('select histogram(col_int, "user_input", "[1,3,5]", 0) from stb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[1,3,5]", 0) from ctb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[1,3,5]", 0) from tb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');

        tdSql.query('select histogram(col_int, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[1,3,5,7]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');

        tdSql.query('select histogram(col_int, "user_input", "[0,10,20,100]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":10, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');
        tdSql.query('select histogram(col_int, "user_input", "[0,10,20,100]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":10, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');
        tdSql.query('select histogram(col_int, "user_input", "[0,10,20,100]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":10, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');

        tdSql.query('select histogram(col_int, "user_input", "[-10,10,20,100]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":10, "count":12}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');
        tdSql.query('select histogram(col_int, "user_input", "[-10,10,20,100]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":10, "count":12}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');
        tdSql.query('select histogram(col_int, "user_input", "[-10,10,20,100]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":10, "count":12}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');

        tdSql.query('select histogram(col_int, "user_input", "[-8.9,9.9,19.9,99.9]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-8.9, "upper_bin":9.9, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":99.9, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[-8.9,9.9,19.9,99.9]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-8.9, "upper_bin":9.9, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":99.9, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[-8.9,9.9,19.9,99.9]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-8.9, "upper_bin":9.9, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":99.9, "count":2}');

        tdSql.query('select histogram(col_int, "user_input", "[-99999999999999,9.9,19.9,99999999999999]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-1e+14, "upper_bin":9.9, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":1e+14, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[-99999999999999,9.9,19.9,99999999999999]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-1e+14, "upper_bin":9.9, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":1e+14, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[-99999999999999,9.9,19.9,99999999999999]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-1e+14, "upper_bin":9.9, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":1e+14, "count":2}');

        #BIGINT
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5]", 0) from stb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5]", 0) from ctb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5]", 0) from tb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');

        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');

        tdSql.query('select histogram(col_bigint, "user_input", "[0,10,20,100]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":10, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');
        tdSql.query('select histogram(col_bigint, "user_input", "[0,10,20,100]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":10, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');
        tdSql.query('select histogram(col_bigint, "user_input", "[0,10,20,100]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":10, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');

        tdSql.query('select histogram(col_bigint, "user_input", "[-10,10,20,100]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":10, "count":12}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');
        tdSql.query('select histogram(col_bigint, "user_input", "[-10,10,20,100]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":10, "count":12}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');
        tdSql.query('select histogram(col_bigint, "user_input", "[-10,10,20,100]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":10, "count":12}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":1}');

        tdSql.query('select histogram(col_bigint, "user_input", "[-8.9,9.9,19.9,99.9]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-8.9, "upper_bin":9.9, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":99.9, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[-8.9,9.9,19.9,99.9]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-8.9, "upper_bin":9.9, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":99.9, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[-8.9,9.9,19.9,99.9]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-8.9, "upper_bin":9.9, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":99.9, "count":2}');

        tdSql.query('select histogram(col_bigint, "user_input", "[-99999999999999,9.9,19.9,99999999999999]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-1e+14, "upper_bin":9.9, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":1e+14, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[-99999999999999,9.9,19.9,99999999999999]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-1e+14, "upper_bin":9.9, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":1e+14, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[-99999999999999,9.9,19.9,99999999999999]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-1e+14, "upper_bin":9.9, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":1e+14, "count":2}');

        #FLOAT
        tdSql.query('select histogram(col_float, "user_input", "[1,3,5]", 0) from stb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.query('select histogram(col_float, "user_input", "[1,3,5]", 0) from ctb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.query('select histogram(col_float, "user_input", "[1,3,5]", 0) from tb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');

        tdSql.query('select histogram(col_float, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.query('select histogram(col_float, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.query('select histogram(col_float, "user_input", "[1,3,5,7]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');

        tdSql.query('select histogram(col_float, "user_input", "[0,10,20,100]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":10, "count":9}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":2}');
        tdSql.query('select histogram(col_float, "user_input", "[0,10,20,100]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":10, "count":9}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":2}');
        tdSql.query('select histogram(col_float, "user_input", "[0,10,20,100]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":10, "count":9}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":2}');

        tdSql.query('select histogram(col_float, "user_input", "[-10,10,20,100]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":10, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":2}');
        tdSql.query('select histogram(col_float, "user_input", "[-10,10,20,100]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":10, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":2}');
        tdSql.query('select histogram(col_float, "user_input", "[-10,10,20,100]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":10, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":2}');

        tdSql.query('select histogram(col_float, "user_input", "[-9.4,9.6,20.4,99.9]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-9.4, "upper_bin":9.6, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":9.6, "upper_bin":20.4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20.4, "upper_bin":99.9, "count":2}');
        tdSql.query('select histogram(col_float, "user_input", "[-9.4,9.6,20.4,99.9]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-9.4, "upper_bin":9.6, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":9.6, "upper_bin":20.4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20.4, "upper_bin":99.9, "count":2}');
        tdSql.query('select histogram(col_float, "user_input", "[-9.4,9.6,20.4,99.9]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-9.4, "upper_bin":9.6, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":9.6, "upper_bin":20.4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20.4, "upper_bin":99.9, "count":2}');

        tdSql.query('select histogram(col_float, "user_input", "[-99999999999999,9.9,19.9,99999999999999]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-1e+14, "upper_bin":9.9, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":1e+14, "count":2}');
        tdSql.query('select histogram(col_float, "user_input", "[-99999999999999,9.9,19.9,99999999999999]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-1e+14, "upper_bin":9.9, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":1e+14, "count":2}');
        tdSql.query('select histogram(col_float, "user_input", "[-99999999999999,9.9,19.9,99999999999999]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-1e+14, "upper_bin":9.9, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":1e+14, "count":2}');

        #DOUBLE
        tdSql.query('select histogram(col_double, "user_input", "[1,3,5]", 0) from stb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.query('select histogram(col_double, "user_input", "[1,3,5]", 0) from ctb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.query('select histogram(col_double, "user_input", "[1,3,5]", 0) from tb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');

        tdSql.query('select histogram(col_double, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.query('select histogram(col_double, "user_input", "[1,3,5,7]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.query('select histogram(col_double, "user_input", "[1,3,5,7]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');

        tdSql.query('select histogram(col_double, "user_input", "[0,10,20,100]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":10, "count":9}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":2}');
        tdSql.query('select histogram(col_double, "user_input", "[0,10,20,100]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":10, "count":9}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":2}');
        tdSql.query('select histogram(col_double, "user_input", "[0,10,20,100]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":10, "count":9}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":2}');

        tdSql.query('select histogram(col_double, "user_input", "[-10,10,20,100]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":10, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":2}');
        tdSql.query('select histogram(col_double, "user_input", "[-10,10,20,100]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":10, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":2}');
        tdSql.query('select histogram(col_double, "user_input", "[-10,10,20,100]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":10, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":10, "upper_bin":20, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20, "upper_bin":100, "count":2}');

        tdSql.query('select histogram(col_double, "user_input", "[-9.4,9.6,20.4,99.9]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-9.4, "upper_bin":9.6, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":9.6, "upper_bin":20.4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20.4, "upper_bin":99.9, "count":2}');
        tdSql.query('select histogram(col_double, "user_input", "[-9.4,9.6,20.4,99.9]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-9.4, "upper_bin":9.6, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":9.6, "upper_bin":20.4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20.4, "upper_bin":99.9, "count":2}');
        tdSql.query('select histogram(col_double, "user_input", "[-9.4,9.6,20.4,99.9]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-9.4, "upper_bin":9.6, "count":10}');
        tdSql.checkData(1, 0, '{"lower_bin":9.6, "upper_bin":20.4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":20.4, "upper_bin":99.9, "count":2}');

        tdSql.query('select histogram(col_double, "user_input", "[-99999999999999,9.9,19.9,99999999999999]", 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-1e+14, "upper_bin":9.9, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":1e+14, "count":2}');
        tdSql.query('select histogram(col_double, "user_input", "[-99999999999999,9.9,19.9,99999999999999]", 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-1e+14, "upper_bin":9.9, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":1e+14, "count":2}');
        tdSql.query('select histogram(col_double, "user_input", "[-99999999999999,9.9,19.9,99999999999999]", 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-1e+14, "upper_bin":9.9, "count":11}');
        tdSql.checkData(1, 0, '{"lower_bin":9.9, "upper_bin":19.9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":19.9, "upper_bin":1e+14, "count":2}');

        #ERROR CASE
        tdSql.error('select histogram(col_double, 1, "[1,5,3,7]", 0) from stb;')
        tdSql.error('select histogram(col_double, 1, "[1,5,3,7]", 0) from ctb;')
        tdSql.error('select histogram(col_double, 1, "[1,5,3,7]", 0) from tb;')
        tdSql.error('select histogram(col_double, -1.0, "[1,5,3,7]", 0) from stb;')
        tdSql.error('select histogram(col_double, -1.0, "[1,5,3,7]", 0) from ctb;')
        tdSql.error('select histogram(col_double, -1.0, "[1,5,3,7]", 0) from tb;')
        tdSql.error('select histogram(col_double, true, "[1,5,3,7]", 0) from stb;')
        tdSql.error('select histogram(col_double, false, "[1,5,3,7]", 0) from ctb;')
        tdSql.error('select histogram(col_double, true, "[1,5,3,7]", 0) from tb;')
        tdSql.error('select histogram(col_double, "user", "[1,5,3,7]", 0) from stb;')
        tdSql.error('select histogram(col_double, "user", "[1,5,3,7]", 0) from ctb;')
        tdSql.error('select histogram(col_double, "user", "[1,5,3,7]", 0) from tb;')
        tdSql.error('select histogram(col_double, "user_input", "[1,5,3,7]", 0) from stb;')
        tdSql.error('select histogram(col_double, "user_input", "[1,5,3,7]", 0) from ctb;')
        tdSql.error('select histogram(col_double, "user_input", "[1,5,3,7]", 0) from tb;')
        tdSql.error('select histogram(col_double, "user_input", "[1,-1,3,-3]", 0) from stb;')
        tdSql.error('select histogram(col_double, "user_input", "[1,-1,3,-3]", 0) from ctb;')
        tdSql.error('select histogram(col_double, "user_input", "[1,-1,3,-3]", 0) from tb;')
        tdSql.error('select histogram(col_double, "user_input", "[1.0,5.5,3.3,7.7]", 0) from stb;')
        tdSql.error('select histogram(col_double, "user_input", "[1.0,5.5,3.3,7.7]", 0) from ctb;')
        tdSql.error('select histogram(col_double, "user_input", "[1.0,5.5,3.3,7.7]", 0) from tb;')
        tdSql.error('select histogram(col_double, "user_input", "[1,1,1]", 0) from stb;')
        tdSql.error('select histogram(col_double, "user_input", "[1,1,1]", 0) from ctb;')
        tdSql.error('select histogram(col_double, "user_input", "[1,1,1]", 0) from tb;')
        tdSql.error('select histogram(col_double, "user_input", "[-1,-1,1]", 0) from stb;')
        tdSql.error('select histogram(col_double, "user_input", "[-1,-1,1]", 0) from ctb;')
        tdSql.error('select histogram(col_double, "user_input", "[-1,-1,1]", 0) from tb;')
        tdSql.error('select histogram(col_double, "user_input", "[false,3,5]", 0) from stb;')
        tdSql.error('select histogram(col_double, "user_input", "[false,3,5]", 0) from ctb;')
        tdSql.error('select histogram(col_double, "user_input", "[false,3,5]", 0) from tb;')
        tdSql.error('select histogram(col_double, "user_input", "[1,true,5]", 0) from stb;')
        tdSql.error('select histogram(col_double, "user_input", "[1,true,5]", 0) from ctb;')
        tdSql.error('select histogram(col_double, "user_input", "[1,true,5]", 0) from tb;')
        tdSql.error('select histogram(col_double, "user_input", "[1.0,"abc",5]", 0) from stb;')
        tdSql.error('select histogram(col_double, "user_input", "[1.0,"abc",5]", 0) from ctb;')
        tdSql.error('select histogram(col_double, "user_input", "[1.0,"abc",5]", 0) from tb;')
        tdSql.error('select histogram(col_double, "user_input", "[1.0, 5, "中文"]", 0) from stb;')
        tdSql.error('select histogram(col_double, "user_input", "[1.0, 5, "中文"]", 0) from ctb;')
        tdSql.error('select histogram(col_double, "user_input", "[1.0, 5, "中文"]", 0) from tb;')
        tdSql.error('select histogram(col_double, "user_input", "{1.0, 3.0, 5.0}", 0) from stb;')
        tdSql.error('select histogram(col_double, "user_input", "{1.0, 3.0, 5.0}", 0) from ctb;')
        tdSql.error('select histogram(col_double, "user_input", "{1.0, 3.0, 5.0}", 0) from tb;')
        tdSql.error('select histogram(col_double, \'user_input\', \'{"start": 1.0, "width": 3.0, "count": 5, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_double, \'user_input\', \'{"start": 1.0, "width": 3.0, "count": 5, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_double, \'user_input\', \'{"start": 1.0, "width": 3.0, "count": 5, "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_double, \'user_input\', \'{"start": 1.0, "factor": 3.0, "count": 5, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_double, \'user_input\', \'{"start": 1.0, "factor": 3.0, "count": 5, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_double, \'user_input\', \'{"start": 1.0, "factor": 3.0, "count": 5, "infinity": true}\', 0) from tb;')


        ## linear_bins ##
        #INTEGER
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": 1, "width": 3, "count": 8, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(8);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":4, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":4, "upper_bin":7, "count":3}');
        tdSql.checkData(2, 0, '{"lower_bin":7, "upper_bin":10, "count":3}');
        tdSql.checkData(3, 0, '{"lower_bin":10, "upper_bin":13, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":13, "upper_bin":16, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":16, "upper_bin":19, "count":0}');
        tdSql.checkData(6, 0, '{"lower_bin":19, "upper_bin":22, "count":1}');
        tdSql.checkData(7, 0, '{"lower_bin":22, "upper_bin":25, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": 1, "width": 3, "count": 8, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(8);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":4, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":4, "upper_bin":7, "count":3}');
        tdSql.checkData(2, 0, '{"lower_bin":7, "upper_bin":10, "count":3}');
        tdSql.checkData(3, 0, '{"lower_bin":10, "upper_bin":13, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":13, "upper_bin":16, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":16, "upper_bin":19, "count":0}');
        tdSql.checkData(6, 0, '{"lower_bin":19, "upper_bin":22, "count":1}');
        tdSql.checkData(7, 0, '{"lower_bin":22, "upper_bin":25, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": 1, "width": 3, "count": 8, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(8);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":4, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":4, "upper_bin":7, "count":3}');
        tdSql.checkData(2, 0, '{"lower_bin":7, "upper_bin":10, "count":3}');
        tdSql.checkData(3, 0, '{"lower_bin":10, "upper_bin":13, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":13, "upper_bin":16, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":16, "upper_bin":19, "count":0}');
        tdSql.checkData(6, 0, '{"lower_bin":19, "upper_bin":22, "count":1}');
        tdSql.checkData(7, 0, '{"lower_bin":22, "upper_bin":25, "count":0}');

        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": -10.0, "width": 3.0, "count": 8, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(8);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":-7, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":-7, "upper_bin":-4, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-4, "upper_bin":-1, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":-1, "upper_bin":2, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":2, "upper_bin":5, "count":3}');
        tdSql.checkData(5, 0, '{"lower_bin":5, "upper_bin":8, "count":3}');
        tdSql.checkData(6, 0, '{"lower_bin":8, "upper_bin":11, "count":2}');
        tdSql.checkData(7, 0, '{"lower_bin":11, "upper_bin":14, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": -10.0, "width": 3.0, "count": 8, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(8);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":-7, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":-7, "upper_bin":-4, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-4, "upper_bin":-1, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":-1, "upper_bin":2, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":2, "upper_bin":5, "count":3}');
        tdSql.checkData(5, 0, '{"lower_bin":5, "upper_bin":8, "count":3}');
        tdSql.checkData(6, 0, '{"lower_bin":8, "upper_bin":11, "count":2}');
        tdSql.checkData(7, 0, '{"lower_bin":11, "upper_bin":14, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": -10.0, "width": 3.0, "count": 8, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(8);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":-7, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":-7, "upper_bin":-4, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-4, "upper_bin":-1, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":-1, "upper_bin":2, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":2, "upper_bin":5, "count":3}');
        tdSql.checkData(5, 0, '{"lower_bin":5, "upper_bin":8, "count":3}');
        tdSql.checkData(6, 0, '{"lower_bin":8, "upper_bin":11, "count":2}');
        tdSql.checkData(7, 0, '{"lower_bin":11, "upper_bin":14, "count":0}');

        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": -2.5, "width": 0.5, "count": 8, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(8);
        tdSql.checkData(0, 0, '{"lower_bin":-2.5, "upper_bin":-2, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-2, "upper_bin":-1.5, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-1.5, "upper_bin":-1, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":-1, "upper_bin":-0.5, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":-0.5, "upper_bin":0, "count":0}');
        tdSql.checkData(5, 0, '{"lower_bin":0, "upper_bin":0.5, "count":0}');
        tdSql.checkData(6, 0, '{"lower_bin":0.5, "upper_bin":1, "count":1}');
        tdSql.checkData(7, 0, '{"lower_bin":1, "upper_bin":1.5, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": -2.5, "width": 0.5, "count": 8, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(8);
        tdSql.checkData(0, 0, '{"lower_bin":-2.5, "upper_bin":-2, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-2, "upper_bin":-1.5, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-1.5, "upper_bin":-1, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":-1, "upper_bin":-0.5, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":-0.5, "upper_bin":0, "count":0}');
        tdSql.checkData(5, 0, '{"lower_bin":0, "upper_bin":0.5, "count":0}');
        tdSql.checkData(6, 0, '{"lower_bin":0.5, "upper_bin":1, "count":1}');
        tdSql.checkData(7, 0, '{"lower_bin":1, "upper_bin":1.5, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": -2.5, "width": 0.5, "count": 8, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(8);
        tdSql.checkData(0, 0, '{"lower_bin":-2.5, "upper_bin":-2, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-2, "upper_bin":-1.5, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-1.5, "upper_bin":-1, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":-1, "upper_bin":-0.5, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":-0.5, "upper_bin":0, "count":0}');
        tdSql.checkData(5, 0, '{"lower_bin":0, "upper_bin":0.5, "count":0}');
        tdSql.checkData(6, 0, '{"lower_bin":0.5, "upper_bin":1, "count":1}');
        tdSql.checkData(7, 0, '{"lower_bin":1, "upper_bin":1.5, "count":0}');

        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": 4, "width": -0.5, "count": 10, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(10);
        tdSql.checkData(0, 0, '{"lower_bin":3.5, "upper_bin":4, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":3.5, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":2.5, "upper_bin":3, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":2, "upper_bin":2.5, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":1.5, "upper_bin":2, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":1, "upper_bin":1.5, "count":0}');
        tdSql.checkData(6, 0, '{"lower_bin":0.5, "upper_bin":1, "count":1}');
        tdSql.checkData(7, 0, '{"lower_bin":0, "upper_bin":0.5, "count":0}');
        tdSql.checkData(8, 0, '{"lower_bin":-0.5, "upper_bin":0, "count":0}');
        tdSql.checkData(9, 0, '{"lower_bin":-1, "upper_bin":-0.5, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": 4, "width": -0.5, "count": 10, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(10);
        tdSql.checkData(0, 0, '{"lower_bin":3.5, "upper_bin":4, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":3.5, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":2.5, "upper_bin":3, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":2, "upper_bin":2.5, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":1.5, "upper_bin":2, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":1, "upper_bin":1.5, "count":0}');
        tdSql.checkData(6, 0, '{"lower_bin":0.5, "upper_bin":1, "count":1}');
        tdSql.checkData(7, 0, '{"lower_bin":0, "upper_bin":0.5, "count":0}');
        tdSql.checkData(8, 0, '{"lower_bin":-0.5, "upper_bin":0, "count":0}');
        tdSql.checkData(9, 0, '{"lower_bin":-1, "upper_bin":-0.5, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": 4, "width": -0.5, "count": 10, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(10);
        tdSql.checkData(0, 0, '{"lower_bin":3.5, "upper_bin":4, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":3.5, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":2.5, "upper_bin":3, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":2, "upper_bin":2.5, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":1.5, "upper_bin":2, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":1, "upper_bin":1.5, "count":0}');
        tdSql.checkData(6, 0, '{"lower_bin":0.5, "upper_bin":1, "count":1}');
        tdSql.checkData(7, 0, '{"lower_bin":0, "upper_bin":0.5, "count":0}');
        tdSql.checkData(8, 0, '{"lower_bin":-0.5, "upper_bin":0, "count":0}');
        tdSql.checkData(9, 0, '{"lower_bin":-1, "upper_bin":-0.5, "count":0}');

        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": 1, "width": 0.5, "count": 1.9999, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(1);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":1.5, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": 1, "width": 0.5, "count": 1.9999, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(1);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":1.5, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": 1, "width": 0.5, "count": 1.9999, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(1);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":1.5, "count":0}');

        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": 1, "width": 0.5, "count": 1.99999999999999999, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":1.5, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":1.5, "upper_bin":2, "count":1}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": 1, "width": 0.5, "count": 1.99999999999999999, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":1.5, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":1.5, "upper_bin":2, "count":1}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": 1, "width": 0.5, "count": 1.99999999999999999, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":1.5, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":1.5, "upper_bin":2, "count":1}');

        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 5, "count": 5, "infinity": true}\', 0) from stb;')
        tdSql.checkRows(7);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":0, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":0, "upper_bin":5, "count":5}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":10, "count":5}');
        tdSql.checkData(3, 0, '{"lower_bin":10, "upper_bin":15, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":15, "upper_bin":20, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":20, "upper_bin":25, "count":0}');
        tdSql.checkData(6, 0, '{"lower_bin":25, "upper_bin":inf, "count":1}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 5, "count": 5, "infinity": true}\', 0) from ctb;')
        tdSql.checkRows(7);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":0, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":0, "upper_bin":5, "count":5}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":10, "count":5}');
        tdSql.checkData(3, 0, '{"lower_bin":10, "upper_bin":15, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":15, "upper_bin":20, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":20, "upper_bin":25, "count":0}');
        tdSql.checkData(6, 0, '{"lower_bin":25, "upper_bin":inf, "count":1}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 5, "count": 5, "infinity": true}\', 0) from tb;')
        tdSql.checkRows(7);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":0, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":0, "upper_bin":5, "count":5}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":10, "count":5}');
        tdSql.checkData(3, 0, '{"lower_bin":10, "upper_bin":15, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":15, "upper_bin":20, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":20, "upper_bin":25, "count":0}');
        tdSql.checkData(6, 0, '{"lower_bin":25, "upper_bin":inf, "count":1}');

        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": -1.76e+308, "width": 5, "count": 1, "infinity": true}\', 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":-1.76e+308, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-1.76e+308, "upper_bin":-1.76e+308, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-1.76e+308, "upper_bin":inf, "count":15}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": -1.76e+308, "width": 5, "count": 1, "infinity": true}\', 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":-1.76e+308, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-1.76e+308, "upper_bin":-1.76e+308, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-1.76e+308, "upper_bin":inf, "count":15}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": -1.76e+308, "width": 5, "count": 1, "infinity": true}\', 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":-1.76e+308, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-1.76e+308, "upper_bin":-1.76e+308, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-1.76e+308, "upper_bin":inf, "count":15}');

        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": 10, "width": -5, "count": 3, "infinity": true}\', 0) from stb;')
        tdSql.checkRows(5);
        tdSql.checkData(0, 0, '{"lower_bin":10, "upper_bin":inf, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":5, "upper_bin":10, "count":5}');
        tdSql.checkData(2, 0, '{"lower_bin":0, "upper_bin":5, "count":5}');
        tdSql.checkData(3, 0, '{"lower_bin":-5, "upper_bin":0, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":-inf, "upper_bin":-5, "count":1}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": 10, "width": -5, "count": 3, "infinity": true}\', 0) from ctb;')
        tdSql.checkRows(5);
        tdSql.checkData(0, 0, '{"lower_bin":10, "upper_bin":inf, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":5, "upper_bin":10, "count":5}');
        tdSql.checkData(2, 0, '{"lower_bin":0, "upper_bin":5, "count":5}');
        tdSql.checkData(3, 0, '{"lower_bin":-5, "upper_bin":0, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":-inf, "upper_bin":-5, "count":1}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": 10, "width": -5, "count": 3, "infinity": true}\', 0) from tb;')
        tdSql.checkRows(5);
        tdSql.checkData(0, 0, '{"lower_bin":10, "upper_bin":inf, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":5, "upper_bin":10, "count":5}');
        tdSql.checkData(2, 0, '{"lower_bin":0, "upper_bin":5, "count":5}');
        tdSql.checkData(3, 0, '{"lower_bin":-5, "upper_bin":0, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":-inf, "upper_bin":-5, "count":1}');

        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": -0.7e+308, "width": 0.7e+308, "count": 2, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":-7e+307, "upper_bin":0, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":0, "upper_bin":7e+307, "count":13}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": -0.7e+308, "width": 0.7e+308, "count": 2, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":-7e+307, "upper_bin":0, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":0, "upper_bin":7e+307, "count":13}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": -0.7e+308, "width": 0.7e+308, "count": 2, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":-7e+307, "upper_bin":0, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":0, "upper_bin":7e+307, "count":13}');

        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": -0.7e+308, "width": 0.7e+308, "count": 2, "infinity": true}\', 0) from stb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":-7e+307, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-7e+307, "upper_bin":0, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":0, "upper_bin":7e+307, "count":13}');
        tdSql.checkData(3, 0, '{"lower_bin":7e+307, "upper_bin":inf, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": -0.7e+308, "width": 0.7e+308, "count": 2, "infinity": true}\', 0) from ctb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":-7e+307, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-7e+307, "upper_bin":0, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":0, "upper_bin":7e+307, "count":13}');
        tdSql.checkData(3, 0, '{"lower_bin":7e+307, "upper_bin":inf, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'linear_bin\', \'{"start": -0.7e+308, "width": 0.7e+308, "count": 2, "infinity": true}\', 0) from tb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":-7e+307, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-7e+307, "upper_bin":0, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":0, "upper_bin":7e+307, "count":13}');
        tdSql.checkData(3, 0, '{"lower_bin":7e+307, "upper_bin":inf, "count":0}');

        #FLOATING NUMBER
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": 1, "width": 3, "count": 8, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(8);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":4, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":4, "upper_bin":7, "count":3}');
        tdSql.checkData(2, 0, '{"lower_bin":7, "upper_bin":10, "count":3}');
        tdSql.checkData(3, 0, '{"lower_bin":10, "upper_bin":13, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":13, "upper_bin":16, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":16, "upper_bin":19, "count":0}');
        tdSql.checkData(6, 0, '{"lower_bin":19, "upper_bin":22, "count":1}');
        tdSql.checkData(7, 0, '{"lower_bin":22, "upper_bin":25, "count":0}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": 1, "width": 3, "count": 8, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(8);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":4, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":4, "upper_bin":7, "count":3}');
        tdSql.checkData(2, 0, '{"lower_bin":7, "upper_bin":10, "count":3}');
        tdSql.checkData(3, 0, '{"lower_bin":10, "upper_bin":13, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":13, "upper_bin":16, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":16, "upper_bin":19, "count":0}');
        tdSql.checkData(6, 0, '{"lower_bin":19, "upper_bin":22, "count":1}');
        tdSql.checkData(7, 0, '{"lower_bin":22, "upper_bin":25, "count":0}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": 1, "width": 3, "count": 8, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(8);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":4, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":4, "upper_bin":7, "count":3}');
        tdSql.checkData(2, 0, '{"lower_bin":7, "upper_bin":10, "count":3}');
        tdSql.checkData(3, 0, '{"lower_bin":10, "upper_bin":13, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":13, "upper_bin":16, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":16, "upper_bin":19, "count":0}');
        tdSql.checkData(6, 0, '{"lower_bin":19, "upper_bin":22, "count":1}');
        tdSql.checkData(7, 0, '{"lower_bin":22, "upper_bin":25, "count":0}');

        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": -10.0, "width": 3.0, "count": 8, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(8);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":-7, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":-7, "upper_bin":-4, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-4, "upper_bin":-1, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":-1, "upper_bin":2, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":2, "upper_bin":5, "count":3}');
        tdSql.checkData(5, 0, '{"lower_bin":5, "upper_bin":8, "count":3}');
        tdSql.checkData(6, 0, '{"lower_bin":8, "upper_bin":11, "count":3}');
        tdSql.checkData(7, 0, '{"lower_bin":11, "upper_bin":14, "count":0}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": -10.0, "width": 3.0, "count": 8, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(8);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":-7, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":-7, "upper_bin":-4, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-4, "upper_bin":-1, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":-1, "upper_bin":2, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":2, "upper_bin":5, "count":3}');
        tdSql.checkData(5, 0, '{"lower_bin":5, "upper_bin":8, "count":3}');
        tdSql.checkData(6, 0, '{"lower_bin":8, "upper_bin":11, "count":3}');
        tdSql.checkData(7, 0, '{"lower_bin":11, "upper_bin":14, "count":0}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": -10.0, "width": 3.0, "count": 8, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(8);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":-7, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":-7, "upper_bin":-4, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-4, "upper_bin":-1, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":-1, "upper_bin":2, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":2, "upper_bin":5, "count":3}');
        tdSql.checkData(5, 0, '{"lower_bin":5, "upper_bin":8, "count":3}');
        tdSql.checkData(6, 0, '{"lower_bin":8, "upper_bin":11, "count":3}');
        tdSql.checkData(7, 0, '{"lower_bin":11, "upper_bin":14, "count":0}');

        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": -2.5, "width": 0.5, "count": 8, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(8);
        tdSql.checkData(0, 0, '{"lower_bin":-2.5, "upper_bin":-2, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-2, "upper_bin":-1.5, "count":1}');
        tdSql.checkData(2, 0, '{"lower_bin":-1.5, "upper_bin":-1, "count":0}');
        tdSql.checkData(3, 0, '{"lower_bin":-1, "upper_bin":-0.5, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":-0.5, "upper_bin":0, "count":0}');
        tdSql.checkData(5, 0, '{"lower_bin":0, "upper_bin":0.5, "count":0}');
        tdSql.checkData(6, 0, '{"lower_bin":0.5, "upper_bin":1, "count":0}');
        tdSql.checkData(7, 0, '{"lower_bin":1, "upper_bin":1.5, "count":1}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": -2.5, "width": 0.5, "count": 8, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(8);
        tdSql.checkData(0, 0, '{"lower_bin":-2.5, "upper_bin":-2, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-2, "upper_bin":-1.5, "count":1}');
        tdSql.checkData(2, 0, '{"lower_bin":-1.5, "upper_bin":-1, "count":0}');
        tdSql.checkData(3, 0, '{"lower_bin":-1, "upper_bin":-0.5, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":-0.5, "upper_bin":0, "count":0}');
        tdSql.checkData(5, 0, '{"lower_bin":0, "upper_bin":0.5, "count":0}');
        tdSql.checkData(6, 0, '{"lower_bin":0.5, "upper_bin":1, "count":0}');
        tdSql.checkData(7, 0, '{"lower_bin":1, "upper_bin":1.5, "count":1}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": -2.5, "width": 0.5, "count": 8, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(8);
        tdSql.checkData(0, 0, '{"lower_bin":-2.5, "upper_bin":-2, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-2, "upper_bin":-1.5, "count":1}');
        tdSql.checkData(2, 0, '{"lower_bin":-1.5, "upper_bin":-1, "count":0}');
        tdSql.checkData(3, 0, '{"lower_bin":-1, "upper_bin":-0.5, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":-0.5, "upper_bin":0, "count":0}');
        tdSql.checkData(5, 0, '{"lower_bin":0, "upper_bin":0.5, "count":0}');
        tdSql.checkData(6, 0, '{"lower_bin":0.5, "upper_bin":1, "count":0}');
        tdSql.checkData(7, 0, '{"lower_bin":1, "upper_bin":1.5, "count":1}');

        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": 4, "width": -0.5, "count": 10, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(10);
        tdSql.checkData(0, 0, '{"lower_bin":3.5, "upper_bin":4, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":3.5, "count":1}');
        tdSql.checkData(2, 0, '{"lower_bin":2.5, "upper_bin":3, "count":0}');
        tdSql.checkData(3, 0, '{"lower_bin":2, "upper_bin":2.5, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":1.5, "upper_bin":2, "count":0}');
        tdSql.checkData(5, 0, '{"lower_bin":1, "upper_bin":1.5, "count":1}');
        tdSql.checkData(6, 0, '{"lower_bin":0.5, "upper_bin":1, "count":0}');
        tdSql.checkData(7, 0, '{"lower_bin":0, "upper_bin":0.5, "count":0}');
        tdSql.checkData(8, 0, '{"lower_bin":-0.5, "upper_bin":0, "count":0}');
        tdSql.checkData(9, 0, '{"lower_bin":-1, "upper_bin":-0.5, "count":0}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": 4, "width": -0.5, "count": 10, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(10);
        tdSql.checkData(0, 0, '{"lower_bin":3.5, "upper_bin":4, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":3.5, "count":1}');
        tdSql.checkData(2, 0, '{"lower_bin":2.5, "upper_bin":3, "count":0}');
        tdSql.checkData(3, 0, '{"lower_bin":2, "upper_bin":2.5, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":1.5, "upper_bin":2, "count":0}');
        tdSql.checkData(5, 0, '{"lower_bin":1, "upper_bin":1.5, "count":1}');
        tdSql.checkData(6, 0, '{"lower_bin":0.5, "upper_bin":1, "count":0}');
        tdSql.checkData(7, 0, '{"lower_bin":0, "upper_bin":0.5, "count":0}');
        tdSql.checkData(8, 0, '{"lower_bin":-0.5, "upper_bin":0, "count":0}');
        tdSql.checkData(9, 0, '{"lower_bin":-1, "upper_bin":-0.5, "count":0}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": 4, "width": -0.5, "count": 10, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(10);
        tdSql.checkData(0, 0, '{"lower_bin":3.5, "upper_bin":4, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":3.5, "count":1}');
        tdSql.checkData(2, 0, '{"lower_bin":2.5, "upper_bin":3, "count":0}');
        tdSql.checkData(3, 0, '{"lower_bin":2, "upper_bin":2.5, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":1.5, "upper_bin":2, "count":0}');
        tdSql.checkData(5, 0, '{"lower_bin":1, "upper_bin":1.5, "count":1}');
        tdSql.checkData(6, 0, '{"lower_bin":0.5, "upper_bin":1, "count":0}');
        tdSql.checkData(7, 0, '{"lower_bin":0, "upper_bin":0.5, "count":0}');
        tdSql.checkData(8, 0, '{"lower_bin":-0.5, "upper_bin":0, "count":0}');
        tdSql.checkData(9, 0, '{"lower_bin":-1, "upper_bin":-0.5, "count":0}');

        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": 1, "width": 0.5, "count": 1.9999, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(1);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":1.5, "count":1}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": 1, "width": 0.5, "count": 1.9999, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(1);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":1.5, "count":1}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": 1, "width": 0.5, "count": 1.9999, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(1);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":1.5, "count":1}');

        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": 1, "width": 0.5, "count": 1.99999999999999999, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":1.5, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":1.5, "upper_bin":2, "count":0}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": 1, "width": 0.5, "count": 1.99999999999999999, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":1.5, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":1.5, "upper_bin":2, "count":0}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": 1, "width": 0.5, "count": 1.99999999999999999, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":1.5, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":1.5, "upper_bin":2, "count":0}');

        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": 0, "width": 5, "count": 5, "infinity": true}\', 0) from stb;')
        tdSql.checkRows(7);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":0, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":0, "upper_bin":5, "count":4}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":10, "count":5}');
        tdSql.checkData(3, 0, '{"lower_bin":10, "upper_bin":15, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":15, "upper_bin":20, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":20, "upper_bin":25, "count":1}');
        tdSql.checkData(6, 0, '{"lower_bin":25, "upper_bin":inf, "count":1}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": 0, "width": 5, "count": 5, "infinity": true}\', 0) from ctb;')
        tdSql.checkRows(7);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":0, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":0, "upper_bin":5, "count":4}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":10, "count":5}');
        tdSql.checkData(3, 0, '{"lower_bin":10, "upper_bin":15, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":15, "upper_bin":20, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":20, "upper_bin":25, "count":1}');
        tdSql.checkData(6, 0, '{"lower_bin":25, "upper_bin":inf, "count":1}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": 0, "width": 5, "count": 5, "infinity": true}\', 0) from tb;')
        tdSql.checkRows(7);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":0, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":0, "upper_bin":5, "count":4}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":10, "count":5}');
        tdSql.checkData(3, 0, '{"lower_bin":10, "upper_bin":15, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":15, "upper_bin":20, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":20, "upper_bin":25, "count":1}');
        tdSql.checkData(6, 0, '{"lower_bin":25, "upper_bin":inf, "count":1}');

        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": 10, "width": -5, "count": 3, "infinity": true}\', 0) from stb;')
        tdSql.checkRows(5);
        tdSql.checkData(0, 0, '{"lower_bin":10, "upper_bin":inf, "count":4}');
        tdSql.checkData(1, 0, '{"lower_bin":5, "upper_bin":10, "count":5}');
        tdSql.checkData(2, 0, '{"lower_bin":0, "upper_bin":5, "count":4}');
        tdSql.checkData(3, 0, '{"lower_bin":-5, "upper_bin":0, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":-inf, "upper_bin":-5, "count":1}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": 10, "width": -5, "count": 3, "infinity": true}\', 0) from ctb;')
        tdSql.checkRows(5);
        tdSql.checkData(0, 0, '{"lower_bin":10, "upper_bin":inf, "count":4}');
        tdSql.checkData(1, 0, '{"lower_bin":5, "upper_bin":10, "count":5}');
        tdSql.checkData(2, 0, '{"lower_bin":0, "upper_bin":5, "count":4}');
        tdSql.checkData(3, 0, '{"lower_bin":-5, "upper_bin":0, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":-inf, "upper_bin":-5, "count":1}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": 10, "width": -5, "count": 3, "infinity": true}\', 0) from tb;')
        tdSql.checkRows(5);
        tdSql.checkData(0, 0, '{"lower_bin":10, "upper_bin":inf, "count":4}');
        tdSql.checkData(1, 0, '{"lower_bin":5, "upper_bin":10, "count":5}');
        tdSql.checkData(2, 0, '{"lower_bin":0, "upper_bin":5, "count":4}');
        tdSql.checkData(3, 0, '{"lower_bin":-5, "upper_bin":0, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":-inf, "upper_bin":-5, "count":1}');

        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": -1.76e+308, "width": 5, "count": 1, "infinity": true}\', 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":-1.76e+308, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-1.76e+308, "upper_bin":-1.76e+308, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-1.76e+308, "upper_bin":inf, "count":15}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": -1.76e+308, "width": 5, "count": 1, "infinity": true}\', 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":-1.76e+308, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-1.76e+308, "upper_bin":-1.76e+308, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-1.76e+308, "upper_bin":inf, "count":15}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": -1.76e+308, "width": 5, "count": 1, "infinity": true}\', 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":-1.76e+308, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-1.76e+308, "upper_bin":-1.76e+308, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-1.76e+308, "upper_bin":inf, "count":15}');

        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": -0.7e+308, "width": 0.7e+308, "count": 2, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":-7e+307, "upper_bin":0, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":0, "upper_bin":7e+307, "count":13}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": -0.7e+308, "width": 0.7e+308, "count": 2, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":-7e+307, "upper_bin":0, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":0, "upper_bin":7e+307, "count":13}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": -0.7e+308, "width": 0.7e+308, "count": 2, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":-7e+307, "upper_bin":0, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":0, "upper_bin":7e+307, "count":13}');

        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": -0.7e+308, "width": 0.7e+308, "count": 2, "infinity": true}\', 0) from stb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":-7e+307, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-7e+307, "upper_bin":0, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":0, "upper_bin":7e+307, "count":13}');
        tdSql.checkData(3, 0, '{"lower_bin":7e+307, "upper_bin":inf, "count":0}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": -0.7e+308, "width": 0.7e+308, "count": 2, "infinity": true}\', 0) from ctb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":-7e+307, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-7e+307, "upper_bin":0, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":0, "upper_bin":7e+307, "count":13}');
        tdSql.checkData(3, 0, '{"lower_bin":7e+307, "upper_bin":inf, "count":0}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"start": -0.7e+308, "width": 0.7e+308, "count": 2, "infinity": true}\', 0) from tb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":-7e+307, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-7e+307, "upper_bin":0, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":0, "upper_bin":7e+307, "count":13}');
        tdSql.checkData(3, 0, '{"lower_bin":7e+307, "upper_bin":inf, "count":0}');

        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"width":2, "start": 0, "count": 4, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":6, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":6, "upper_bin":8, "count":2}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"width":2, "start": 0, "count": 4, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":6, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":6, "upper_bin":8, "count":2}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"width":2, "start": 0, "count": 4, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":6, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":6, "upper_bin":8, "count":2}');

        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"width":2, "start": 0, "count": 4, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":6, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":6, "upper_bin":8, "count":2}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"width":2, "start": 0, "count": 4, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":6, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":6, "upper_bin":8, "count":2}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"width":2, "start": 0, "count": 4, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":6, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":6, "upper_bin":8, "count":2}');

        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"count": 4, "width":2, "start": 0, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":6, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":6, "upper_bin":8, "count":2}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"count": 4, "width":2, "start": 0, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":6, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":6, "upper_bin":8, "count":2}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"count": 4, "width":2, "start": 0, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":6, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":6, "upper_bin":8, "count":2}');

        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"infinity": false, "width":2, "start": 0, "count": 4}\', 0) from stb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":6, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":6, "upper_bin":8, "count":2}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"infinity": false, "width":2, "start": 0, "count": 4}\', 0) from ctb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":6, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":6, "upper_bin":8, "count":2}');
        tdSql.query('select histogram(col_float, \'linear_bin\', \'{"infinity": false, "width":2, "start": 0, "count": 4}\', 0) from tb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":6, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":6, "upper_bin":8, "count":2}');

        #ERROR CASE
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": true, "width": 5, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": true, "width": 5, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": true, "width": 5, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": false, "width": 5, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": false, "width": 5, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": false, "width": 5, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": "abc", "width": 5, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": "abc", "width": 5, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": "abc", "width": 5, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": "中文", "width": 5, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": "中文", "width": 5, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": "中文", "width": 5, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": abc, "width": 5, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": abc, "width": 5, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": abc, "width": 5, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": -1.80e+308, "width": 5, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": -1.80e+308, "width": 5, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": -1.80e+308, "width": 5, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 1.80e+308, "width": 5, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 1.80e+308, "width": 5, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 1.80e+308, "width": 5, "count": 5, "infinity": false}\', 0) from tb;')

        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": true, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": true, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": true, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": false, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": false, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": false, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": "abc", "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": "abc", "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": "abc", "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": "中文", "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": "中文", "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": "中文", "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": abc, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": abc, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": abc, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 0, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 0, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 0, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": -1.80e+308, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": -1.80e+308, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": -1.80e+308, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1.80e+308, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1.80e+308, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1.80e+308, "count": 5, "infinity": false}\', 0) from tb;')

        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": -1.4e+308, "width": 1.4e+308, "count": 3, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": -1.4e+308, "width": 1.4e+308, "count": 3, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": -1.4e+308, "width": 1.4e+308, "count": 3, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": -1.4e+308, "width": 1.4e+308, "count": 3, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": -1.4e+308, "width": 1.4e+308, "count": 3, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": -1.4e+308, "width": 1.4e+308, "count": 3, "infinity": true}\', 0) from tb;')

        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": -1, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": -1, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": -1, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 0, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 0, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 0, "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1001, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1001, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1001, "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": true, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": true, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": true, "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": false, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": false, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": false, "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": "abc", "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": "abc", "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": "abc", "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": "中文", "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": "中文", "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": "中文", "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": abc, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": abc, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": abc, "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1.8e+308, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1.8e+308, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1.8e+308, "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": -1.8e+308, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": -1.8e+308, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": -1.8e+308, "infinity": true}\', 0) from tb;')

        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": 1}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": 1}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": 1}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": 0}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": 0}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": 0}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": -1.5}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": -1.5}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": -1.5}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": 1.8e+308}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": 1.8e+308}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": 1.8e+308}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": "abc"}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": "abc"}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": "abc"}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": "中文"}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": "中文"}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": "中文"}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": abc}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": abc}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": abc}\', 0) from tb;')

        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"begin": 0, "width": 1, "count": 1, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"begin": 0, "width": 1, "count": 1, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"begin": 0, "width": 1, "count": 1, "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "factor": 1, "cnt": 1, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "factor": 1, "cnt": 1, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "factor": 1, "cnt": 1, "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "inf": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "inf": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{"start": 0, "width": 1, "count": 1, "inf": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{start: 0, width: 1, count: 1, infinity: true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{start: 0, width: 1, count: 1, infinity: true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'{start: 0, width: 1, count: 1, infinity: true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'[ 0, 1, 1, true]\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'[ 0, 1, 1, true]\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'linear_bin\', \'[ 0, 1, 1, true]\', 0) from tb;')

        ## log_bin ##
        #INTEGER
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": 3, "count": 6, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(6);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":9, "count":6}');
        tdSql.checkData(2, 0, '{"lower_bin":9, "upper_bin":27, "count":3}');
        tdSql.checkData(3, 0, '{"lower_bin":27, "upper_bin":81, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":81, "upper_bin":243, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":243, "upper_bin":729, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": 3, "count": 6, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(6);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":9, "count":6}');
        tdSql.checkData(2, 0, '{"lower_bin":9, "upper_bin":27, "count":3}');
        tdSql.checkData(3, 0, '{"lower_bin":27, "upper_bin":81, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":81, "upper_bin":243, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":243, "upper_bin":729, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": 3, "count": 6, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(6);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":9, "count":6}');
        tdSql.checkData(2, 0, '{"lower_bin":9, "upper_bin":27, "count":3}');
        tdSql.checkData(3, 0, '{"lower_bin":27, "upper_bin":81, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":81, "upper_bin":243, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":243, "upper_bin":729, "count":0}');

        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": -1.0, "factor": 3.0, "count": 6, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(6);
        tdSql.checkData(0, 0, '{"lower_bin":-3, "upper_bin":-1, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":-9, "upper_bin":-3, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-27, "upper_bin":-9, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":-81, "upper_bin":-27, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":-243, "upper_bin":-81, "count":0}');
        tdSql.checkData(5, 0, '{"lower_bin":-729, "upper_bin":-243, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": -1.0, "factor": 3.0, "count": 6, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(6);
        tdSql.checkData(0, 0, '{"lower_bin":-3, "upper_bin":-1, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":-9, "upper_bin":-3, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-27, "upper_bin":-9, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":-81, "upper_bin":-27, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":-243, "upper_bin":-81, "count":0}');
        tdSql.checkData(5, 0, '{"lower_bin":-729, "upper_bin":-243, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": -1.0, "factor": 3.0, "count": 6, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(6);
        tdSql.checkData(0, 0, '{"lower_bin":-3, "upper_bin":-1, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":-9, "upper_bin":-3, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-27, "upper_bin":-9, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":-81, "upper_bin":-27, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":-243, "upper_bin":-81, "count":0}');
        tdSql.checkData(5, 0, '{"lower_bin":-729, "upper_bin":-243, "count":0}');

        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 10, "factor": 0.5, "count": 6, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(6);
        tdSql.checkData(0, 0, '{"lower_bin":5, "upper_bin":10, "count":5}');
        tdSql.checkData(1, 0, '{"lower_bin":2.5, "upper_bin":5, "count":3}');
        tdSql.checkData(2, 0, '{"lower_bin":1.25, "upper_bin":2.5, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":0.625, "upper_bin":1.25, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":0.3125, "upper_bin":0.625, "count":0}');
        tdSql.checkData(5, 0, '{"lower_bin":0.15625, "upper_bin":0.3125, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 10, "factor": 0.5, "count": 6, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(6);
        tdSql.checkData(0, 0, '{"lower_bin":5, "upper_bin":10, "count":5}');
        tdSql.checkData(1, 0, '{"lower_bin":2.5, "upper_bin":5, "count":3}');
        tdSql.checkData(2, 0, '{"lower_bin":1.25, "upper_bin":2.5, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":0.625, "upper_bin":1.25, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":0.3125, "upper_bin":0.625, "count":0}');
        tdSql.checkData(5, 0, '{"lower_bin":0.15625, "upper_bin":0.3125, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 10, "factor": 0.5, "count": 6, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(6);
        tdSql.checkData(0, 0, '{"lower_bin":5, "upper_bin":10, "count":5}');
        tdSql.checkData(1, 0, '{"lower_bin":2.5, "upper_bin":5, "count":3}');
        tdSql.checkData(2, 0, '{"lower_bin":1.25, "upper_bin":2.5, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":0.625, "upper_bin":1.25, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":0.3125, "upper_bin":0.625, "count":0}');
        tdSql.checkData(5, 0, '{"lower_bin":0.15625, "upper_bin":0.3125, "count":0}');

        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": -10, "factor": 0.5, "count": 6, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(6);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":-5, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":-5, "upper_bin":-2.5, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-2.5, "upper_bin":-1.25, "count":0}');
        tdSql.checkData(3, 0, '{"lower_bin":-1.25, "upper_bin":-0.625, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":-0.625, "upper_bin":-0.3125, "count":0}');
        tdSql.checkData(5, 0, '{"lower_bin":-0.3125, "upper_bin":-0.15625, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": -10, "factor": 0.5, "count": 6, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(6);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":-5, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":-5, "upper_bin":-2.5, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-2.5, "upper_bin":-1.25, "count":0}');
        tdSql.checkData(3, 0, '{"lower_bin":-1.25, "upper_bin":-0.625, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":-0.625, "upper_bin":-0.3125, "count":0}');
        tdSql.checkData(5, 0, '{"lower_bin":-0.3125, "upper_bin":-0.15625, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": -10, "factor": 0.5, "count": 6, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(6);
        tdSql.checkData(0, 0, '{"lower_bin":-10, "upper_bin":-5, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":-5, "upper_bin":-2.5, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-2.5, "upper_bin":-1.25, "count":0}');
        tdSql.checkData(3, 0, '{"lower_bin":-1.25, "upper_bin":-0.625, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":-0.625, "upper_bin":-0.3125, "count":0}');
        tdSql.checkData(5, 0, '{"lower_bin":-0.3125, "upper_bin":-0.15625, "count":0}');

        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 2, "factor": 1.5, "count": 6, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(6);
        tdSql.checkData(0, 0, '{"lower_bin":2, "upper_bin":3, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":4.5, "count":1}');
        tdSql.checkData(2, 0, '{"lower_bin":4.5, "upper_bin":6.75, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":6.75, "upper_bin":10.125, "count":4}');
        tdSql.checkData(4, 0, '{"lower_bin":10.125, "upper_bin":15.1875, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":15.1875, "upper_bin":22.7812, "count":1}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 2, "factor": 1.5, "count": 6, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(6);
        tdSql.checkData(0, 0, '{"lower_bin":2, "upper_bin":3, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":4.5, "count":1}');
        tdSql.checkData(2, 0, '{"lower_bin":4.5, "upper_bin":6.75, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":6.75, "upper_bin":10.125, "count":4}');
        tdSql.checkData(4, 0, '{"lower_bin":10.125, "upper_bin":15.1875, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":15.1875, "upper_bin":22.7812, "count":1}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 2, "factor": 1.5, "count": 6, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(6);
        tdSql.checkData(0, 0, '{"lower_bin":2, "upper_bin":3, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":4.5, "count":1}');
        tdSql.checkData(2, 0, '{"lower_bin":4.5, "upper_bin":6.75, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":6.75, "upper_bin":10.125, "count":4}');
        tdSql.checkData(4, 0, '{"lower_bin":10.125, "upper_bin":15.1875, "count":1}');
        tdSql.checkData(5, 0, '{"lower_bin":15.1875, "upper_bin":22.7812, "count":1}');

        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 3.2, "factor": 0.5, "count": 1.9999, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(1);
        tdSql.checkData(0, 0, '{"lower_bin":1.6, "upper_bin":3.2, "count":2}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 3.2, "factor": 0.5, "count": 1.9999, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(1);
        tdSql.checkData(0, 0, '{"lower_bin":1.6, "upper_bin":3.2, "count":2}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 3.2, "factor": 0.5, "count": 1.9999, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(1);
        tdSql.checkData(0, 0, '{"lower_bin":1.6, "upper_bin":3.2, "count":2}');

        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 3.2, "factor": 0.5, "count": 1.99999999999999999, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1.6, "upper_bin":3.2, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":0.8, "upper_bin":1.6, "count":1}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 3.2, "factor": 0.5, "count": 1.99999999999999999, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1.6, "upper_bin":3.2, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":0.8, "upper_bin":1.6, "count":1}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 3.2, "factor": 0.5, "count": 1.99999999999999999, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(2);
        tdSql.checkData(0, 0, '{"lower_bin":1.6, "upper_bin":3.2, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":0.8, "upper_bin":1.6, "count":1}');

        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": 5, "count": 3, "infinity": true}\', 0) from stb;')
        tdSql.checkRows(5);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":1, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":1, "upper_bin":5, "count":4}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":25, "count":7}');
        tdSql.checkData(3, 0, '{"lower_bin":25, "upper_bin":125, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":125, "upper_bin":inf, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": 5, "count": 3, "infinity": true}\', 0) from ctb;')
        tdSql.checkRows(5);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":1, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":1, "upper_bin":5, "count":4}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":25, "count":7}');
        tdSql.checkData(3, 0, '{"lower_bin":25, "upper_bin":125, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":125, "upper_bin":inf, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": 5, "count": 3, "infinity": true}\', 0) from tb;')
        tdSql.checkRows(5);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":1, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":1, "upper_bin":5, "count":4}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":25, "count":7}');
        tdSql.checkData(3, 0, '{"lower_bin":25, "upper_bin":125, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":125, "upper_bin":inf, "count":0}');

        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 0.2e+308, "factor": 3.14, "count": 1, "infinity": true}\', 0) from stb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":2e+307, "count":15}');
        tdSql.checkData(1, 0, '{"lower_bin":2e+307, "upper_bin":6.28e+307, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":6.28e+307, "upper_bin":inf, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 0.2e+308, "factor": 3.14, "count": 1, "infinity": true}\', 0) from ctb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":2e+307, "count":15}');
        tdSql.checkData(1, 0, '{"lower_bin":2e+307, "upper_bin":6.28e+307, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":6.28e+307, "upper_bin":inf, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 0.2e+308, "factor": 3.14, "count": 1, "infinity": true}\', 0) from tb;')
        tdSql.checkRows(3);
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":2e+307, "count":15}');
        tdSql.checkData(1, 0, '{"lower_bin":2e+307, "upper_bin":6.28e+307, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":6.28e+307, "upper_bin":inf, "count":0}');

        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": -2, "factor": 3, "count": 3, "infinity": true}\', 0) from stb;')
        tdSql.checkRows(5);
        tdSql.checkData(0, 0, '{"lower_bin":-2, "upper_bin":inf, "count":14}');
        tdSql.checkData(1, 0, '{"lower_bin":-6, "upper_bin":-2, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-18, "upper_bin":-6, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":-54, "upper_bin":-18, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":-inf, "upper_bin":-54, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": -2, "factor": 3, "count": 3, "infinity": true}\', 0) from ctb;')
        tdSql.checkRows(5);
        tdSql.checkData(0, 0, '{"lower_bin":-2, "upper_bin":inf, "count":14}');
        tdSql.checkData(1, 0, '{"lower_bin":-6, "upper_bin":-2, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-18, "upper_bin":-6, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":-54, "upper_bin":-18, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":-inf, "upper_bin":-54, "count":0}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": -2, "factor": 3, "count": 3, "infinity": true}\', 0) from tb;')
        tdSql.checkRows(5);
        tdSql.checkData(0, 0, '{"lower_bin":-2, "upper_bin":inf, "count":14}');
        tdSql.checkData(1, 0, '{"lower_bin":-6, "upper_bin":-2, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-18, "upper_bin":-6, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":-54, "upper_bin":-18, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":-inf, "upper_bin":-54, "count":0}');

        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 10, "factor": 0.5, "count": 3, "infinity": true}\', 0) from stb;')
        tdSql.checkRows(5);
        tdSql.checkData(0, 0, '{"lower_bin":10, "upper_bin":inf, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":5, "upper_bin":10, "count":5}');
        tdSql.checkData(2, 0, '{"lower_bin":2.5, "upper_bin":5, "count":3}');
        tdSql.checkData(3, 0, '{"lower_bin":1.25, "upper_bin":2.5, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":-inf, "upper_bin":1.25, "count":3}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 10, "factor": 0.5, "count": 3, "infinity": true}\', 0) from ctb;')
        tdSql.checkRows(5);
        tdSql.checkData(0, 0, '{"lower_bin":10, "upper_bin":inf, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":5, "upper_bin":10, "count":5}');
        tdSql.checkData(2, 0, '{"lower_bin":2.5, "upper_bin":5, "count":3}');
        tdSql.checkData(3, 0, '{"lower_bin":1.25, "upper_bin":2.5, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":-inf, "upper_bin":1.25, "count":3}');
        tdSql.query('select histogram(col_tinyint, \'log_bin\', \'{"start": 10, "factor": 0.5, "count": 3, "infinity": true}\', 0) from tb;')
        tdSql.checkRows(5);
        tdSql.checkData(0, 0, '{"lower_bin":10, "upper_bin":inf, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":5, "upper_bin":10, "count":5}');
        tdSql.checkData(2, 0, '{"lower_bin":2.5, "upper_bin":5, "count":3}');
        tdSql.checkData(3, 0, '{"lower_bin":1.25, "upper_bin":2.5, "count":1}');
        tdSql.checkData(4, 0, '{"lower_bin":-inf, "upper_bin":1.25, "count":3}');

        #FLOAT
        tdSql.query('select histogram(col_float, \'log_bin\', \'{"factor":2, "start": 1, "count": 4, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":8, "count":4}');
        tdSql.checkData(3, 0, '{"lower_bin":8, "upper_bin":16, "count":4}');
        tdSql.query('select histogram(col_float, \'log_bin\', \'{"factor":2, "start": 1, "count": 4, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":8, "count":4}');
        tdSql.checkData(3, 0, '{"lower_bin":8, "upper_bin":16, "count":4}');
        tdSql.query('select histogram(col_float, \'log_bin\', \'{"factor":2, "start": 1, "count": 4, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":8, "count":4}');
        tdSql.checkData(3, 0, '{"lower_bin":8, "upper_bin":16, "count":4}');

        tdSql.query('select histogram(col_float, \'log_bin\', \'{"count": 4, "factor":2, "start": 1, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":8, "count":4}');
        tdSql.checkData(3, 0, '{"lower_bin":8, "upper_bin":16, "count":4}');
        tdSql.query('select histogram(col_float, \'log_bin\', \'{"count": 4, "factor":2, "start": 1, "infinity": false}\', 0) from ctb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":8, "count":4}');
        tdSql.checkData(3, 0, '{"lower_bin":8, "upper_bin":16, "count":4}');
        tdSql.query('select histogram(col_float, \'log_bin\', \'{"count": 4, "factor":2, "start": 1, "infinity": false}\', 0) from tb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":8, "count":4}');
        tdSql.checkData(3, 0, '{"lower_bin":8, "upper_bin":16, "count":4}');

        tdSql.query('select histogram(col_float, \'log_bin\', \'{"infinity": false, "count": 4, "factor":2, "start": 1}\', 0) from stb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":8, "count":4}');
        tdSql.checkData(3, 0, '{"lower_bin":8, "upper_bin":16, "count":4}');
        tdSql.query('select histogram(col_float, \'log_bin\', \'{"infinity": false, "count": 4, "factor":2, "start": 1}\', 0) from ctb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":8, "count":4}');
        tdSql.checkData(3, 0, '{"lower_bin":8, "upper_bin":16, "count":4}');
        tdSql.query('select histogram(col_float, \'log_bin\', \'{"infinity": false, "count": 4, "factor":2, "start": 1}\', 0) from tb;')
        tdSql.checkRows(4);
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":4, "upper_bin":8, "count":4}');
        tdSql.checkData(3, 0, '{"lower_bin":8, "upper_bin":16, "count":4}');

        #ERROR CASE
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": true, "factor": 5, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": true, "factor": 5, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": true, "factor": 5, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": false, "factor": 5, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": false, "factor": 5, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": false, "factor": 5, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": "abc", "factor": 5, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": "abc", "factor": 5, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": "abc", "factor": 5, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": "中文", "factor": 5, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": "中文", "factor": 5, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": "中文", "factor": 5, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": abc, "factor": 5, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": abc, "factor": 5, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": abc, "factor": 5, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": -1.80e+308, "factor": 5, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": -1.80e+308, "factor": 5, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": -1.80e+308, "factor": 5, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1.80e+308, "factor": 5, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1.80e+308, "factor": 5, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1.80e+308, "factor": 5, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 5, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 5, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 5, "count": 5, "infinity": false}\', 0) from tb;')

        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": true, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": true, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": true, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": false, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": false, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": false, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": "abc", "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": "abc", "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": "abc", "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": "中文", "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": "中文", "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": "中文", "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": abc, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": abc, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": abc, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": 1.80e+308, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": 1.80e+308, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": 1.80e+308, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": 0, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": 0, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": 0, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": -5, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": -5, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": -5, "count": 5, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": 1, "count": 5, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": 1, "count": 5, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 1, "factor": 1, "count": 5, "infinity": false}\', 0) from tb;')

        #out of range
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": -1.4e+308, "factor": 1.5, "count": 3, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": -1.4e+308, "factor": 1.5, "count": 3, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": -1.4e+308, "factor": 1.5, "count": 3, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": -1.4e+308, "factor": 1.5, "count": 3, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": -1.4e+308, "factor": 1.5, "count": 3, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": -1.4e+308, "factor": 1.5, "count": 3, "infinity": true}\', 0) from tb;')

        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": -1, "infinity": false}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": -1, "infinity": false}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": -1, "infinity": false}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 0, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 0, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 0, "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1001, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1001, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1001, "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": true, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": true, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": true, "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": false, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": false, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": false, "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": "abc", "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": "abc", "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": "abc", "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": "中文", "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": "中文", "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": "中文", "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": abc, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": abc, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": abc, "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1.8e+308, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1.8e+308, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1.8e+308, "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": -1.8e+308, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": -1.8e+308, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": -1.8e+308, "infinity": true}\', 0) from tb;')

        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": 1}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": 1}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": 1}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": 0}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": 0}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": 0}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": -1.5}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": -1.5}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": -1.5}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": 1.8e+308}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": 1.8e+308}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": 1.8e+308}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": "abc"}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": "abc"}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": "abc"}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": "中文"}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": "中文"}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": "中文"}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": abc}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": abc}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "infinity": abc}\', 0) from tb;')

        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"begin": 0, "factor": 1, "count": 1, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"begin": 0, "factor": 1, "count": 1, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"begin": 0, "factor": 1, "count": 1, "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "width": 1, "count": 1, "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "cnt": 1, "infinity": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "cnt": 1, "infinity": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "cnt": 1, "infinity": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "inf": true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "inf": true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{"start": 0, "factor": 1, "count": 1, "inf": true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{start: 0, factor: 1, count: 1, infinity: true}\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{start: 0, factor: 1, count: 1, infinity: true}\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'{start: 0, factor: 1, count: 1, infinity: true}\', 0) from tb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'[ 0, 1, 1, true]\', 0) from stb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'[ 0, 1, 1, true]\', 0) from ctb;')
        tdSql.error('select histogram(col_tinyint, \'log_bin\', \'[ 0, 1, 1, true]\', 0) from tb;')

        print("============== STEP 3: normalization  ================== ")
        ## Normalization ##
        tdSql.query('select histogram(col_smallint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.query('select histogram(col_smallint, "user_input", "[1,3,5,7]", 1) from ctb;')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":0.333333}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":0.333333}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":0.333333}');
        tdSql.query('select histogram(col_smallint, "user_input", "[1,3,5,7]", 1) from tb;')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":0.333333}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":0.333333}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":0.333333}');

        tdSql.query('select histogram(col_int, "user_input", "[1,5,10]", 0) from stb;')
        tdSql.checkRows(2)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":5, "count":4}');
        tdSql.checkData(1, 0, '{"lower_bin":5, "upper_bin":10, "count":5}');
        tdSql.query('select histogram(col_int, "user_input", "[1,5,10]", 1) from ctb;')
        tdSql.checkRows(2)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":5, "count":0.444444}');
        tdSql.checkData(1, 0, '{"lower_bin":5, "upper_bin":10, "count":0.555556}');
        tdSql.query('select histogram(col_int, "user_input", "[1,5,10]", 1) from tb;')
        tdSql.checkRows(2)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":5, "count":0.444444}');
        tdSql.checkData(1, 0, '{"lower_bin":5, "upper_bin":10, "count":0.555556}');

        tdSql.query('select histogram(col_double, "user_input", "[0,5,11]", 0) from stb;')
        tdSql.checkRows(2)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":5, "count":4}');
        tdSql.checkData(1, 0, '{"lower_bin":5, "upper_bin":11, "count":6}');
        tdSql.query('select histogram(col_double, "user_input", "[0,5,11]", 1) from ctb;')
        tdSql.checkRows(2)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":5, "count":0.400000}');
        tdSql.checkData(1, 0, '{"lower_bin":5, "upper_bin":11, "count":0.600000}');
        tdSql.query('select histogram(col_double, "user_input", "[0,5,11]", 1) from tb;')
        tdSql.checkRows(2)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":5, "count":0.400000}');
        tdSql.checkData(1, 0, '{"lower_bin":5, "upper_bin":11, "count":0.600000}');

        tdSql.query('select histogram(col_bigint, \'linear_bin\', \'{"start": 1, "width": 5, "count": 2, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(2)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":6, "count":5}');
        tdSql.checkData(1, 0, '{"lower_bin":6, "upper_bin":11, "count":4}');
        tdSql.query('select histogram(col_bigint, \'linear_bin\', \'{"start": 1, "width": 5, "count": 2, "infinity": false}\', 1) from ctb;')
        tdSql.checkRows(2)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":6, "count":0.555556}');
        tdSql.checkData(1, 0, '{"lower_bin":6, "upper_bin":11, "count":0.444444}');
        tdSql.query('select histogram(col_bigint, \'linear_bin\', \'{"start": 1, "width": 5, "count": 2, "infinity": false}\', 1) from tb;')
        tdSql.checkRows(2)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":6, "count":0.555556}');
        tdSql.checkData(1, 0, '{"lower_bin":6, "upper_bin":11, "count":0.444444}');

        tdSql.query('select histogram(col_int, \'linear_bin\', \'{"start": -10, "width": 5, "count": 3, "infinity": true}\', 0) from stb;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":-10, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-10, "upper_bin":-5, "count":1}');
        tdSql.checkData(2, 0, '{"lower_bin":-5, "upper_bin":0, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":0, "upper_bin":5, "count":5}');
        tdSql.checkData(4, 0, '{"lower_bin":5, "upper_bin":inf, "count":8}');
        tdSql.query('select histogram(col_int, \'linear_bin\', \'{"start": -10, "width": 5, "count": 3, "infinity": true}\', 1) from ctb;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":-10, "count":0.000000}');
        tdSql.checkData(1, 0, '{"lower_bin":-10, "upper_bin":-5, "count":0.066667}');
        tdSql.checkData(2, 0, '{"lower_bin":-5, "upper_bin":0, "count":0.066667}');
        tdSql.checkData(3, 0, '{"lower_bin":0, "upper_bin":5, "count":0.333333}');
        tdSql.checkData(4, 0, '{"lower_bin":5, "upper_bin":inf, "count":0.533333}');
        tdSql.query('select histogram(col_int, \'linear_bin\', \'{"start": -10, "width": 5, "count": 3, "infinity": true}\', 1) from tb;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":-10, "count":0.000000}');
        tdSql.checkData(1, 0, '{"lower_bin":-10, "upper_bin":-5, "count":0.066667}');
        tdSql.checkData(2, 0, '{"lower_bin":-5, "upper_bin":0, "count":0.066667}');
        tdSql.checkData(3, 0, '{"lower_bin":0, "upper_bin":5, "count":0.333333}');
        tdSql.checkData(4, 0, '{"lower_bin":5, "upper_bin":inf, "count":0.533333}');

        tdSql.query('select histogram(col_float, \'log_bin\', \'{"start": 1, "factor": 5, "count": 3, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":5, "count":4}');
        tdSql.checkData(1, 0, '{"lower_bin":5, "upper_bin":25, "count":8}');
        tdSql.checkData(2, 0, '{"lower_bin":25, "upper_bin":125, "count":1}');
        tdSql.query('select histogram(col_float, \'log_bin\', \'{"start": 1, "factor": 5, "count": 3, "infinity": false}\', 1) from ctb;')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":5, "count":0.307692}');
        tdSql.checkData(1, 0, '{"lower_bin":5, "upper_bin":25, "count":0.615385}');
        tdSql.checkData(2, 0, '{"lower_bin":25, "upper_bin":125, "count":0.076923}');
        tdSql.query('select histogram(col_float, \'log_bin\', \'{"start": 1, "factor": 5, "count": 3, "infinity": false}\', 1) from tb;')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":5, "count":0.307692}');
        tdSql.checkData(1, 0, '{"lower_bin":5, "upper_bin":25, "count":0.615385}');
        tdSql.checkData(2, 0, '{"lower_bin":25, "upper_bin":125, "count":0.076923}');

        tdSql.query('select histogram(col_double, \'log_bin\', \'{"start": -0.5, "factor": 0.5, "count": 2, "infinity": false}\', 0) from stb;')
        tdSql.checkRows(2)
        tdSql.checkData(0, 0, '{"lower_bin":-0.5, "upper_bin":-0.25, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":-0.25, "upper_bin":-0.125, "count":0}');
        tdSql.query('select histogram(col_double, \'log_bin\', \'{"start": -0.5, "factor": 0.5, "count": 2, "infinity": false}\', 1) from ctb;')
        tdSql.checkRows(2)
        tdSql.checkData(0, 0, '{"lower_bin":-0.5, "upper_bin":-0.25, "count":0.000000}');
        tdSql.checkData(1, 0, '{"lower_bin":-0.25, "upper_bin":-0.125, "count":0.000000}');
        tdSql.query('select histogram(col_double, \'log_bin\', \'{"start": -0.5, "factor": 0.5, "count": 2, "infinity": false}\', 1) from tb;')
        tdSql.checkRows(2)
        tdSql.checkData(0, 0, '{"lower_bin":-0.5, "upper_bin":-0.25, "count":0.000000}');
        tdSql.checkData(1, 0, '{"lower_bin":-0.25, "upper_bin":-0.125, "count":0.000000}');

        tdSql.query('select histogram(col_double, \'log_bin\', \'{"start": -0.5, "factor": 0.5, "count": 2, "infinity": true}\', 0) from stb;')
        tdSql.checkRows(4)
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":-0.5, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":-0.5, "upper_bin":-0.25, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":-0.25, "upper_bin":-0.125, "count":0}');
        tdSql.checkData(3, 0, '{"lower_bin":-0.125, "upper_bin":inf, "count":13}');
        tdSql.query('select histogram(col_double, \'log_bin\', \'{"start": -0.5, "factor": 0.5, "count": 2, "infinity": true}\', 1) from ctb;')
        tdSql.checkRows(4)
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":-0.5, "count":0.133333}');
        tdSql.checkData(1, 0, '{"lower_bin":-0.5, "upper_bin":-0.25, "count":0.000000}');
        tdSql.checkData(2, 0, '{"lower_bin":-0.25, "upper_bin":-0.125, "count":0.000000}');
        tdSql.checkData(3, 0, '{"lower_bin":-0.125, "upper_bin":inf, "count":0.866667}');
        tdSql.query('select histogram(col_double, \'log_bin\', \'{"start": -0.5, "factor": 0.5, "count": 2, "infinity": true}\', 1) from tb;')
        tdSql.checkRows(4)
        tdSql.checkData(0, 0, '{"lower_bin":-inf, "upper_bin":-0.5, "count":0.133333}');
        tdSql.checkData(1, 0, '{"lower_bin":-0.5, "upper_bin":-0.25, "count":0.000000}');
        tdSql.checkData(2, 0, '{"lower_bin":-0.25, "upper_bin":-0.125, "count":0.000000}');
        tdSql.checkData(3, 0, '{"lower_bin":-0.125, "upper_bin":inf, "count":0.866667}');

        #ERROR CASE
        tdSql.error('select histogram(col_smallint, "user_input", "[1,3,5,7]", -10) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 2) from ctb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 3.14) from tb;')

        tdSql.error('select histogram(col_bigint, \'linear_bin\', \'{"start": 1, "width": 5, "count": 2, "infinity": false}\', true) from stb;')
        tdSql.error('select histogram(col_bigint, \'linear_bin\', \'{"start": 1, "width": 5, "count": 2, "infinity": false}\', false) from ctb;')

        tdSql.error('select histogram(col_double, \'log_bin\', \'{"start": -0.5, "factor": 0.5, "count": 2, "infinity": true}\', "abc") from tb;')
        tdSql.error('select histogram(col_double, \'log_bin\', \'{"start": -0.5, "factor": 0.5, "count": 2, "infinity": true}\', abc) from tb;')

        print("============== STEP 4: combinations ================== ")
        ## Combinations ##
        #select distinct func(col_name)
        tdSql.error('select distinct histogram(col_tinyint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select distinct histogram(col_smallint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select distinct histogram(col_int, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select distinct histogram(col_bigint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select distinct histogram(col_float, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select distinct histogram(col_double, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select distinct histogram(col_bool, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select distinct histogram(col_timestamp, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select distinct histogram(col_nchar, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select distinct histogram(col_binary, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select distinct histogram(tag_tinyint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select distinct histogram(tag_smallint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select distinct histogram(tag_int, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select distinct histogram(tag_bigint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select distinct histogram(tag_float, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select distinct histogram(tag_double, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select distinct histogram(tag_bool, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select distinct histogram(tag_timestamp, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select distinct histogram(tag_nchar, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select distinct histogram(tag_binary, "user_input", "[1,3,5,7]", 0) from stb;')

        tdSql.error('select histogram(*, "user_input", "[1,3,5,7]", 0) from stb;')

        #select func(col_name arith_oper xxx)
        tdSql.error('select histogram(col_int + 1, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_int - 1, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_int * 2.0, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_int / 2.0, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_int % 2.0, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_timestamp + now, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_int + col_bigint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_int - col_bigint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_int * col_bigint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_int / col_bigint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_int % col_bigint, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_int + pow(1,2), "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_int - abs(-100), "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_int * round(col_float), "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_int / ceil(1.5), "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_int % floor(col_double), "user_input", "[1,3,5,7]", 0) from stb;')

        #select func() arith_oper xxx
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) + 1 from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) - 1 from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) * 1 from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) / 1 from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) % 1 from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) + col_double from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) - col_double from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) * col_double from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) / col_double from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) % col_double from stb;')

        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) + abs(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) - ceil(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) * floor(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) / round(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) % acos(col_double) from stb;')

        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) + max(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) - min(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) * first(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) / last(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) % top(col_double, 1) from stb;')

        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) + sum(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) - avg(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) * count(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) / stddev(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0) % twa(col_double) from stb;')

        #select func(),xxx
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),col_tinyint from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),col_smallint from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),col_int from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),col_bigint from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),col_timstamp from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),col_bool from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),col_float from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),col_double from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),col_binary from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),col_nchar from stb;')

        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_tinyint from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_smallint from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_int from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_bigint from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_timstamp from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_bool from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_float from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_double from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_binary from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_nchar from stb;')

        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_tinyint from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_smallint from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_int from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_bigint from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_timstamp from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_bool from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_float from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_double from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_binary from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tag_nchar from stb;')

        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),ts from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),tbname from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),_c0 from stb;')
        tdSql.error('select histogram(tag_int, "user_input", "[1,3,5,7]", 0),_C0 from stb;')

        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),abs(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),ceil(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),floor(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),round(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),acos(col_double) from stb;')

        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),max(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),min(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),first(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),last(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),top(col_double, 1) from stb;')

        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),sum(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),avg(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),count(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),stddev(col_double) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),twa(col_double) from stb;')

        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),histogram(col_int, "user_input", "[1,3,5,7]", 0) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),histogram(col_int, "linear_bin", \'{"start": -1, "width":5, "count":5, "infinity":false}\', 0) from stb;')
        tdSql.error('select histogram(col_int, "user_input", "[1,3,5,7]", 0),histogram(col_int, "log_bin", \'{"start": 10, "factor":0.5, "count":5, "infinity":false}\', 0) from stb;')

        #select where condition
        tdSql.query('select histogram(col_int, "user_input", "[1,3,5,7,9,15]", 0) from tb;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[1,3,5,7,9,15]", 0) from tb where col_int > 3;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[1,3,5,7,9,15]", 0) from tb where col_int < 7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":0}');
        tdSql.query('select histogram(col_int, "user_input", "[1,3,5,7,9,15]", 0) from tb where col_int >= 3;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[1,3,5,7,9,15]", 0) from tb where col_int <= 7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":0}');
        tdSql.query('select histogram(col_int, "user_input", "[1,3,5,7,9,15]", 0) from tb where col_int = 7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":0}');
        tdSql.query('select histogram(col_int, "user_input", "[1,3,5,7,9,15]", 0) from tb where col_int != 7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[1,3,5,7,9,15]", 0) from tb where col_int <> 7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[1,3,5,7,9,15]", 0) from tb where col_int > 5 and col_int <7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":0}');
        tdSql.query('select histogram(col_int, "user_input", "[1,3,5,7,9,15]", 0) from tb where col_int >= 5 and col_int <=7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":1}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":0}');
        tdSql.query('select histogram(col_int, "user_input", "[1,3,5,7,9,15]", 0) from tb where col_int between 5 and 7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":1}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":0}');

        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5,7,9,15]", 0) from ctb;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5,7,9,15]", 0) from ctb where col_tinyint > 3;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5,7,9,15]", 0) from ctb where col_tinyint < 7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":0}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5,7,9,15]", 0) from ctb where col_tinyint >= 3;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5,7,9,15]", 0) from ctb where col_tinyint <= 7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":0}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5,7,9,15]", 0) from ctb where col_tinyint = 7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":0}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5,7,9,15]", 0) from ctb where col_tinyint != 7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5,7,9,15]", 0) from ctb where col_tinyint <> 7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5,7,9,15]", 0) from ctb where col_tinyint > 5 and col_tinyint <7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":0}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5,7,9,15]", 0) from ctb where col_tinyint >= 5 and col_tinyint <=7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":1}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":0}');
        tdSql.query('select histogram(col_tinyint, "user_input", "[1,3,5,7,9,15]", 0) from ctb where col_tinyint between 5 and 7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":1}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":0}');

        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where col_bigint > 3;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where col_bigint < 7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":0}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where col_bigint >= 3;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where col_bigint <= 7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":0}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where col_bigint = 7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":0}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where col_bigint != 7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where col_bigint <> 7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where col_bigint > 5 and col_bigint <7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":0}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":0}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where col_bigint >= 5 and col_bigint <=7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":1}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":0}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where col_bigint between 5 and 7;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":0}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":1}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":0}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":0}');

        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where tag_bigint > 0;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where tag_bigint < 2;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where tag_bigint >= 1;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where tag_bigint <= 1;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where tag_bigint = 1;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where tag_bigint != 2;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where tag_bigint <> 2;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where tag_bigint > 0 and tag_bigint < 2;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where tag_bigint >= 1 and tag_bigint <= 1;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_bigint, "user_input", "[1,3,5,7,9,15]", 0) from stb where tag_bigint between 0 and 2;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');

        #select session
        #tdSql.query('select histogram(col_int, "user_input", "[0,10]", 0) from tb session (col_timestamp, 1w);')
        #tdSql.checkRows(1)
        #tdSql.checkData(0, 1, '{"lower_bin":0, "upper_bin":10, "count":10}');

        #tdSql.query('select histogram(col_int, "user_input", "[0,10]", 0) from tb session (col_timestamp, 1d);')
        #tdSql.checkRows(1)
        #tdSql.checkData(0, 1, '{"lower_bin":0, "upper_bin":10, "count":10}');

        #tdSql.query('select histogram(col_int, "user_input", "[0,10]", 0) from tb session (col_timestamp, 1h);')
        #tdSql.checkRows(1)
        #tdSql.checkData(0, 1, '{"lower_bin":0, "upper_bin":10, "count":10}');

        #tdSql.query('select histogram(col_int, "user_input", "[0,10]", 0) from tb session (col_timestamp, 1m);')
        #tdSql.checkRows(1)
        #tdSql.checkData(0, 1, '{"lower_bin":0, "upper_bin":10, "count":10}');

        #tdSql.query('select histogram(col_int, "user_input", "[0,10]", 0) from tb session (col_timestamp, 1s);')
        #tdSql.checkRows(16)
        #tdSql.checkData(0,  1, "(0:10]:0");
        #tdSql.checkData(1,  1, "(0:10]:0");
        #tdSql.checkData(2,  1, "(0:10]:1");
        #tdSql.checkData(3,  1, "(0:10]:1");
        #tdSql.checkData(4,  1, "(0:10]:1");
        #tdSql.checkData(5,  1, "(0:10]:1");
        #tdSql.checkData(6,  1, "(0:10]:1");
        #tdSql.checkData(7,  1, "(0:10]:1");
        #tdSql.checkData(8,  1, "(0:10]:1");
        #tdSql.checkData(9, 1,  "(0:10]:1");
        #tdSql.checkData(10, 1,  "(0:10]:1");
        #tdSql.checkData(11, 1,  "(0:10]:1");
        #tdSql.checkData(12, 1,  "(0:10]:0");
        #tdSql.checkData(13, 1,  "(0:10]:0");
        #tdSql.checkData(14, 1,  "(0:10]:0");
        #tdSql.checkData(15, 1,  "(0:10]:0");

        #tdSql.query('select histogram(col_int, "user_input", "[0,10]", 0) from tb session (col_timestamp, 1a);')
        #tdSql.checkRows(16)
        #tdSql.checkData(0,  1, "(0:10]:0");
        #tdSql.checkData(1,  1, "(0:10]:0");
        #tdSql.checkData(2,  1, "(0:10]:1");
        #tdSql.checkData(3,  1, "(0:10]:1");
        #tdSql.checkData(4,  1, "(0:10]:1");
        #tdSql.checkData(5,  1, "(0:10]:1");
        #tdSql.checkData(6,  1, "(0:10]:1");
        #tdSql.checkData(7,  1, "(0:10]:1");
        #tdSql.checkData(8,  1, "(0:10]:1");
        #tdSql.checkData(9, 1,  "(0:10]:1");
        #tdSql.checkData(10, 1,  "(0:10]:1");
        #tdSql.checkData(11, 1,  "(0:10]:1");
        #tdSql.checkData(12, 1,  "(0:10]:0");
        #tdSql.checkData(13, 1,  "(0:10]:0");
        #tdSql.checkData(14, 1,  "(0:10]:0");
        #tdSql.checkData(15, 1,  "(0:10]:0");

        #select state_window
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from tb state_window(col_timestamp);')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from tb state_window(col_tinyint);')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from tb state_window(col_smallint);')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from tb state_window(col_int);')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from tb state_window(col_bigint);')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from tb state_window(col_bool);')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from tb state_window(col_float);')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from tb state_window(col_double);')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from tb state_window(col_binary);')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from tb state_window(col_nchar);')

        #select interval/sliding/fill
        #tdSql.query('select histogram(col_int, "user_input", "[0,10]", 0) from tb interval(1y);')
        #tdSql.checkRows(1)
        #tdSql.checkData(0, 1, '{"lower_bin":0, "upper_bin":10, "count":10}');

        #tdSql.query('select histogram(col_int, "user_input", "[0,10]", 0) from tb interval(1n);')
        #tdSql.checkRows(1)
        #tdSql.checkData(0, 1, '{"lower_bin":0, "upper_bin":10, "count":10}');

        #tdSql.query('select histogram(col_int, "user_input", "[0,10]", 0) from tb interval(1w);')
        #tdSql.checkRows(1)
        #tdSql.checkData(0, 1, '{"lower_bin":0, "upper_bin":10, "count":10}');

        #tdSql.query('select histogram(col_int, "user_input", "[0,10]", 0) from tb interval(1d);')
        #tdSql.checkRows(1)
        #tdSql.checkData(0, 1, '{"lower_bin":0, "upper_bin":10, "count":10}');

        #tdSql.query('select histogram(col_int, "user_input", "[0,10]", 0) from tb interval(1h);')
        #tdSql.checkRows(1)
        #tdSql.checkData(0, 1, '{"lower_bin":0, "upper_bin":10, "count":10}');

        #tdSql.query('select histogram(col_int, "user_input", "[0,10]", 0) from tb interval(1s);')
        #tdSql.checkRows(16)
        #tdSql.checkData(0, 1, '{"lower_bin":0, "upper_bin":10, "count":0}');
        #tdSql.checkData(1, 1, '{"lower_bin":0, "upper_bin":10, "count":0}');
        #tdSql.checkData(2, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(3, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(4, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(5, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(6, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(7, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(8, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(9, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(10, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(11, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(12, 1, '{"lower_bin":0, "upper_bin":10, "count":0}');
        #tdSql.checkData(13, 1, '{"lower_bin":0, "upper_bin":10, "count":0}');
        #tdSql.checkData(14, 1, '{"lower_bin":0, "upper_bin":10, "count":0}');
        #tdSql.checkData(15, 1, '{"lower_bin":0, "upper_bin":10, "count":0}');
        #tdSql.query('select histogram(col_int, "user_input", "[0,10]", 0) from tb interval(1a);')
        #tdSql.checkRows(16)
        #tdSql.checkData(0, 1, '{"lower_bin":0, "upper_bin":10, "count":0}');
        #tdSql.checkData(1, 1, '{"lower_bin":0, "upper_bin":10, "count":0}');
        #tdSql.checkData(2, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(3, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(4, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(5, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(6, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(7, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(8, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(9, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(10, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(11, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(12, 1, '{"lower_bin":0, "upper_bin":10, "count":0}');
        #tdSql.checkData(13, 1, '{"lower_bin":0, "upper_bin":10, "count":0}');
        #tdSql.checkData(14, 1, '{"lower_bin":0, "upper_bin":10, "count":0}');
        #tdSql.checkData(15, 1, '{"lower_bin":0, "upper_bin":10, "count":0}');

        #tdSql.query('select histogram(col_int, "user_input", "[0,10]", 0) from tb interval(1w) sliding(1w);')
        #tdSql.checkRows(1)
        #tdSql.checkData(0, 1, '{"lower_bin":0, "upper_bin":10, "count":10}');

        #tdSql.query('select histogram(col_int, "user_input", "[0,10]", 0) from tb interval(1d) sliding(1d);')
        #tdSql.checkRows(1)
        #tdSql.checkData(0, 1, '{"lower_bin":0, "upper_bin":10, "count":10}');

        #tdSql.query('select histogram(col_int, "user_input", "[0,10]", 0) from tb interval(1h) sliding(1h);')
        #tdSql.checkRows(1)
        #tdSql.checkData(0, 1, '{"lower_bin":0, "upper_bin":10, "count":10}');

        #tdSql.query('select histogram(col_int, "user_input", "[0,10]", 0) from tb interval(1s) sliding(1s);')
        #tdSql.checkRows(16)
        #tdSql.checkData(0, 1, '{"lower_bin":0, "upper_bin":10, "count":0}');
        #tdSql.checkData(1, 1, '{"lower_bin":0, "upper_bin":10, "count":0}');
        #tdSql.checkData(2, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(3, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(4, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(5, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(6, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(7, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(8, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(9, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(10, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(11, 1, '{"lower_bin":0, "upper_bin":10, "count":1}');
        #tdSql.checkData(12, 1, '{"lower_bin":0, "upper_bin":10, "count":0}');
        #tdSql.checkData(13, 1, '{"lower_bin":0, "upper_bin":10, "count":0}');
        #tdSql.checkData(14, 1, '{"lower_bin":0, "upper_bin":10, "count":0}');
        #tdSql.checkData(15, 1, '{"lower_bin":0, "upper_bin":10, "count":0}');

        #tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from tb where col_timestamp > now - 1w and col_timestamp < now + 1w interval(1w) fill(NULL);')
        #tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from tb where col_timestamp > now - 1d and col_timestamp < now + 1d interval(1d) fill(None);')
        #tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from tb where col_timestamp > now - 1h and col_timestamp < now + 1h interval(1h) fill(Prev);')
        #tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from tb where col_timestamp > now - 1m and col_timestamp < now + 1m interval(1m) fill(Next);')
        #tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from tb where col_timestamp > now - 1s and col_timestamp < now + 1s interval(1s) fill(Linear);')
        #tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from tb where col_timestamp > now - 1a and col_timestamp < now + 1a interval(1a) fill(Value, 1);')

        #select group by
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by col_tinyint;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by col_smallint;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by col_int;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by col_bigint;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by col_bool;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by col_float;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by col_double;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by col_binary;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by col_nchar;')

        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by tag_tinyint;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by tag_smallint;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by tag_int;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by tag_bigint;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by tag_bool;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by tag_float;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by tag_double;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by tag_binary;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by tag_nchar;')

        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by tbname;')

        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by tag_tinyint,col_tinyint;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by tag_smallint,col_smallint;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by tag_int,col_int;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by tag_bigint,col_bigint;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by tag_bool,col_bool;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by tag_float,col_float;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by tag_double,col_double;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by tag_binary,col_binary;')
        tdSql.error('select histogram(col_int, "user_input", "[0,10]", 0) from stb group by tag_nchar,col_nchar;')

        #select order by
        tdSql.query('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by col_timestamp;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');

        tdSql.query('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by col_timestamp desc;')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');

        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by col_tinyint;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by col_tinyint desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by col_smallint;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by col_smallint desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by col_int;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by col_int desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by col_bigint;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by col_bigint desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by col_bool;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by col_bool desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by col_float;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by col_float desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by col_double;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by col_double desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by col_double;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by col_double desc;')

        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_timestamp;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_timestamp desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_tinyint;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_tinyint desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_smallint;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_smallint desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_int;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_int desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_bigint;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_bigint desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_bool;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_bool desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_float;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_float desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_double;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_double desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_double;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_double desc;')

        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tbname;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tbname desc;')

        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_timestamp,col_timestamp;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_timestamp,col_timestamp desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_tinyint,col_timestamp;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_tinyint,col_timestamp desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_smallint,col_timestamp;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_smallint,col_timestamp desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_int,col_timestamp;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_int,col_timestamp desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_bigint,col_timestamp;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_bigint,col_timestamp desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_bool,col_timestamp;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_bool,col_timestamp desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_float,col_timestamp;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_float,col_timestamp desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_double,col_timestamp;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_double,col_timestamp desc;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_double,col_timestamp;')
        tdSql.error('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by tag_double,col_timestamp desc;')

        #select limit/offset
        tdSql.query('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb limit 3;')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from ctb limit 3;')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from tb limit 3;')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');

        tdSql.query('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb limit 3 offset 2;')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from ctb limit 3 offset 2;')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from tb limit 3 offset 2;')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');

        tdSql.query('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb limit 2,3;')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from ctb limit 2,3;')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from tb limit 2,3;')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');

        #nested query
        tdSql.query('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from (select * from stb);')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from (select * from ctb);')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from (select * from tb);')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');

        tdSql.query('select histogram(val, "user_input", "[0,3,5,7,9,15]", 0) from (select col_int as val from stb);')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(val, "user_input", "[0,3,5,7,9,15]", 0) from (select col_int as val from ctb);')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select histogram(val, "user_input", "[0,3,5,7,9,15]", 0) from (select col_int as val from tb);')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');

        tdSql.query('select * from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb);')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select * from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from ctb)')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select * from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from tb)')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');

        tdSql.query('select _c0 from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb);')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select _c0 from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from ctb)')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select _c0 from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from tb)')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');

        tdSql.query('select first(_c0) from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb);')
        tdSql.checkRows(1)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.query('select first(_c0) from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from ctb)')
        tdSql.checkRows(1)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.query('select first(_c0) from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from tb)')
        tdSql.checkRows(1)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');

        tdSql.query('select last(_c0) from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb);')
        tdSql.checkRows(1)
        tdSql.checkData(0, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select last(_c0) from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from ctb)')
        tdSql.checkRows(1)
        tdSql.checkData(0, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select last(_c0) from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from tb)')
        tdSql.checkRows(1)
        tdSql.checkData(0, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');


        tdSql.query('select _c0 from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb limit 3);')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.query('select _c0 from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from ctb limit 3)')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.query('select _c0 from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from tb limit 3)')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');

        tdSql.query('select _c0 from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb) limit 3;')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.query('select _c0 from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from ctb) limit 3')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.query('select _c0 from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from tb) limit 3')
        tdSql.checkRows(3)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');

        tdSql.query('select _c0 from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb order by col_timestamp);')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select _c0 from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from ctb order by col_timestamp)')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');
        tdSql.query('select _c0 from (select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from tb order by col_timestamp)')
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');

        #join
        tdSql.execute("create stable stb1 (col_timestamp timestamp, col_tinyint tinyint, col_smallint smallint, col_int int, col_bigint bigint, col_float float, col_double double, col_bool bool, col_binary binary(10), col_nchar nchar(10)) \
                       tags(tag_timestamp timestamp, tag_tinyint tinyint, tag_smallint smallint, tag_int int, tag_bigint bigint, tag_float float, tag_double double, tag_bool bool, tag_binary binary(10), tag_nchar nchar(10));")
        tdSql.execute("create table ctb1 using stb1 tags (now, 1, 1, 1, 1, 1.0, 1.0, true, 'abc', 'abc');")
        tdSql.execute("create table tb1 (col_timestamp timestamp, col_tinyint tinyint, col_smallint smallint, col_int int, col_bigint bigint, col_float float, col_double double, col_bool bool, col_binary binary(10), col_nchar nchar(10));")

        tdSql.execute("insert into ctb1 values ('2022-01-01 00:00:00', -9, -9, -9, -9, -9.5, -9.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb1 values ('2022-01-01 00:00:01', -1, -1, -1, -1, -1.5, -1.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb1 values ('2022-01-01 00:00:02', 1, 1, 1, 1, 1.5, 1.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb1 values ('2022-01-01 00:00:03', 2, 2, 2, 2, 2.5, 2.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb1 values ('2022-01-01 00:00:04', 3, 3, 3, 3, 3.5, 3.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb1 values ('2022-01-01 00:00:05', 4, 4, 4, 4, 4.5, 4.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb1 values ('2022-01-01 00:00:06', 5, 5, 5, 5, 5.5, 5.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb1 values ('2022-01-01 00:00:07', 6, 6, 6, 6, 6.5, 6.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb1 values ('2022-01-01 00:00:08', 7, 7, 7, 7, 7.5, 7.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb1 values ('2022-01-01 00:00:09', 8, 8, 8, 8, 8.5, 8.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb1 values ('2022-01-01 00:00:10', 9, 9, 9, 9, 9.5, 9.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb1 values ('2022-01-01 00:00:11', 10, 10, 10, 10, 10.5, 10.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb1 values ('2022-01-01 00:00:12', 15, 15, 15, 15, 15.5, 15.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb1 values ('2022-01-01 00:00:13', 20, 20, 20, 20, 20.5, 20.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb1 values ('2022-01-01 00:00:14', 99, 99, 99, 99, 99.5, 99.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb1 values ('2022-01-01 00:00:15', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);")

        tdSql.execute("insert into tb1 values ('2022-01-01 00:00:00', -9, -9, -9, -9, -9.5, -9.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb1 values ('2022-01-01 00:00:01', -1, -1, -1, -1, -1.5, -1.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb1 values ('2022-01-01 00:00:02', 1, 1, 1, 1, 1.5, 1.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb1 values ('2022-01-01 00:00:03', 2, 2, 2, 2, 2.5, 2.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb1 values ('2022-01-01 00:00:04', 3, 3, 3, 3, 3.5, 3.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb1 values ('2022-01-01 00:00:05', 4, 4, 4, 4, 4.5, 4.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb1 values ('2022-01-01 00:00:06', 5, 5, 5, 5, 5.5, 5.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb1 values ('2022-01-01 00:00:07', 6, 6, 6, 6, 6.5, 6.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb1 values ('2022-01-01 00:00:08', 7, 7, 7, 7, 7.5, 7.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb1 values ('2022-01-01 00:00:09', 8, 8, 8, 8, 8.5, 8.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb1 values ('2022-01-01 00:00:10', 9, 9, 9, 9, 9.5, 9.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb1 values ('2022-01-01 00:00:11', 10, 10, 10, 10, 10.5, 10.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb1 values ('2022-01-01 00:00:12', 15, 15, 15, 15, 15.5, 15.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb1 values ('2022-01-01 00:00:13', 20, 20, 20, 20, 20.5, 20.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb1 values ('2022-01-01 00:00:14', 99, 99, 99, 99, 99.5, 99.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb1 values ('2022-01-01 00:00:15', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);")

        tdSql.execute("create stable stb2 (col_timestamp timestamp, col_tinyint tinyint, col_smallint smallint, col_int int, col_bigint bigint, col_float float, col_double double, col_bool bool, col_binary binary(10), col_nchar nchar(10)) \
                       tags(tag_timestamp timestamp, tag_tinyint tinyint, tag_smallint smallint, tag_int int, tag_bigint bigint, tag_float float, tag_double double, tag_bool bool, tag_binary binary(10), tag_nchar nchar(10));")
        tdSql.execute("create table ctb2 using stb2 tags (now, 1, 1, 1, 1, 1.0, 1.0, true, 'abc', 'abc');")
        tdSql.execute("create table tb2 (col_timestamp timestamp, col_tinyint tinyint, col_smallint smallint, col_int int, col_bigint bigint, col_float float, col_double double, col_bool bool, col_binary binary(10), col_nchar nchar(10));")

        tdSql.execute("insert into ctb2 values ('2022-01-01 00:00:00', -9, -9, -9, -9, -9.5, -9.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb2 values ('2022-01-01 00:00:01', -1, -1, -1, -1, -1.5, -1.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb2 values ('2022-01-01 00:00:02', 1, 1, 1, 1, 1.5, 1.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb2 values ('2022-01-01 00:00:03', 2, 2, 2, 2, 2.5, 2.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb2 values ('2022-01-01 00:00:04', 3, 3, 3, 3, 3.5, 3.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb2 values ('2022-01-01 00:00:05', 4, 4, 4, 4, 4.5, 4.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb2 values ('2022-01-01 00:00:06', 5, 5, 5, 5, 5.5, 5.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb2 values ('2022-01-01 00:00:07', 6, 6, 6, 6, 6.5, 6.5, true, 'abc', 'abc');")
        tdSql.execute("insert into ctb2 values ('2022-01-01 00:00:08', 7, 7, 7, 7, 7.5, 7.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb2 values ('2022-01-01 00:00:09', 8, 8, 8, 8, 8.5, 8.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb2 values ('2022-01-01 00:00:10', 9, 9, 9, 9, 9.5, 9.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb2 values ('2022-01-01 00:00:11', 10, 10, 10, 10, 10.5, 10.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb2 values ('2022-01-01 00:00:12', 15, 15, 15, 15, 15.5, 15.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb2 values ('2022-01-01 00:00:13', 20, 20, 20, 20, 20.5, 20.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb2 values ('2022-01-01 00:00:14', 99, 99, 99, 99, 99.5, 99.5, false, 'abc', 'abc');")
        tdSql.execute("insert into ctb2 values ('2022-01-01 00:00:15', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);")

        tdSql.execute("insert into tb2 values ('2022-01-01 00:00:00', -9, -9, -9, -9, -9.5, -9.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb2 values ('2022-01-01 00:00:01', -1, -1, -1, -1, -1.5, -1.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb2 values ('2022-01-01 00:00:02', 1, 1, 1, 1, 1.5, 1.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb2 values ('2022-01-01 00:00:03', 2, 2, 2, 2, 2.5, 2.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb2 values ('2022-01-01 00:00:04', 3, 3, 3, 3, 3.5, 3.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb2 values ('2022-01-01 00:00:05', 4, 4, 4, 4, 4.5, 4.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb2 values ('2022-01-01 00:00:06', 5, 5, 5, 5, 5.5, 5.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb2 values ('2022-01-01 00:00:07', 6, 6, 6, 6, 6.5, 6.5, true, 'abc', 'abc');")
        tdSql.execute("insert into tb2 values ('2022-01-01 00:00:08', 7, 7, 7, 7, 7.5, 7.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb2 values ('2022-01-01 00:00:09', 8, 8, 8, 8, 8.5, 8.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb2 values ('2022-01-01 00:00:10', 9, 9, 9, 9, 9.5, 9.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb2 values ('2022-01-01 00:00:11', 10, 10, 10, 10, 10.5, 10.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb2 values ('2022-01-01 00:00:12', 15, 15, 15, 15, 15.5, 15.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb2 values ('2022-01-01 00:00:13', 20, 20, 20, 20, 20.5, 20.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb2 values ('2022-01-01 00:00:14', 99, 99, 99, 99, 99.5, 99.5, false, 'abc', 'abc');")
        tdSql.execute("insert into tb2 values ('2022-01-01 00:00:15', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);")

        tdSql.query('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from tb1, tb2 where tb1.col_timestamp = tb2.col_timestamp;');
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');

        tdSql.query('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from ctb1, ctb2 where ctb1.col_timestamp = ctb2.col_timestamp;');
        tdSql.checkRows(5)
        tdSql.checkData(0, 0, '{"lower_bin":0, "upper_bin":3, "count":3}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":5, "upper_bin":7, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":7, "upper_bin":9, "count":2}');
        tdSql.checkData(4, 0, '{"lower_bin":9, "upper_bin":15, "count":2}');

        #stable join will cause crash
        #tdSql.query('select histogram(col_int, "user_input", "[0,3,5,7,9,15]", 0) from stb1, stb2 where stb1.col_timestamp = stb2.col_timestamp and stb1.tag_int = stb2.tag_int;');
        #tdSql.checkRows(5)
        #tdSql.checkData(0,  0, "(0:3]:3");
        #tdSql.checkData(1,  0, "(3:5]:2");
        #tdSql.checkData(2,  0, "(5:7]:2");
        #tdSql.checkData(3,  0, "(7:9]:2");
        #tdSql.checkData(4,  0, "(9:15]:2");

        #union all
        tdSql.query('select histogram(col_int, \'user_input\', \'[1,3,5]\', 0) from tb1 union all select histogram(col_int, \'user_input\', \'[1,3,5]\', 0) from tb2;')
        tdSql.checkRows(4)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.query('select histogram(col_int, \'user_input\', \'[1,3,5]\', 0) from ctb1 union all select histogram(col_int, \'user_input\', \'[1,3,5]\', 0) from ctb2;')
        tdSql.checkRows(4)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.query('select histogram(col_int, \'user_input\', \'[1,3,5]\', 0) from stb1 union all select histogram(col_int, \'user_input\', \'[1,3,5]\', 0) from stb2;')
        tdSql.checkRows(4)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');

        tdSql.query('select histogram(col_int, \'linear_bin\', \'{"start":1, "width":2, "count":2, "infinity":false}\', 0) from tb1 union all select histogram(col_int, \'linear_bin\', \'{"start":1, "width":2, "count":2, "infinity":false}\', 0) from tb2;')
        tdSql.checkRows(4)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.query('select histogram(col_int, \'linear_bin\', \'{"start":1, "width":2, "count":2, "infinity":false}\', 0) from ctb1 union all select histogram(col_int, \'linear_bin\', \'{"start":1, "width":2, "count":2, "infinity":false}\', 0) from ctb2;')
        tdSql.checkRows(4)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.query('select histogram(col_int, \'linear_bin\', \'{"start":1, "width":2, "count":2, "infinity":false}\', 0) from stb1 union all select histogram(col_int, \'linear_bin\', \'{"start":1, "width":2, "count":2, "infinity":false}\', 0) from stb2;')
        tdSql.checkRows(4)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(1, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":1, "upper_bin":3, "count":2}');
        tdSql.checkData(3, 0, '{"lower_bin":3, "upper_bin":5, "count":2}');

        tdSql.query('select histogram(col_int, \'log_bin\', \'{"start":1, "factor":2, "count":2, "infinity":false}\', 0) from tb1 union all select histogram(col_int, \'log_bin\', \'{"start":1, "factor":2, "count":2, "infinity":false}\', 0) from tb2;')
        tdSql.checkRows(4)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":1, "upper_bin":2, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.query('select histogram(col_int, \'log_bin\', \'{"start":1, "factor":2, "count":2, "infinity":false}\', 0) from ctb1 union all select histogram(col_int, \'log_bin\', \'{"start":1, "factor":2, "count":2, "infinity":false}\', 0) from ctb2;')
        tdSql.checkRows(4)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":1, "upper_bin":2, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.query('select histogram(col_int, \'log_bin\', \'{"start":1, "factor":2, "count":2, "infinity":false}\', 0) from stb1 union all select histogram(col_int, \'log_bin\', \'{"start":1, "factor":2, "count":2, "infinity":false}\', 0) from stb2;')
        tdSql.checkRows(4)
        tdSql.checkData(0, 0, '{"lower_bin":1, "upper_bin":2, "count":1}');
        tdSql.checkData(1, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');
        tdSql.checkData(2, 0, '{"lower_bin":1, "upper_bin":2, "count":1}');
        tdSql.checkData(3, 0, '{"lower_bin":2, "upper_bin":4, "count":2}');


        tdSql.execute('drop database db')
    def stop(self):
        tdSql.close()
        tdLog.success("%s successfully executed" % __file__)


tdCases.addWindows(__file__, TDTestCase())
tdCases.addLinux(__file__, TDTestCase())
