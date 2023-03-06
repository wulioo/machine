import json
from datetime import datetime
from multiprocessing import Pool

from django.test import TestCase, Client



class SystemTest(TestCase):
    def setUp(self) -> None:
        self.Client = Client()

    def test_create_menus(self):
        data1 = {
            # "id": 'null',
            "title": "1",
            "menuSort": 999,
            "path": "1",
            "component": '',
            "componentName": '123',
            "iFrame": False,
            "roles": [],
            "pid": 0,
            "icon": "app",
            "cache": False,
            "hidden": False,
            "type": 0,
            "permission": '',
            "platform": 1
        }
        data2 = {
            "id": '',
            "title": "123412",
            "menuSort": 999,
            "path": "123",
            "component": "123412",
            "componentName": "123412",
            "iFrame": False,
            "roles": [],
            "pid": 1,
            "icon": "backup",
            "cache": False,
            "hidden": False,
            "type": "1",
            "permission": '',
            "platform": 1
        }
        res = self.client.post('/system/menus/', data1, 'application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client.post('/system/menus/', data2, 'application/json')
        self.assertEqual(res.status_code, 201)

    def test_menus_build(self):
        res = self.Client.get('/system/menus/build/', {'platform': 1})
        self.assertEqual(res.status_code, 200)
