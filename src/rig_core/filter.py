# -*-coding:utf-8 -*-
u"""
:创建时间: 2022/4/7 14:38
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

"""
from __future__ import unicode_literals, print_function, division
import cpmel.cmds as cc


class Filter(object):
    def __init__(self, ctx, objs=None):
        self.ctx = ctx
        self.tag_rt = ctx.tag_rt
        self.objs = cc.ls('*') if objs is None else objs

    def to_set(self):
        return set(self)

    def __iter__(self):
        for obj in self.objs:
            if obj.ref.is_valid():
                if len(self.tag_rt.get_tags(obj)):
                    yield obj

    def filter(self, key):
        objs = set()
        for obj in self:
            if key(obj):
                objs.add(obj)
        return Filter(self, objs)

    def tag_equal(self, *s):
        s = set(s)
        return self.filter(key=lambda obj: s <= set(self.tag_rt.get_tags(obj)))

    def tag_not_equal(self, *s):
        s = set(s)
        return self.filter(key=lambda obj: not s <= set(self.tag_rt.get_tags(obj)))

    def __and__(self, other):
        return Filter(self.ctx, self.to_set() & other.to_set())

    def __or__(self, other):
        return Filter(self.ctx, self.to_set() | other.to_set())
