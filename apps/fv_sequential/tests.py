from django.test import TestCase, Client

from Machine.settings import BASE_DIR


# Create your tests here.


class SequentialTest(TestCase):
    fixtures = ['section.json']
    databases = ['default', 'tq_factor', 'tqmain']

    def setUp(self) -> None:
        self.client = Client()
        # self.varieties = ['all', 'zero', 'mean', 'median']
        # self.earnings_fun = ["close_price", "open_price"]
        self.varieties = ['zero', 'mean']  # 默认测试2种
        self.earnings_fun = ["close_price"]  # 默认测试 close

    def test_sequential_icir(self):
        param = {
            "section": {
                "fv_1d_fundamental_1": {
                    "factor_list": [
                        "inventory1",
                        "inventory2"
                    ]
                }
            },
            "stime": "2022-08-14",
            "etime": "2022-11-14",
            "windows": [
                5,
                20,
                60,
                120,
                240
            ],
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
            ]
        }

        for ear in self.earnings_fun:
            param['earnings_fun'] = ear
            for var in self.varieties:
                param['varieties'] = var
                res = self.client.post('/fv_sequential/icir/', param, 'application/json')
                self.assertGreaterEqual(len(res.data), 1)
                self.assertEqual(res.status_code, 201)
                self.__test_redis_icir(res.data.get('fv_1d_fundamental_1')['AL.SHF'])

    def test_sequential_category_icir(self):
        param = {
            "section": {
                "合成": {
                    "其它": [
                        "signal"
                    ]
                },
                "基本面": {
                    "库存仓单": [
                        "warehouse_receipt_5"
                    ]
                }
            },
            "stime": "2022-08-14",
            "etime": "2022-11-14",
            "windows": [
                5,
                20,
                60,
                120,
                240
            ],

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
            ]
        }
        for ear in self.earnings_fun:
            param['earnings_fun'] = ear
            for var in self.varieties:
                param['varieties'] = var
                res = self.client.post('/fv_sequential/category/icir/', param, 'application/json')
                self.assertGreaterEqual(len(res.data), 1)
                self.assertEqual(res.status_code, 201)
                self.__test_redis_icir(res.data.get('seq_factor_temp')['AL.SHF'])

    def test_req_review_icir(self):

        param = {
            "correlation": "pearson,spearman",
            "periods_list": "1, 3, 5, 10",
            "windows": "5,20,60,120,240,480,till_now"

        }
        for ear in self.earnings_fun:
            param['earnings_fun'] = ear
            param['file'] = ("demo.xlsx", open(f"{BASE_DIR}/fixtures/demo.xlsx", "rb"))
            res = self.client.post('/fv_sequential/review/icir/', param)
            self.assertGreaterEqual(len(res.data), 1)
            self.assertEqual(res.status_code, 200)
            self.__test_redis_icir(res.data.get('demo.xlsx')['M.DCE'])

    def __test_redis_icir(self, table_type):
        param = {
            "table_type": table_type,
            "corr_label": "label_1",
            "windows": 5,

        }
        for corr in ["pearson", "spearman"]:
            param['corr'] = corr
            res = self.client.post('/fv_sequential/redis_icir/', param, 'application/json')
            self.assertGreaterEqual(len(res.data), 1)
            self.assertEqual(res.status_code, 201)
