# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   pytest_advance
# FileName:     test_example_1.py
# Author:      Jakiro
# Datetime:    2022/10/31 13:51
# Description:
# 命名规则  文件名小写字母+下划线，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------
import pytest


@pytest.mark.run(order=6)
def test_example_2():
    assert 1 == 1
