# -*-coding:utf-8 -*-
"""
:创建时间: 2022/10/2 22:36
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division
from unittest import TestCase

class Test(TestCase):
    def test_create_quick_select_set(self):
        def test():
            from rig_core.ctx import Ctx

            ctx = Ctx()

            joint = ctx.create_dag_node('joint')

            ctx.create_quick_select_set([joint], name='test_quick_select_set')

        test()
