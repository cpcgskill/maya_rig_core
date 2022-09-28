# -*-coding:utf-8 -*-
u"""
:创建时间: 2022/3/22 22:53
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

"""
from __future__ import unicode_literals, print_function

import json

import cpmel.cmds as cc
from cpmel.exc import *


def attribute_exists(node, attr):
    try:
        return node.attr(attr)
    except CPMelException:
        return None


class TagRt(object):
    def __init__(self, tag_attr="tag_runtime"):
        self.tag_attr = tag_attr
        self.cache = dict()

    def get_tags(self, obj):
        cache = self.cache.get(hash(obj))
        if cache is not None:
            return cache
        attr = attribute_exists(obj, self.tag_attr)
        if attr:
            tags = json.loads(cc.getAttr(attr))
        else:
            tags = []
        return tags

    def set_tags(self, obj, tags):
        attr = attribute_exists(obj, self.tag_attr)
        if attr is None:
            cc.addAttr(obj, ln=self.tag_attr, dt="string")
        attr = attribute_exists(obj, self.tag_attr)
        tags = list(set(tags))
        cc.setAttr(attr, json.dumps(tags), type="string")
        self.cache[hash(obj)] = tags
        return self

    def add_tags(self, obj, *new_tags):
        tags = self.get_tags(obj)
        for i in new_tags:
            tags.append(i)
        self.set_tags(obj, tags)
        return self

    def add_tag_to_objs(self, tag, *objs):
        for o in objs:
            self.add_tags(o, tag)
        return self
