# -*-coding:utf-8 -*-
u"""
:创建时间: 2022/6/13 21:03
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

"""
from __future__ import unicode_literals, print_function, division
import contextlib

import cpmel.cmds as cc
import maya.cmds as mc

if False:
    from typing import List, Tuple, AnyStr, Any, Callable, Generator, ContextManager


def _filter_node(nodes):
    for n in nodes:
        f = n.api2_m_fn_dependency_node()
        if not (f.isDefaultNode | f.isShared | f.isFromReferencedFile):
            if f.typeName not in {'ikRPsolver'}:
                yield n


@contextlib.contextmanager
def create_recorder(old_node_key=None, new_node_key=None):
    """
    记录器

    :type old_node_key: (List[cc.Node]) -> None
    :param old_node_key: 在上下文开始前执行
    :type new_node_key: (List[cc.Node]) -> None
    :param new_node_key: 在上下文结束后执行
    :return:
    """
    nodes = mc.ls('*', uid=True)
    if old_node_key is not None:
        old_node_key(cc.ls(nodes))
    yield
    new_nodes = mc.ls('*', uid=True)
    new_nodes = set(new_nodes) - set(nodes)
    if new_node_key is not None:
        new_nodes = _filter_node(cc.ls(new_nodes))
        new_node_key(list(new_nodes))


@contextlib.contextmanager
def enter_new_name_space(prefix='', suffix=''):
    """
    进入一个名称空间

    :type prefix: AnyStr
    :type suffix: AnyStr
    :return:
    """

    def enter(nodes):
        pass

    def exit_(nodes):
        for n in nodes:
            n.rename('{}{}{}'.format(prefix, n.node_name(), suffix))

    with create_recorder(enter, exit_):
        yield


@contextlib.contextmanager
def enter_build_block(key=None):
    """
    进入一个生成块

    :type key: None or (List[cc.Node]) -> None
    :param key: 成功记录了构建出来的节点时的回调
    :rtype: ContextManager[List[cc.Node]]
    :return: 一个 yield 生成出来的节点的列表的上下文管理器。
        ps: 这个生成出来的节点的列表要在上下文管理器退出时才会被填充
    """

    def enter(nodes):
        pass

    def exit_(nodes):
        build_complete_of_nodes.extend(nodes)
        if key is not None:
            key(nodes)

    build_complete_of_nodes = list()
    with create_recorder(enter, exit_):
        yield build_complete_of_nodes


__all__ = ['create_recorder', 'enter_new_name_space', 'enter_build_block']

if __name__ == "__main__":
    from rig_core.ctx import Ctx
    from maya_test_tools import question_open_maya_gui

    cc.file(f=True, new=True)
    ctx = Ctx()
    with enter_new_name_space('why'):
        cc.eval("""
        select -d;
        joint -p 2.406541 0 -5.622661 ;
        joint -p 1.434784 0 -0.347754 ;
        joint -e -zso -oj xyz -sao yup joint1;
        joint -p 5.493291 0 3.421071 ;
        joint -e -zso -oj xyz -sao yup joint2;
        joint -p 3.005031 0 8.218354 ;
        joint -e -zso -oj xyz -sao yup joint3;
        joint -p -0.587268 0 7.836342 ;
        joint -e -zso -oj xyz -sao yup joint4;
        select -d joint1 ;
        // 错误: 未选择有效项目。必须是关节、效应器或 NURBS 曲线。 // 
        select -r joint1 joint5 ;
        ikHandle;
        // 结果: ikHandle1 effector1 // 
        createNode "time";
        """)

    question_open_maya_gui()
