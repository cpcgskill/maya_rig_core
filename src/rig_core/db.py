# -*-coding:utf-8 -*-
"""
:创建时间: 2022/8/22 3:57
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division

import json

import cpmel.cmds as cc
from cpmel.exc import *

if False:
    from typing import List, Tuple, AnyStr, Any

__all__ = ['AllNodeDbRt', 'NodeDbRt']


def _attribute_exists(node, attr):
    try:
        return node.attr(attr)
    except CPMelException:
        return None


class AllNodeDbRt(object):
    """对于所有节点的数据库实现"""
    __slots__ = ('db_runtime_attribute', '__cache')

    def __init__(self, db_runtime_attribute="db_runtime"):
        """
        :type db_runtime_attribute: AnyStr
        """
        self.db_runtime_attribute = db_runtime_attribute
        self.__cache = dict()

    def __read_data(self, obj):
        """
        :type obj: cc.Node
        :rtype: dict
        """
        obj = cc.new_object(obj)
        cache = self.__cache.get(hash(obj))
        if cache is not None:
            return cache
        attr = _attribute_exists(obj, self.db_runtime_attribute)
        if attr is None:
            return dict()
        return json.loads(cc.getAttr(attr))

    def __save_data(self, obj, data):
        """
        :type obj: cc.Node
        :type data: Any
        :rtype: DbRt
        """
        obj = cc.new_object(obj)
        attr = _attribute_exists(obj, self.db_runtime_attribute)
        if attr is None:
            cc.addAttr(obj, ln=self.db_runtime_attribute, dt="string")
            attr = _attribute_exists(obj, self.db_runtime_attribute)
        cc.setAttr(attr, json.dumps(data), type="string")
        self.__cache[hash(obj)] = data
        return self

    def get_data(self, obj, key, default=None):
        """
        :type obj: cc.Node
        :type key: AnyStr
        :type default: Any
        :rtype: Any
        """
        return self.__read_data(obj).get(key, default)

    def keys(self, obj):
        """
        :type obj: cc.Node
        :rtype: List[AnyStr]
        """
        return self.__read_data(obj).keys()

    def values(self, obj):
        """
        :type obj: cc.Node
        :rtype: List[Any]
        """
        return self.__read_data(obj).values()

    def items(self, obj):
        """
        :type obj: cc.Node
        :rtype: List[Tuple[AnyStr, Any]]
        """
        return self.__read_data(obj).items()

    def set_data(self, obj, key, value):
        """
        :type obj: cc.Node
        :type key: AnyStr
        :type value: Any
        :rtype: DbRt
        """
        data = self.__read_data(obj)
        data[key] = value
        self.__save_data(obj, data)
        return self

    def __setitem__(self, key, value):
        """
        :type key: Tuple[cc.Node, AnyStr]
        :type value: Any
        :rtype: DbRt
        """
        (obj, key) = key
        return self.set_data(obj, key, value)

    def __getitem__(self, key):
        """
        :type key: Tuple[cc.Node, AnyStr]
        :rtype: Any
        """
        (obj, key) = key
        return self.__read_data(obj)[key]

    def create_node_db_rt(self, node):
        """
        :type node: cc.Node
        :type: NodeDbRt
        """
        return NodeDbRt(node, self.db_runtime_attribute)


class NodeDbRt(object):
    """对单节点的数据库实现"""
    __slots__ = ('obj', 'db_rt')

    def __init__(self, obj, db_runtime_attribute="db_runtime"):
        """
        :type obj: cc.Node
        :type db_runtime_attribute: AnyStr
        """
        self.obj = obj
        self.db_rt = AllNodeDbRt(db_runtime_attribute)

    def get(self, key, default=None):
        """
        :type key: AnyStr
        :type default: Any
        :rtype: Any
        """
        return self.db_rt.get_data(self.obj, key, default)

    def keys(self):
        """
        :rtype: List[AnyStr]
        """
        return self.db_rt.keys(self.obj)

    def values(self):
        """
        :rtype: List[Any]
        """
        return self.db_rt.values(self.obj)

    def items(self):
        """
        :rtype: List[Tuple[AnyStr, Any]]
        """
        return self.db_rt.items(self.obj)

    def set(self, key, value):
        """
        :type key: AnyStr
        :type value: Any
        :rtype: NodeDbRt
        """
        self.db_rt.set_data(self.obj, key, value)
        return self

    def __getitem__(self, key):
        """

        :type key: AnyStr
        :rtype: Any
        """
        return self.db_rt[self.obj, key]

    def __setitem__(self, key, value):
        """

        :type key: AnyStr
        :type value: Any
        :rtype: NodeDbRt
        """
        self.db_rt[self.obj, key] = value
        return self


if __name__ == '__main__':
    print('test AllNodeDbRt')
    all_db_rt = AllNodeDbRt()
    test_node = cc.createNode('transform')
    print('test __setitem__')
    all_db_rt[test_node, 'test_key'] = 'test_all_db_rt_data'
    print('test __getitem__', all_db_rt[test_node, 'test_key'])
    print('test keys', all_db_rt.keys(test_node))
    print('test values', all_db_rt.values(test_node))
    print('test items', all_db_rt.items(test_node))

    print('test NodeDbRt')
    db_rt = all_db_rt.create_node_db_rt(test_node)
    print('test __setitem__')
    db_rt['test_key'] = 'test_db_rt_data'
    print('test __getitem__', db_rt['test_key'])
    print('test keys', db_rt.keys())
    print('test values', db_rt.values())
    print('test items', db_rt.items())
