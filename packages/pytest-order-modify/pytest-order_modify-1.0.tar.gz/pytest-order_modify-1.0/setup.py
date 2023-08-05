# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   pytest-order_modify_plugin
# FileName:     setup.py
# Author:      Jakiro
# Datetime:    2022/11/3 16:34
# Description:
# 命名规则  文件名小写字母+下划线，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------

from setuptools import setup, find_packages

setup(
    name='pytest-order_modify',
    author='Jakilo',
    version='1.0',
    url='https://github.com/Jakilo1996/PytestTestOrderModify',
    python_requires=' >=3',
    description='新增run_marker 来自定义用例的执行顺序',
    classifiers=['Framework :: Pytest'],
    py_modules=['pytest_order_modify'],  # 需要包含插件函数所在的文件内容
    packages=find_packages(),
    install_require=['pytest'],
    entry_points={
        # pytest11为官方定义的固定入口点，用于发现插件
        'pytest11': [
            'pytest-order_modify = pytest_order_modify',
        ],
    },
)