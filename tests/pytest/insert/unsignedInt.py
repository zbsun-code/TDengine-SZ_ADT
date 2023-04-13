# -*- coding: utf-8 -*-

import sys
from util.log import *
from util.cases import *
from util.sql import *


class TDTestCase:
    def init(self, conn, logSql):
        tdLog.debug("start to execute %s" % __file__)
        tdSql.init(conn.cursor(), logSql)

    def run(self):
        tdSql.prepare()

        tdLog.info('=============== step1')
        tdLog.info('create table tb (ts timestamp, speed int unsigned)')
        tdSql.execute('create table tb (ts timestamp, speed int unsigned)')
        tdLog.info("insert into tb values (now, NULL)")
        tdSql.execute("insert into tb values (now, NULL)")
        tdLog.info('select * from tb order by ts desc')
        tdSql.query('select * from tb order by ts desc')
        tdLog.info('tdSql.checkRow(1)')
        tdSql.checkRows(1)
        tdLog.info('tdSql.checkData(0, 1, null)')
        tdSql.checkData(0, 1, None)
        tdLog.info('=============== step2')
        tdLog.info("insert into tb values (now+1m, -1)  -x step2")
        tdSql.error("insert into tb values (now+1m, -1) ")
        tdLog.info("insert into tb values (now+1m, NULL)")
        tdSql.execute("insert into tb values (now+1m, NULL)")
        tdLog.info('select * from tb order by ts desc')
        tdSql.query('select * from tb order by ts desc')
        tdLog.info('tdSql.checkRow(2)')
        tdSql.checkRows(2)
        tdLog.info('tdSql.checkData(0, 1, null)')
        tdSql.checkData(0, 1, None)
        tdLog.info('=============== step3')
        tdLog.info("insert into tb values (now+2m, 4294967294)")
        tdSql.execute("insert into tb values (now+2m, 4294967294)")
        tdLog.info('select * from tb order by ts desc')
        tdSql.query('select * from tb order by ts desc')
        tdLog.info('tdSql.checkRow(3)')
        tdSql.checkRows(3)
        tdLog.info('tdSql.checkData(0, 1, 4294967294)')
        tdSql.checkData(0, 1, 4294967294)
        tdLog.info('=============== step4')
        tdLog.info("insert into tb values (now+3m, 4294967295) -x step4")
        tdSql.error("insert into tb values (now+3m, 4294967295)")
        tdLog.info("insert into tb values (now+3m, NULL)")
        tdSql.execute("insert into tb values (now+3m, NULL)")
        tdLog.info('select * from tb')
        tdSql.query('select * from tb')
        tdLog.info('tdSql.checkRow(4)')
        tdSql.checkRows(4)
        tdLog.info('tdSql.checkData(0, 1, null)')
        tdSql.checkData(0, 1, None)
        tdLog.info('=============== step5')
        tdLog.info("insert into tb values (now+4m, a2)")
        tdSql.error("insert into tb values (now+4m, a2)")
        tdLog.info("insert into tb values (now-4m, -1)")
        tdSql.error("insert into tb values (now-4m, -1)")
        tdLog.info("insert into tb values (now+4m, 0)")
        tdSql.execute("insert into tb values (now+4m, 0)")
        tdLog.info('select * from tb order by ts desc')
        tdSql.query('select * from tb order by ts desc')
        tdLog.info('tdSql.checkRow(5)')
        tdSql.checkRows(5)
        tdLog.info('tdSql.checkData(0, 1, 0)')
        tdSql.checkData(0, 1, 0)
        tdLog.info('=============== step6')
        tdLog.info("insert into tb values (now+5m, 2a)")
        tdSql.error("insert into tb values (now+5m, 2a)")
        tdLog.info("insert into tb values (now+5m, 2)")
        tdSql.execute("insert into tb values (now+5m, 2)")
        tdLog.info('select * from tb order by ts desc')
        tdSql.query('select * from tb order by ts desc')
        tdLog.info('tdSql.checkRow(6)')
        tdSql.checkRows(6)
        tdLog.info('tdSql.checkData(0, 1, 2)')
        tdSql.checkData(0, 1, 2)
        tdLog.info('=============== step7')
        tdLog.info("insert into tb values (now+6m, 2a'1)")
        tdSql.error("insert into tb values (now+6m, 2a'1)")
        tdLog.info("insert into tb values (now+6m, 2)")
        tdSql.execute("insert into tb values (now+6m, 2)")
        tdLog.info('select * from tb order by ts desc')
        tdSql.query('select * from tb order by ts desc')
        tdLog.info('tdSql.checkRow(7)')
        tdSql.checkRows(7)
        tdLog.info('tdSql.checkData(0, 1, 2)')
        tdSql.checkData(0, 1, 2)
        tdLog.info('drop database db')
        tdSql.execute('drop database db')
# convert end

    def stop(self):
        tdSql.close()
        tdLog.success("%s successfully executed" % __file__)


tdCases.addWindows(__file__, TDTestCase())
tdCases.addLinux(__file__, TDTestCase())
