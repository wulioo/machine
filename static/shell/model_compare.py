"""
模型对比工具：自动化对比差异并输出到控制台，之后便于手动合并冲突
    1，从DB下载models文件
    2，读取本地models文件
    3，对比两个models文件的所有类的集合，找出差异的类并输出到控制台
    4，对公共部分类的每个方法、属性进行对比，输出差异的类
"""
import os
from importlib import import_module
from pathlib import Path
from typing import AnyStr

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Machine.settings')

CURRENT_DIR = Path(
    os.path.abspath(__file__)
).parent

NEW_MODEL_FILE = CURRENT_DIR / 'new_models.py'
OLD_MODELS_FILE = CURRENT_DIR / "old_models.py"

TQMAIN_MODELS_PATH = CURRENT_DIR.parent / "tqmain" / "models.py"
TQMODEL_MODELS_PATH = CURRENT_DIR.parent / "extra" / "db" / "models_tqfactor.py"

REPLACE = """
from unittest.mock import MagicMock\n
models = MagicMock()
"""


class ModelsOutput(object):
    file = open(NEW_MODEL_FILE, 'w', encoding='utf-8')

    @classmethod
    def write(cls, s: AnyStr):
        if "from django.db import models" in s:
            s = REPLACE
        # s = s.replace("models.Model", "")
        cls.file.write(s)

    @classmethod
    def close(cls):
        cls.file.close()


def get_models_set(obj: object):
    return set(obj.__dict__.keys())


def get_fields_set(obj: object):
    return set(obj.__dict__['_mock_return_value'].keys())


class ModelsUtil(object):
    options = {
        "database": "tq_model_predict",
        "include_partitions": True,
        "include_views": True,
        "table": []

    }

    @staticmethod
    def copy_tqmain_models_to_here():
        with open(TQMAIN_MODELS_PATH, 'r', encoding='utf-8') as f_read:
            with open(OLD_MODELS_FILE, 'w', encoding='utf-8') as f_write:
                for line in f_read:
                    if "from django.db import models" in line:
                        line = REPLACE
                        # line = line.replace("models.Model", "")
                    f_write.writelines([line])

    @staticmethod
    def copy_tqmodel_models_to_here():
        with open(TQMODEL_MODELS_PATH, 'r', encoding='utf-8') as f_read:
            with open(OLD_MODELS_FILE, 'w', encoding='utf-8') as f_write:
                for line in f_read:
                    if "from django.db import models" in line:
                        line = REPLACE
                        # line = line.replace("models.Model", "")
                    f_write.writelines([line])

    @classmethod
    def make_tqmain_models_from_db(cls, if_my_command=True):
        if not if_my_command:
            from django.core.management.commands import inspectdb
        else:
            import my_inspect as inspectdb

        inspectdb = inspectdb.Command(
            stdout=ModelsOutput
        )
        inspectdb.handle(**cls.options)
        ModelsOutput.close()


def get_models_from_file(model_file_name="new_models"):
    new_modules = import_module(model_file_name)
    new_modules_set = get_models_set(new_modules)
    return new_modules, new_modules_set


def main_tqmain():
    ModelsUtil.options['database'] = 'tqmain'

    ModelsUtil.copy_tqmain_models_to_here()
    ModelsUtil.make_tqmain_models_from_db()

    new_modules, new_modules_set = get_models_from_file("new_models")
    old_modules, old_modules_set = get_models_from_file("old_models")

    print(f"增加了的类： {new_modules_set - old_modules_set}")
    print(f"减少了的类： {old_modules_set - new_modules_set}")

    # compare common models about fields
    common_models_set = new_modules_set & old_modules_set
    for model in common_models_set:
        # print(model)
        if model.startswith("__"):
            continue
        if model in ('MagicMock', "models"):  # skip invalid class
            continue
        new_fields = get_fields_set(getattr(new_modules, model))
        old_fields = get_fields_set(getattr(old_modules, model))
        if old_fields != new_fields:
            print(f"{model}的字段增加了: {new_fields - old_fields}")
            print(f"{model}的字段减少了: {old_fields - new_fields}")


def main_tqmodel():
    ModelsUtil.options['database'] = 'tq_factor'

    ModelsUtil.copy_tqmodel_models_to_here()
    ModelsUtil.make_tqmain_models_from_db()

    new_modules, new_modules_set = get_models_from_file("new_models")
    old_modules, old_modules_set = get_models_from_file("old_models")

    print(f"增加了的类： {new_modules_set - old_modules_set}")
    print(f"减少了的类： {old_modules_set - new_modules_set}")

    # compare common models about fields
    common_models_set = new_modules_set & old_modules_set
    for model in common_models_set:
        # print(model)
        if model.startswith("__"):
            continue
        if model in ('MagicMock', "models"):  # skip invalid class
            continue
        new_fields = get_fields_set(getattr(new_modules, model))
        old_fields = get_fields_set(getattr(old_modules, model))
        if old_fields != new_fields:
            print(f"{model}的字段增加了: {new_fields - old_fields}")
            print(f"{model}的字段减少了: {old_fields - new_fields}")


if __name__ == '__main__':
    # copy old models to here
    # main_tqmain()
    main_tqmodel()
