from __future__ import annotations

from enum import Enum
from typing import Dict, List, NamedTuple

import pandas as pd
import typer
from mysql.connector import MySQLConnection
from tq_data_update import BaseTqmainTableUpdate
from tq_data_update.utils.objects import TimePeriod
from tq_data_update.utils.types import DateWithoutDash
from logs import logger
# from conf.settings import LOG_FILE, db_conf, redis_conf
# from utils.email_notifier import notify


class _Item(NamedTuple):
    type_name: str
    text: List[str]

    def template(self):
        texts = " 和 ".join(self.text)
        return f"{texts} 龙虎榜数据缺失"


class FutureRank(BaseTqmainTableUpdate):
    default_db_settings = {
        "host": "192.168.1.154",
        "port": 3306,
        "user": "daihuizheng",
        "passwd": "Iry7X+pP7D0E+A==",
        "db": "tqmain",
    }
    default_redis_settings = {"host": "192.168.1.166", "port": 6479,"password":"123456"}

    no_send_email = False

    _cron_log = {}  # 存储定时任务状态数据，以json格式上传DB。可以根据具体情况在get_data中对状态数据进行采集

    # log_file = (
    #     LOG_FILE  # 用于exit方法检查是否出现了ERROR，并将ERROR传递给airflow的bashoperator，使其Task failed
    # )

    def get_start_log(self) -> Dict:
        self._cron_log["today"] = str(self.date)
        return self._cron_log

    def get_end_log(self) -> Dict:
        return self._cron_log

    def get_wind_codes(self) -> List[str]:
        conn = self.conn
        today = DateWithoutDash(self.date)
        sql = f"""
        select distinct type_name_ab from tqmain.future_header where ipo_date<='{today}' and last_tradedate>='{today}'
"""
        df = pd.read_sql(sql, con=conn)

        assert not df.empty, f"{df.shape}"

        return df["type_name_ab"].tolist()

    def main(self):
        self.cron_log_start()

        today = DateWithoutDash(self.date)
        if not self.is_trading_date(today):
            self.logger.warning(f"{today} not td")
            return
        html = self.get_data()

        if self.no_send_email:
            self.cron_log_end()
            return

        # self.send_log_email(
        #     LOG_FILE.as_posix(),
        #     notify=notify,
        #     subject="future_rank数据检查",
        #     extra_text=html,
        #     to=[
        #         "zhouyang@transquant.com.cn",
        #         "weinanwang@transquant.com.cn",
        #         "zhaogang@transquant.com.cn",
        #         "tqdata@transquant.com.cn",
        #     ],
        # )

        self.cron_log_end()

    def get_data(self) -> str:
        """日度检查品种层面的rank_type是否有缺失"""
        try:
            today = DateWithoutDash(self.date)
            logger = self.logger
            conn: MySQLConnection = self.conn
            cursor = conn.cursor()

            rank_type2zh = {
                0: "空头持仓",
                1: "多头持仓",
                2: "成交量",
            }

            types = self.wind_codes

            res = []
            for idx, t in enumerate(types):
                logger.debug(f"{idx + 1}/{len(types)} || {t}")
                sql = f"""
                select distinct rank_type from tqmain.future_rank where trading_date='{today}' and wind_code='{t}'
                """

                cursor.execute(sql)

                rank_types = cursor.fetchall()
                if not rank_types:
                    logger.warning(f"{t} || {today} || 无数据")
                    # continue

                rank_types = [i[0] for i in rank_types]
                text = sorted(list(set(rank_type2zh) - set(rank_types)))
                if not text:
                    logger.debug(f"{t} 通过检查 || {today}")
                    continue

                text = [rank_type2zh.get(i) for i in text]

                res.append(_Item(t, text))

            if not res:
                text = "全部品种通过检查"
                logger.success(text)
                return text

            res.sort(key=lambda i: len(i[1]))

            res2 = []
            for i in res:
                res2.append((i.type_name, i.template()))

            df = pd.DataFrame(res2, columns=["品种名", "缺失描述"])

            self.logger.debug(f"res: {len(res)} || {today}")

            return df.to_html()
            # self._insert_db(df, self.table_name)
        except Exception as e:
            self.has_been_raise = True
            raise e

    @property
    def table_name(self) -> str:
        return "tqmain.future_rank"


def main(
        flag: TimePeriod = TimePeriod.Daily, start="", end="", no_send_email: bool = False
):
    logger.info(f"flag: {flag}, {type(flag)}")
    logger.info(f"start: {start}, {type(start)}")
    logger.info(f"end: {end}, {type(end)}")
    logger.info(f"no_send_email: {no_send_email}, {type(no_send_email)}")

    if flag == TimePeriod.Daily:
        FutureRank(no_send_email=no_send_email).daily_update()
    else:
        FutureRank(no_send_email=no_send_email).his_update(start=start, end=end)


if __name__ == "__main__":
    # typer.run(main)
    main()
