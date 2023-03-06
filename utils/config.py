from Machine.settings import BASE_DIR

EXCHANGE_FUTURE = {
    'SHF': '上海期货交易所',
    'CFE': '中国金融期货交易所',
    'DCE': '大连商品交易所',
    'CZC': '郑州商品交易所',
    'INE': '上海国际能源交易中心',
}

TABLENAME = {
    "fac_table": "tq_factor",
    "fac_category": "tq_factor",
    "sga_table": "tq_signal",
    "sga_category": "tq_signal"
}

# 截面信号IC IR 纳入
SEC_ADD_IC_SIG_THRESHOLD = 0.02
SEC_ADD_IR_SIG_THRESHOLD = 0.12
# 截面信号IC IR 剔除
SEC_SUB_IC_SIG_THRESHOLD = 0.016
SEC_SUB_IR_SIG_THRESHOLD = 0.096

# 时序信号IC IR 纳入
SEQ_ADD_IC_SIG_THRESHOLD = 0.1
SEQ_ADD_IR_SIG_THRESHOLD = 0.75
# 时序信号IC IR 剔除
SEQ_SUB_IC_SIG_THRESHOLD = 0.08
SEQ_SUB_IR_SIG_THRESHOLD = 0.6

# ----------------------
# 截面因子IC IR 纳入
SEC_ADD_IC_FAC_THRESHOLD = 0.01
SEC_ADD_IR_FAC_THRESHOLD = 0.06
# 截面因子IC IR 剔除
SEC_SUB_IC_FAC_THRESHOLD = 0.008
SEC_SUB_IR_FAC_THRESHOLD = 0.048

# 时序因子IC IR 纳入
SEQ_ADD_IC_FAC_THRESHOLD = 0.05
SEQ_ADD_IR_FAC_THRESHOLD = 0.375

# 时序因子IC IR 剔除
SEQ_SUB_IC_FAC_THRESHOLD = 0.04
SEQ_SUB_IR_FAC_THRESHOLD = 0.3

SYS_VERSION = 'v1.0.18a'

MONITOR_ICIR_TIME = '2022-01-01'
SEQ_DATE_TIME = 4

FILE_SEC_SIG_PATH = f"{BASE_DIR}/static/fixtures/rolling_signal_list_platform.json"
FILE_SEC_FAC_PATH = f"{BASE_DIR}/static/fixtures/rolling_factor_list_platform.json"
FILE_SEQ_FAC_PATH = f"{BASE_DIR}/static/fixtures/rolling_factor_list_flatform.json"
FILE_SEQ_SIG_PATH = f"{BASE_DIR}/static/fixtures/rolling_signal_list_flatform.json"
DATABASE_DB = {
    "host": "192.168.1.166",
    "port": 3306,
    "user": "root",
    "passwd": "c298b8c3aa41c3c8",
    "db": "tqmain",
}
