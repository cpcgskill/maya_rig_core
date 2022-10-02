# -*-coding:utf-8 -*-
"""
:创建时间: 2022/10/2 22:51
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
    def test_create_real_joints_from_root(self):
        import cpmel.cmds as cc
        from rig_core.all import Ctx, create_real_joints_from_root

        ctx = Ctx()

        root_con = ctx.controller()
        root_grp = ctx.add_group_to_object(root_con)

        # 进入一个新的根虚拟关节
        with ctx.create_child_joint_as_new_root_joint(obj=root_con):
            # 创建控制器和组
            con_list = ctx.controller_list(tags=['test'], count=10)
            grp_list = ctx.add_group_to_object_list(con_list, tags=['test'])

            # 将控制器添加虚拟骨骼树下面
            ctx.root_joint.add_child_from_object_list(con_list)

        # 将虚拟骨骼树转化为实体骨骼
        with ctx.enter_build_block() as skin_joint_list:
            create_real_joints_from_root(ctx, ctx.root_joint)
        skin_joint_list = cc.ls(skin_joint_list, type='joint')
        print(skin_joint_list)
        print('one joint tags', ctx.tag_rt.get_tags(skin_joint_list[0]))
