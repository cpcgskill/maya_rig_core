# -*-coding:utf-8 -*-
u"""
:创建时间: 2022/3/22 6:00
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

"""
from __future__ import unicode_literals, print_function
import contextlib

import cpmel.cmds as cc
# import rig_core.std_func as rig_std_func
import rig_core.tag as tag
import rig_core.db as db
from rig_core.filter import Filter
from rig_core.joint_tree import Joint
import rig_core.contextmanager as rig_contextmanager

if False:
    from typing import List, Tuple, AnyStr, Any, Callable, Generator, ContextManager


class Ctx(object):
    """绑定上下文类"""

    def __init__(self):
        self.data = dict()
        self.feature = set()
        self._nodes = list()
        self._tag_rt = tag.TagRt()
        self._all_node_db_rt = db.AllNodeDbRt()
        self._root_object = None
        self._root_joint = Joint(None)

    # 数据系统
    def set(self, k, v):
        self.data[k] = v
        return self

    def get(self, k, default=None):
        return self.data.get(k, default)

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, item, value):
        self.data[item] = value

    def ass_data(self, k):
        return self.data[k]

    # 特性系统 (默认支持特性: [invisible_locator: 启用这个特性将阻止定位器创建形状节点，在发布时启用它可以避免隐藏定位器的工作])

    def on_feature(self, n):
        self.feature.add(n)
        return self

    def off_feature(self, n):
        if n in self.feature:
            self.feature.remove(n)
        return self

    # 过滤器
    def filter(self, nodes=None):
        return Filter(self, nodes)

    # 这个方法没有什么用
    def add_nodes(self, *nodes):
        for i in nodes:
            self._nodes.append(i)
        return self

    # 节点创建编辑等
    def create_node(self, type_, name=None):
        node = cc.createNode(type_)
        if name is not None:
            node.rename(name)
        self._nodes.append(node)
        return node

    def create_dag_node(self, type_, name=None, parent=None):
        n = self.create_node(type_, name)  # type: cc.DagNode
        if parent is None:
            if self.root_object is not None:
                n.parent = self.root_object
        else:
            n.parent = parent
        return n

    def create_node_list(self, t_n, count):
        return [self.create_node(t_n) for _ in range(count)]

    def delete_node(self, *nodes):
        new_nodes = []
        for node in nodes:
            if isinstance(node, (list, tuple, set)):
                for n in node:
                    new_nodes.append(n)
            else:
                new_nodes.append(node)
        cc.delete(new_nodes)
        return self

    @staticmethod
    def add_attribute(node, name, default=None, min=None, max=None, typ='float', key=True):
        """
        为节点添加属性

        :type node: cc.Node
        :type name: AnyStr
        :type default: float
        :type min: float
        :type max: float
        :type typ: AnyStr
        :type key: bool
        :rtype: cc.Attr
        """
        type_type_map = {
            'float': "double",
            'float1': "double",
            'float2': "double2",
            'float3': "double3",
        }
        node = cc.new_object(node)
        cc.addAttr(
            node,
            shortName=name, longName=name,
            at=type_type_map[typ]
        )

        attr = node.attr(name)
        if default is not None:
            cc.addAttr(attr, e=True, defaultValue=default)
            attr.set_value(default)
        if min is not None:
            cc.addAttr(attr, e=True, minValue=min)
        if max is not None:
            cc.addAttr(attr, e=True, maxValue=max)

        if key:
            cc.setAttr(attr, k=True)

        return attr

    @classmethod
    def need_attribute(cls, node, name, default=None, min=None, max=None, typ='float', key=True):
        """
        需要一个属性， 如果不存在则创建

        :type node: cc.Node
        :type name: AnyStr
        :type default: float
        :type min: float
        :type max: float
        :type typ: AnyStr
        :type key: bool
        :rtype: cc.Attr
        """
        node = cc.new_object(node)
        if cc.objExists('{}.{}'.format(node.name(), name)):
            return node.attr(name)
        else:
            return cls.add_attribute(node, name, default, min, max, typ, key)

    def locator(self, n=None):
        """

        :type n: AnyStr
        :rtype: cc.Transform
        """
        if n is None:
            n = 'space_locator'
        if 'invisible_locator' in self.feature:
            loc = self.create_node('transform')
        else:
            loc = cc.spaceLocator()[0]
        loc.rename(n)
        if self.root_object is not None:
            loc.parent = self.root_object
        return loc

    def locator_list(self, count=None, n=None):
        """

        :type count: int
        :type n: AnyStr
        :rtype: List[cc.Transform]
        """
        if n is None:
            n = 'space_locator'
        return [self.locator(n="{}{}".format(n, i)) for i in range(count)]

    def controller(self, tags=[], point=None):
        """
        :type tags: List[AnyStr]
        :param point: 控制器的位置
        :rtype: cc.Transform
        """
        if tags is None:
            tags = []
        con = cc.circle(nr=(1, 0, 0), sw=360, r=0.5, d=3, s=8, ch=False, n='controller')[0]
        self.add_tags(con, "controller", *tags)
        self.add_nodes(con)
        if point is not None:
            cc.xform(con, ws=True, t=point)
        if self.root_object is not None:
            con.parent = self.root_object
        if 'automatic_view_refresh' in self.feature:
            cc.refresh()
        return con

    def fk_controller(self, tags=[], point=None):
        return self.controller(["fk"] + tags, point)

    def ik_controller(self, tags=[], point=None):
        return self.controller(["ik"] + tags, point)

    def controller_list(self, tags=[], count=1, point_list=None):
        if point_list is None:
            point_list = [(0, 0, 0) for _ in range(count)]
        cons = [self.controller(tags, p) for _, p in zip(range(count), point_list)]
        for id_, c in enumerate(cons):
            self.all_node_db_rt.set_data(c, 'controller_id', id_)
        return cons

    def fk_controller_list(self, tags=[], count=1, point_list=None):
        return self.controller_list(["fk"] + tags, count, point_list)

    def ik_controller_list(self, tags=[], count=1, point_list=None):
        return self.controller_list(["ik"] + tags, count, point_list)

    def add_child_object_to_object(self, obj, tags=[], suffix='_of_child_object', name=None, point=None):
        n = self.create_node('transform')
        n.matrix = obj.matrix
        n.parent = obj

        n.rename(obj.node_name() + suffix)

        if name is not None:
            n.rename(name)
        if point is not None:
            n.set_translation(point, ws=True)

        self.add_tags(n, *tags)
        self.add_nodes(n)
        return n

    def add_group_to_object(self, obj, tags=[], suffix='_group'):
        n = self.create_node('transform')
        n.matrix = obj.matrix
        if obj.parent is not None:
            n.parent = obj.parent

        obj.parent = n

        n.rename(obj.node_name() + suffix)

        self.add_tags(n, *tags)
        self.add_nodes(n)
        return n

    def add_group_to_object_list(self, objs, tags=[], suffix='_group'):
        return [self.add_group_to_object(o, tags, suffix) for o in objs]

    @property
    def nodes(self):
        return self._nodes

    @property
    def tag_rt(self):
        return self._tag_rt

    @tag_rt.setter
    def tag_rt(self, rt):
        if isinstance(rt, tag.TagRt):
            self._tag_rt = rt
        else:
            raise TypeError

    # tag_rt = property(get_tag_rt, set_tag_rt)
    def add_tags(self, obj, *new_tags):
        """TagRt在Ctx上的快捷方法"""
        return self._tag_rt.add_tags(obj, *new_tags)

    @contextlib.contextmanager
    def enter_new_tag_rt(self, tag_attr):
        """进入新的tag_rt， 新的与旧的互相隔离"""
        old_rt = self.tag_rt
        self.tag_rt = tag.TagRt('_'.join([tag_attr, old_rt.tag_attr]))
        yield
        self.tag_rt = old_rt

    @property
    def all_node_db_rt(self):
        return self._all_node_db_rt

    @all_node_db_rt.setter
    def all_node_db_rt(self, rt):
        if isinstance(rt, db.AllNodeDbRt):
            self._all_node_db_rt = rt
        else:
            raise TypeError

    @contextlib.contextmanager
    def enter_new_all_node_db_rt(self, db_runtime_attribute):
        """进入新的all_node_db_rt， 新的与旧的互相隔离"""
        old_rt = self.all_node_db_rt
        self.all_node_db_rt = db.AllNodeDbRt('_'.join([db_runtime_attribute, old_rt.db_runtime_attribute]))
        yield self
        self.all_node_db_rt = old_rt

    @property
    def root_object(self):
        """
        :rtype: cc.DagNode or None
        """
        return self._root_object

    @root_object.setter
    def root_object(self, value):
        if cc.objExists(value):
            value = cc.new_object(value)
            self._root_object = value

    @root_object.deleter
    def root_object(self):
        self._root_object = None

    @contextlib.contextmanager
    def enter_new_root_object(self, new):
        """切换到新的根对象"""
        new = None if new is None else cc.new_object(new)
        old = self._root_object
        self._root_object = new
        yield new
        self._root_object = old

    @contextlib.contextmanager
    def create_group_as_new_root_object(self, name=None):
        if name is None:
            name = 'group'
        n = self.create_node('transform', name)
        if self.root_object is not None:
            n.parent = self.root_object
            n.matrix = self.root_object.matrix
        with self.enter_new_root_object(n):
            yield n

    def add_object_to_root_object(self, obj):
        obj = cc.new_object(obj)
        if self.root_object is None:
            if obj.parent is not None:
                cc.parent(obj, w=True)
        else:
            if obj.parent != self.root_object:
                cc.parent(obj, self.root_object)
        return self

    @property
    def root_joint(self):
        """:rtype: Joint"""
        return self._root_joint

    @root_joint.setter
    def root_joint(self, jin):
        """:type jin: Joint"""
        self._root_joint = jin

    @contextlib.contextmanager
    def enter_new_root_joint(self, new_root_joint):
        """切换到新的根关节， 新的是旧的子关节"""
        old_root_joint = self.root_joint
        # old_root_joint.add_childs(new_root_joint)
        self.root_joint = new_root_joint
        yield
        self.root_joint = old_root_joint

    @contextlib.contextmanager
    def create_joint_as_new_root_joint(self, *args, **kwargs):
        new_root_joint = Joint(*args, **kwargs)
        with self.enter_new_root_joint(new_root_joint):
            yield new_root_joint

    @contextlib.contextmanager
    def create_child_joint_as_new_root_joint(self, *args, **kwargs):
        new_root_joint = Joint(*args, **kwargs)
        self.root_joint.add_childs(new_root_joint)
        with self.enter_new_root_joint(new_root_joint):
            yield new_root_joint

    @contextlib.contextmanager
    def enter_new_name_space(self, prefix='', suffix=''):
        """
        进入一个名称空间

        :type prefix: AnyStr
        :type suffix: AnyStr
        :return:
        """
        with rig_contextmanager.enter_new_name_space(prefix, suffix):
            yield

    @contextlib.contextmanager
    def enter_build_block(self, key=None):
        """
        进入一个生成块

        :type key: None or (List[cc.Node]) -> None
        :param key: 成功记录了构建出来的节点时的回调
        :rtype: ContextManager[List[cc.Node]]
        :return: 一个 yield 生成出来的节点的列表的上下文管理器。
            ps: 这个生成出来的节点的列表要在上下文管理器退出时才会被填充
        """
        with rig_contextmanager.enter_build_block(key) as wing_build_complete_of_nodes:
            yield wing_build_complete_of_nodes

    def create_quick_select_set(self, objs, name='quick_select_set'):
        node = cc.sets(*objs, n=name)
        self.add_nodes(node)
        return node


__all__ = ['Ctx']
