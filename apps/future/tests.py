import json
from multiprocessing import Pool

from django.test import TestCase, Client

from Machine.settings import BASE_DIR
from apps.future.models import SysTable
from utils.code import TableTypeCode


# , 'tq_factor', 'tqmain'

class FactorTest(TestCase):
    # fixtures = ['section.json', 'fv_type.json']
    databases = ['default', 'tq_factor', 'tqmain']

    def setUp(self) -> None:
        self.client = Client()
        # self.varieties = ['all', 'zero', 'mean', 'median']
        # self.earnings_fun = ["close_price", "open_price"]
        self.varieties = ['zero', 'mean']  # 默认测试2种
        self.earnings_fun = ["close_price"]  # 默认测试 close

    def test_factor_list(self):
        res = self.client.get('/section/list/', {'type': 'ic', 'platform': 1})
        self.assertGreaterEqual(len(res.data), 1)
        self.assertEqual(res.status_code, 200)

    def test_factor_icir(self):
        redis_key = 111
        param = {
            "section": {
                "fv_1d_fundamental_1": {
                    "factor_list": [
                        "inventory1",
                        "inventory2"
                    ],

                }
            },
            "exchange_future": [
                "SHF",
                "CFE",
                "DCE",
                "CZC",
                "INE"
            ],
            "periods": [
                1,
                3,
                5,
                10
            ],
            "correlation": [
                "pearson",
                "spearman"
            ],
            "stime": "2022-08-16",
            "etime": "2022-11-16",
            "earnings_fun": "close_price",
            "factor_diff": True,
            "factor_sort": True,
            "varieties": "all",
            "redis_key": redis_key
        }
        for ear in self.earnings_fun:
            param['earnings_fun'] = ear
            for var in self.varieties:
                param['varieties'] = var
                res = self.client.post('/section/icir/', param, 'application/json')
                self.assertGreaterEqual(len(res.data), 1)
                self.assertEqual(res.status_code, 201)
                data = self.__test_redis_icir('fv_1d_fundamental_1', redis_key)
                chart = self.__test_redis_ic_chart('fv_1d_fundamental_1', redis_key)

    def test_factor_category_icir(self):
        redis_key = 222
        param = {
            "section": {
                "合成": {
                    "AI": [
                        "v00_mlp_return_5d"
                    ],
                },
                "基本面": {
                    "期限结构": [
                        "basis"
                    ],

                }
            },
            "stime": "2022-08-14",
            "etime": "2022-11-14",
            "factor_diff": True,
            "factor_sort": True,
            "correlation": [
                "pearson",
                "spearman"
            ],
            "periods": [
                1,
                3,
                5,
                10
            ],
            "exchange_future": [
                "SHF",
                "DCE",
                "CZC",
                "INE"
            ],
            "redis_key": redis_key
        }
        for ear in self.earnings_fun:
            param['earnings_fun'] = ear
            for var in self.varieties:
                param['varieties'] = var
                res = self.client.post('/section/fv/category/icir/', param, 'application/json')
                self.assertGreaterEqual(len(res.data), 1)
                self.assertEqual(res.status_code, 201)
                data = self.__test_redis_icir('fv_factor_all_temp', redis_key)
                chart = self.__test_redis_ic_chart('fv_factor_all_temp', redis_key)

    def test_review_icir(self):
        redis_key = 333
        param = {
            "correlation": "pearson,spearman",
            "periods": "1, 3, 5, 10",
            "factor_diff": True,
            "factor_sort": True,
            "redis_key": redis_key
        }
        for ear in self.earnings_fun:
            param['earnings_fun'] = ear
            param['file0'] = ("demo.xlsx", open(f"{BASE_DIR}/fixtures/demo.xlsx", "rb"))
            res = self.client.post('/section/review/icir', param)
            self.assertGreaterEqual(len(res.data), 1)
            self.assertEqual(res.status_code, 200)
            data = self.__test_redis_icir('demo.xlsx', redis_key)
            chart = self.__test_redis_ic_chart('demo.xlsx', redis_key)

    def test_review_multiple_icir(self):
        redis_key = 343
        param = {
            "correlation": "pearson,spearman",
            "periods": "1, 3, 5, 10",
            "factor_diff": True,
            "factor_sort": True,
            "redis_key": redis_key
        }
        for ear in self.earnings_fun:
            param['earnings_fun'] = ear
            param['file0'] = ("predict_mlp_v02.csv", open(f"{BASE_DIR}/fixtures/predict_mlp_v02.csv", "rb"))
            param['file1'] = ("preprocessed.csv", open(f"{BASE_DIR}/fixtures/preprocessed.csv", "rb"))
            res = self.client.post('/section/review/icir', param)
            self.assertGreaterEqual(len(res.data), 1)
            self.assertEqual(res.status_code, 200)
            data = self.__test_redis_icir('predict_mlp_v02.csv', redis_key)
            chart = self.__test_redis_ic_chart('predict_mlp_v02.csv', redis_key)

    def __test_redis_icir(self, table_name, redis_key):
        param = {
            "correlation": "summary",
            "table_name": table_name,
            "redis_key": redis_key
        }
        corr_label = ['label_1', 'label_3', 'label_5', 'label_10']
        result = {}
        for label in corr_label:
            param['corr_label'] = label
            res = self.client.post('/section/ic/', param, 'application/json')
            self.assertGreaterEqual(len(res.data), 1)
            self.assertEqual(res.status_code, 201)
            result[label] = res.data
        return result

    def __test_redis_ic_chart(self, table_name, redis_key):
        param = {
            'table_name': table_name,
            'redis_key': redis_key
        }
        correlation = ["pearson", "spearman"]
        corr_label = ['label_1', 'label_3', 'label_5', 'label_10']

        result = {}
        for corr in correlation:
            param['correlation'] = corr
            result[corr] = {}
            for label in corr_label:
                param['corr_label'] = label
                res = self.client.post('/section/getcorr/', param, 'application/json')
                self.assertGreaterEqual(len(res.data), 1)
                self.assertEqual(res.status_code, 201)
                result[corr][label] = res
        return result

    def test_layered(self):
        redis_key = 444
        param = {
            "section": {
                "fv_1d_fundamental_1": {
                    "factor_list": [
                        "inventory1",
                    ],

                }
            },
            "exchange_future": [
                "SHF",
                "CFE",
                "DCE",
                "CZC",
                "INE"
            ],
            "periods": [1, 3, 5, 10],
            "layered_fun": [
                "直接排序法"
            ],
            "layered_num": [5],
            "stime": "2022-08-14",
            "etime": "2022-11-14",
            "redis_key": redis_key
        }
        for ear in self.earnings_fun:
            param['earnings_fun'] = ear
            for var in self.varieties:
                param['varieties'] = var
                res = self.client.post('/section/zonaltesting/', param, 'application/json')
                self.assertGreaterEqual(len(res.data), 1)
                self.assertEqual(res.status_code, 201)
                data = self.__test_redis_layered('fv_1d_fundamental_1', ["inventory1"], redis_key)

    def test_category_layered(self):
        redis_key = 555
        param = {
            "section": {
                "合成": {
                    "其它": [
                        "signal"
                    ]
                },
                "基本面": {
                    "库存仓单": [
                        "inventory"
                    ]
                }
            },
            "stime": "2022-08-14",
            "etime": "2022-11-14",
            "layered_num": [5],
            "layered_fun": ["直接排序法"],
            "periods": [1, 3, 5, 10],
            "exchange_future": [
                "SHF",
                "DCE",
                "CZC",
                "INE"
            ],
            "redis_key": redis_key
        }
        for ear in self.earnings_fun:
            param['earnings_fun'] = ear
            for var in self.varieties:
                param['varieties'] = var
                res = self.client.post('/section/fv/category/zonaltesting/', param, 'application/json')
                self.assertGreaterEqual(len(res.data), 1)
                self.assertEqual(res.status_code, 201)
                data = self.__test_redis_layered('fv_factor_layered', ['signal', 'inventory'], redis_key)

    def test_review_layered(self):
        redis_key = 666
        param = {
            "layered_num": "5, 7, 10",
            "periods": "1, 3, 5, 10",
            "redis_key": redis_key

        }
        for ear in self.earnings_fun:
            param['earnings_fun'] = ear
            param['file0'] = ("demo.xlsx", open(f"{BASE_DIR}/fixtures/demo.xlsx", "rb"))
            res = self.client.post('/section/review/layered', param)
            self.assertGreaterEqual(len(res.data), 1)
            self.assertEqual(res.status_code, 201)
            data = self.__test_redis_layered('demo.xlsx', ['return_5_norm_predict', 'sharpe_5_norm_predict',
                                                           "return_5_rank_predict"], redis_key)

    def test_review_multiple_layered(self):
        redis_key = 1274
        param = {
            "layered_num": "5, 7, 10",
            "periods": "1, 3, 5, 10",
            "redis_key": redis_key

        }
        for ear in self.earnings_fun:
            param['earnings_fun'] = ear
            param['file0'] = ("predict_mlp_v02.csv", open(f"{BASE_DIR}/fixtures/predict_mlp_v02.csv", "rb"))
            param['file1'] = ("preprocessed.csv", open(f"{BASE_DIR}/fixtures/preprocessed.csv", "rb"))
            res = self.client.post('/section/review/layered', param)
            self.assertGreaterEqual(len(res.data), 1)
            self.assertEqual(res.status_code, 201)
            data = self.__test_redis_layered('predict_mlp_v02.csv', ['5day_ret_0931_rank', '5day_ret_0931_rank_mxm'],
                                             redis_key)

    def __test_redis_layered(self, table_name, factor, redis_key):
        param = {
            "table_name": table_name,
            "redis_key": redis_key,
        }

        group_name = ["group5"]
        factor_label = ["label_1", "label_3", "label_5", "label_10"]

        result = {}
        for f in factor:
            param['section'] = f
            result[f] = {}
            for label in factor_label:
                param['factor_label'] = label
                result[f][label] = {}
                for group in group_name:
                    param['group_name'] = group
                    res = self.client.post('/section/echarts/', param, 'application/json')
                    self.assertGreaterEqual(len(res.data), 1)
                    self.assertEqual(res.status_code, 201)
                    result[f][label][group] = res
        return result

    def test_ndcg(self):
        param = {
            "section": {
                "fv_1d_fundamental_1": {
                    "factor_list": [
                        "inventory1",
                    ],

                }
            },
            "exchange_future": [
                "SHF",
                "CFE",
                "DCE",
                "CZC",
                "INE"
            ],
            "periods": [
                1,
                3,
                5,
                10
            ],
            "stime": "2022-08-14",
            "etime": "2022-11-14",
        }
        for ear in self.earnings_fun:
            param['earnings_fun'] = ear
            for var in self.varieties:
                param['varieties'] = var
                res = self.client.post('/section/ndcg/', param, 'application/json')
                self.assertGreaterEqual(len(res.data), 1)
                self.assertEqual(res.status_code, 200)
                # data = self.__test_redis_ndcg('fv_1d_fundamental_1', redis_key)

    def test_category_ndcg(self):
        param = {
            "section": {
                "合成": {
                    "其它": [
                        "signal"
                    ]
                },
                "基本面": {
                    "期限结构": [
                        "basis"
                    ]
                }
            },
            "stime": "2022-08-14",
            "etime": "2022-11-14",
            "periods": [
                1,
                3,
                5,
                10
            ],
            "exchange_future": [
                "SHF",
                "DCE",
                "CZC",
                "INE"
            ],
        }
        for ear in self.earnings_fun:
            param['earnings_fun'] = ear
            for var in self.varieties:
                param['varieties'] = var
                res = self.client.post('/section/fv/category/ndcg/', param, 'application/json')
                self.assertGreaterEqual(len(res.data), 1)
                self.assertEqual(res.status_code, 200)

    def test_review_ndcg(self):
        param = {
            "periods": "1, 3, 5, 10",
        }
        for ear in self.earnings_fun:
            param['earnings_fun'] = ear
            param['file'] = ("demo.xlsx", open(f"{BASE_DIR}/fixtures/demo.xlsx", "rb"))
            res = self.client.post('/section/review/ndcg', param)
            self.assertGreaterEqual(len(res.data), 1)
            self.assertEqual(res.status_code, 200)

    def test_corr(self):

        param = {
            "section": {
                "fv_1d_fundamental_1": {
                    "factor_list": [
                        "inventory1",
                        "inventory2"
                    ]
                },
                "fv_1d_fundamental_2": {
                    "factor_list": [
                        "basis",
                        "standardized_basis",
                        "momentum",
                        "inventory"
                    ]
                }
            },
            "stime": "2022-05-01",
            "etime": "2022-11-01",
            "factor_sort": True,
            "platform": "1",

        }
        res = self.client.post('/section/corr/', param, 'application/json')
        self.assertGreaterEqual(len(res.data), 1)
        self.assertEqual(res.status_code, 200)

    def test_category_corr(self):

        param = {
            "section": {
                "合成": {
                    "其它": [
                        "signal"
                    ]
                },
                "量价": {
                    "波动率": [
                        "atr_5",
                        "atr_10",
                        "atr_15",
                        "atr_20",
                        "turn_std_6",
                        "idio_vol_5"
                    ]
                }
            },
            "stime": "2022-05-01",
            "etime": "2022-11-01",
            "factor_sort": True,
            "platform": "1",

        }
        res = self.client.post('/section/fv/category/corr/', param, 'application/json')
        self.assertGreaterEqual(len(res.data), 1)
        self.assertEqual(res.status_code, 200)

    def test_review_corr(self):

        param = {"section": json.dumps({
            "fv_1d_fundamental_1": {"factor_list": ["inventory1", "inventory2"]},
            "fv_1d_signal_1": {"factor_list": ["signal"]}
        }),
            "stime": "2021-01-01",
            "etime": "2022-01-01",
            "factor_sort": "true",
            "platform": 1,
            "file": ("demo.xlsx", open(f"{BASE_DIR}/fixtures/demo.xlsx", "rb"))
        }

        res = self.client.post('/section/review/corr', param)
        self.assertGreaterEqual(len(res.data), 1)
        self.assertEqual(res.status_code, 200)

    def test_review_category_corr(self):
        param = {"section": json.dumps({"合成": {"其它": ["signal"]}}),
                 "stime": "2021-01-01",
                 "etime": "2022-01-01",
                 "factor_sort": "true",
                 "platform": 1,
                 "file": ("demo.xlsx", open(f"{BASE_DIR}/fixtures/demo.xlsx", "rb"))
                 }
        res = self.client.post('/section/fv/review/category/corr', param)
        self.assertGreaterEqual(len(res.data), 1)
        self.assertEqual(res.status_code, 200)

    def test_coverage(self):
        param = {
            "section": {
                "fv_1d_fundamental_1": {
                    "factor_list": [
                        "inventory1",
                        "inventory2"
                    ]
                },
                "fv_1d_signal_1": {
                    "factor_list": [
                        "signal"
                    ]
                }
            },
            "stime": "2022-05-01",
            "etime": "2022-11-01",
            "exchange_future": [
                "SHF",
                "DCE",
                "CZC",
                "INE"
            ]
        }
        res = self.client.post('/section/varie/avg/', param, 'application/json')
        self.assertGreaterEqual(len(res.data), 1)
        self.assertEqual(res.status_code, 201)

    def test_category_coverage(self):
        param = {
            "section": {
                "合成": {
                    "其它": [
                        "signal"
                    ]
                },
                "基本面": {
                    "库存仓单": [
                        "inventory",
                        "warehouse_receipt_5",
                        "warehouse_receipt_10",
                        "warehouse_receipt_15",
                        "warehouse_receipt_20"
                    ]
                }
            },
            "stime": "2022-05-01",
            "etime": "2022-11-01",
            "exchange_future": [
                "SHF",
                "DCE",
                "CZC",
                "INE"
            ]
        }
        res = self.client.post('/section/varie/category/avg/', param, 'application/json')
        self.assertGreaterEqual(len(res.data), 1)
        self.assertEqual(res.status_code, 201)

    def test_earnings(self):
        param = {
            "stime": "2022-05-01",
            "etime": "2022-11-01",
            "periods": [
                1,
                3,
                5,
                10
            ],
            "exchange_future": [
                "SHF",
                "DCE",
                "CZC",
                "INE"
            ]
        }
        for ear in self.earnings_fun:
            param["earnings_fun"] = ear
            res = self.client.post('/section/earnings/n/', param, 'application/json')
            self.assertGreaterEqual(len(res.data), 1)
            self.assertEqual(res.status_code, 201)

    def test_sharpe_earnings(self):
        param = {
            "stime": "2022-05-01",
            "etime": "2022-11-01",
            "periods": [
                3,
                5,
                10
            ],
            "exchange_future": [
                "SHF",
                "DCE",
                "CZC",
                "INE"
            ]
        }
        for ear in self.earnings_fun:
            param["earnings_fun"] = ear
            res = self.client.post('/section/earnings/sharpe/', param, 'application/json')
            self.assertGreaterEqual(len(res.data), 1)
            self.assertEqual(res.status_code, 201)

    def test_distribute(self):
        param = {
            "stime": "2022-05-18",
            "etime": "2022-11-18",
            "factor_sort": True,
            "exchange_future": ["SHF", "DCE", "CZC", "INE"]
        }
        table_type_list = ["single_table", "multi_table"]
        for type in table_type_list:
            param["table_type"] = type
            if type == TableTypeCode.SINGLE.value:
                param['section'] = {
                    "fv_1d_fundamental_1": {
                        "factor_list": [
                            "inventory1"
                        ]
                    }
                }
            else:
                param['section'] = {
                    "基本面": {
                        "期限结构": [
                            "basis"
                        ],
                        "库存仓单": [
                            "warehouse_receipt_5"
                        ]
                    }
                }
            res = self.client.post('/section/fv/distribute/', param, 'application/json')
            self.assertGreaterEqual(len(res.data), 1)
            self.assertEqual(res.status_code, 201)

    def test_review_distribute(self):
        param = {
            "file": ("demo.xlsx", open(f"{BASE_DIR}/fixtures/demo.xlsx", "rb"))
        }
        res = self.client.post('/section/fv/review/distribute/', param)
        self.assertGreaterEqual(len(res.data), 1)
        self.assertEqual(res.status_code, 201)
