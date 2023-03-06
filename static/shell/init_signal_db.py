import pandas as pd

from service.db import MysqlDb


def main():
    signal_json = dict()
    fv_1d_ai_co_1 = ["v00_mlp_return_5d", "v00_mlp_sharpe_5d", "v00_mlp_r_rank_5d"]
    with MysqlDb() as db:
        sql_1 = f"""SELECT factor FROM (
					SELECT
						TABLE_NAME as t_name,
						COLUMN_NAME as factor 
					FROM
						information_schema.COLUMNS 
					WHERE
						`table_schema` = 'tq_signal'
						and TABLE_NAME BETWEEN 'fv_1d_ai_5' AND 'fv_1d_ai_9'
						AND COLUMN_NAME NOT IN ('upload_user' ,'upload_time' ,'trading_date','type_name_ab')
						) t 
						WHERE factor like '%_1_rank%' or factor like '%_2_rank%' or factor like '%_3_rank%' or factor like '%_5_rank%'"""

        signal_json[1] = pd.read_sql(sql_1, con=db.conn)['factor'].to_list()

        sql_5 = f"""SELECT factor FROM (
        					SELECT
        						TABLE_NAME as t_name,
        						COLUMN_NAME as factor 
        					FROM
        						information_schema.COLUMNS 
        					WHERE
        						`table_schema` = 'tq_signal'
        						and TABLE_NAME BETWEEN 'fv_1d_ai_5' AND 'fv_1d_ai_9'
        						AND COLUMN_NAME NOT IN ('upload_user' ,'upload_time' ,'trading_date','type_name_ab')
        						) t 
        						WHERE factor like '%_5_rank%' or factor like '%_10_rank%'"""

        signal_json[5] = pd.read_sql(sql_5, con=db.conn)['factor'].to_list() + fv_1d_ai_co_1

        sql_10 = f"""SELECT factor FROM (
        					SELECT
        						TABLE_NAME as t_name,
        						COLUMN_NAME as factor 
        					FROM
        						information_schema.COLUMNS 
        					WHERE
        						`table_schema` = 'tq_signal'
        						and TABLE_NAME BETWEEN 'fv_1d_ai_5' AND 'fv_1d_ai_9'
        						AND COLUMN_NAME NOT IN ('upload_user' ,'upload_time' ,'trading_date','type_name_ab')
        						) t 
        						WHERE  factor like '%_10_rank%'"""

        signal_json[10] = pd.read_sql(sql_10, con=db.conn)['factor'].to_list() + fv_1d_ai_co_1


if __name__ == '__main__':
    main()
