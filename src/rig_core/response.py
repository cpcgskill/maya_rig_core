# -*-coding:utf-8 -*-
u"""
:创建时间: 2022/6/13 21:02
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

这是个为构建器创建的模块
"""
from __future__ import unicode_literals, print_function, division


class Response(object):
    def __init__(self, **kwargs):
        self._kwarg = kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)

    def set(self, k, v):
        self._kwarg[k] = v
        setattr(self, k, v)
        return self

    def get(self, k):
        return self._kwarg[k]

    def __str__(self):
        return '{}{}'.format(self.__class__.__name__, self._kwarg)

    def __unicode__(self):
        return '{}{}'.format(self.__class__.__name__, self._kwarg)

    @staticmethod
    def from_locals(locals):
        return Response(**{k: v for k, v in locals.items() if k[0] != '_' and k not in {'self'}})
