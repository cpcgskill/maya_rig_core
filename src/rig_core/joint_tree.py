# -*-coding:utf-8 -*-
u"""
:创建时间: 2022/3/23 4:20
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

一个逻辑上的关节树实现， 并不实际上存在。
这个逻辑关节将用于，绑定生成的最后生成蒙皮关节
"""
from __future__ import unicode_literals, print_function, division
import cpmel.cmds as cc

if False:
    from rig_core.ctx import Ctx


class Joint(object):
    def __init__(
            self,
            obj=None,
            point=None,
            create_only=False,
            name=None,
    ):
        if obj is not None:
            obj = cc.new_object(obj)
        self.obj = obj
        self.point = point
        self.name = name

        # 如果create_only属性为真将会仅创建，而不参与蒙皮
        self.create_only = create_only

        self.parent = None
        self.childs = list()

    def add_childs(self, *jins):
        for jin in jins:
            self.childs.append(jin)
            jin.parent = self
        return self

    def add_child_from_object(self, obj):
        return self.add_childs(Joint(obj=obj))

    def add_child_from_object_list(self, objs):
        for i in objs:
            self.add_child_from_object(i)
        return self

    def add_joint_chain(self, jins, are_end_joints_only_created=False):
        """
        添加关节链
        例如:
            输入: [jin1, jin2, jin3, jin4]
            输出:
                -self
                 -jin1
                  -jin2
                   -jin3
                    -jin4
        :param are_end_joints_only_created: 是否将末端关节设置为仅创建，而不参与蒙皮
        :param jins:
        :return:
        """
        root = self
        for jin in jins:
            root.add_childs(jin)
            root = jin
        root.create_only = are_end_joints_only_created
        return self

    def add_joint_chain_from_object_list(self, objs, extra_end_joint_of_point=None):
        jins = [Joint(obj=i) for i in objs]
        root = self
        for jin in jins:
            root.add_childs(jin)
            root = jin
        if extra_end_joint_of_point is not None:
            root.add_childs(Joint(point=extra_end_joint_of_point, create_only=True))
        return jins


def get_joint_output_name(root):
    if root.name is not None:
        return root.name
    name = None
    if isinstance(root.obj, cc.DagNode):
        name = root.obj.node_name() + '_skin_joint'
    if name is None and root.parent is not None:
        if len(root.childs) < 1:
            name = 'end_joint_of_' + get_joint_output_name(root.parent)
        else:
            name = 'child_joint_of_' + get_joint_output_name(root.parent)
    if name is None:
        if len(root.childs) < 1:
            name = 'end_joint'
        else:
            name = 'joint'
    return name


def _create_real_joints_from_root(ctx, root, parent, control_table):
    # name = 'joint'
    # if root.create_only:
    #     if parent is not None:
    #         name = parent.name() + '_end'
    # if isinstance(root.obj, cc.DagNode):
    #     name = root.obj.node_name() + '_skin_joint'
    # if root.name is not None:
    #     name = root.name
    name = get_joint_output_name(root)
    if parent is None:
        n = cc.createNode('joint', n=name)
    else:
        n = cc.createNode('joint', n=name, p=parent)
    if isinstance(root.obj, cc.DagNode):
        n.translation = root.obj.translation
        n.rotation = root.obj.rotation
        n['jointOrient'] = n.get_rotation(False)
        n.set_rotation((0, 0, 0), False)
        n.scale = root.obj.scale
        ctx.tag_rt.add_tags(n, *ctx.tag_rt.get_tags(root.obj))
        control_table.append((root.obj, n))
    elif root.point is not None:
        n.set_translation(root.point, ws=True)
    ctx.tag_rt.add_tags(n, 'skin_joint')
    for i in root.childs:
        _create_real_joints_from_root(ctx, i, n, control_table)


def create_real_joints_from_root(ctx, root, parent=None):
    """

    :type ctx: Ctx
    :type root: Joint
    :param parent:
    :return:
    """
    control_table = list()
    for i in root.childs:
        _create_real_joints_from_root(ctx, i, parent, control_table)
    for con, jin in control_table:
        cc.parentConstraint(con, jin)
        cc.scaleConstraint(con, jin)
