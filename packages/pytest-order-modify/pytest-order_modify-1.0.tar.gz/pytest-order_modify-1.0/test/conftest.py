# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   pytest-order_modify_plugin
# FileName:     conftest.py
# Author:      Jakiro
# Datetime:    2022/11/3 16:35
# Description:
# 命名规则  文件名小写字母+下划线，类名大驼峰，方法、变量名小写字母+下划线连接
# 常量大写，变量和常量用名词、方法用动词
# -----------------------------------------------------------------------------------

import operator

import pytest

orders_map = {
    'first': 0,
    'second': 1,
    'third': 2,
    'fourth': 3,
    'fifth': 4,
    'sixth': 5,
    'seventh': 6,
    'eighth': 7,
    'last': -1,
    'second_to_last': -2,
    'third_to_last': -3,
    'fourth_to_last': -4,
    'fifth_to_last': -5,
    'sixth_to_last': -6,
    'seventh_to_last': -7,
    'eighth_to_last': -8,
}


def pytest_configure(config):
    """Register the "run" marker."""

    config_line = (
        'run: specify ordering information for when tests should run '
        'in relation to one another. Provided by pytest-ordering. '
        'See also: http://pytest-ordering.readthedocs.org/'
    )
    # 将 run这个marker注册到marker 列表中
    config.addinivalue_line('markers', config_line)


def pytest_collection_modifyitems(session, config, items):
    print(f'items_type{items}')
    # 声明一个空的字典，用于以 order为key 存储每级order对应的item列表
    grouped_items = {}

    for item in items:
        print(f'item:{item}')
        for mark_name, order in orders_map.items():
            # 返回与mark_name匹配的第一个标记，从最近的级别(例如函数)到更远的级别(例如模块级别)
            mark = item.get_closest_marker(mark_name)

            if mark:
                # 向节点添加一个标记对象
                item.add_marker(pytest.mark.run(order=order))
                break
        # 获取标记
        mark = item.get_closest_marker('run')
        print('mark', mark)
        if mark:
            # 通过标记获取 标记的关键字参数 order的value
            order = mark.kwargs.get('order')
        else:
            order = None
        #  在grouped_items中设置对应1、2、3。。。。级别的run_mark中对应的测试item，如果没有order，则将item放到 None对应list中
        # 最终形式为 {x:[item_x,item_x],x:[item1,item2],x:[item_x,item_x],...,None:[item,...]}
        grouped_items.setdefault(order, []).append(item)
    print('grouped_items\n', grouped_items)

    # 将不需要排序key值为None的item提取出来，如果没有None 提取一个空列表
    unordered_items = [grouped_items.pop(None, [])]

    # 将需要排序的grouped_items 中key大于等于0的item按 key的由小到大顺序排序 ；元祖推导式的内容为 提取key大于等于0的
    start_list = sorted((i for i in grouped_items.items() if i[0] >= 0),
                        key=operator.itemgetter(0))
    # 将需要排序的grouped_items 中key小于0的item按 key的由小到大顺序排序 ；元祖推导式的内容为 提取key小于0的
    end_list = sorted((i for i in grouped_items.items() if i[0] < 0),
                      key=operator.itemgetter(0))
    # 最终结果为 [[1,[item_x,item_x]],[2,[item_x,item_x]]]

    # 对用例的执行顺序进行排序
    #  声明一个列表 存储排序后的内容  最终格式为 [[item1,item2],[item1,item2],[item1,item2]]
    sorted_items = []
    # 先将有run mark标记的 order大于0的排序，处理先执行的用例
    sorted_items.extend([i[1] for i in start_list])
    # 按默认顺序添加未被标记的用例
    sorted_items.extend(unordered_items)
    # 最后排序需要倒数执行的用例，由order value由小到大排序
    sorted_items.extend([i[1] for i in end_list])

    # 最终格式为 [[item1,item2],[item1,item2],[item1,item2]]

    # 去掉sorted_items中的列表套，列表格式，将其变为一个纯列表
    # 格式为 [item1,item2,item1,item2,item1,item2]
    # items[:]
    items[:] = [item for sublist in sorted_items for item in sublist]
    print(f'items{items}')

# pytest_plugins = ['pytester']
