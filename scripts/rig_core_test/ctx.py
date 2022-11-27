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
        from rig_core.ctx import Ctx

        ctx = Ctx()

        joint = ctx.create_dag_node('joint')

        ctx.create_quick_select_set([joint], name='test_quick_select_set')

    def test_create_locator(self):
        from rig_core.ctx import Ctx

        ctx = Ctx()

        ctx.locator_list(count=12, tags=['test'])

        print(list(ctx.filter().tag_equal('test')))

    def test_tag_rt(self):
        from rig_core.all import Ctx

        ctx = Ctx()

        with ctx.add_base_tags_as_new_tag_rt(['test_add_base_tags_as_new_tag_rt']):
            test_locator = ctx.locator(tags=['test'])
        self.assertEqual(ctx.tag_rt.get_tags(test_locator), ['test', 'test_add_base_tags_as_new_tag_rt'])
