maya_rig_core
=============

一个好用的绑定核心库

目录
----

-  `快速开始 <#快速开始>`__

   -  `安装 <#安装>`__
   -  `使用 <#使用>`__

-  `版权说明 <#版权说明>`__

快速开始
--------

安装
~~~~

注意下方的python是你的Python, 正常情况下可以直接通过python调用,
而Maya的python一般是C::raw-latex:`\Program`
Files:raw-latex:`\Autodesk`<Maya版本>:raw-latex:`\bin`:raw-latex:`\mayapy`.exe

.. code:: commandline

   python -m pip install maya-rig-core

在windows下maya的安装例子

注意:

1. 请将Maya路径替换为自己的。
2. 请使用cmd

.. code:: commandline

   "C:\Program Files\Autodesk\Maya2018\bin\mayapy.exe" -m pip install maya-rig-core

使用
~~~~

创建控制器与组
^^^^^^^^^^^^^^

.. code:: python

   # -*-coding:utf-8 -*-
   from __future__ import print_function, unicode_literals, division
   from rig_core.all import *

   ctx = Ctx()
   con = ctx.controller()
   grp = ctx.add_group_to_object(con)

创建名称空间上下文
^^^^^^^^^^^^^^^^^^

.. code:: python

   # -*-coding:utf-8 -*-
   from __future__ import print_function, unicode_literals, division
   from rig_core.all import *

   ctx = Ctx()
   with ctx.enter_new_name_space(prefix='prefix_'):
       con_list = ctx.controller()
   print('在这里你可以查看名称空间上下文结束之后的名称', con_list)

创建生成块上下文
^^^^^^^^^^^^^^^^

.. code:: python

   # -*-coding:utf-8 -*-
   from __future__ import print_function, unicode_literals, division
   from rig_core.all import *

   ctx = Ctx()
   # nodes 就是这个生成块记录的节点, 两个nodes都是.
   with ctx.enter_build_block(key=lambda nodes: print('从回调获得 生成块中创建了什么节点 >>  ', nodes)) as nodes:
       con_list = ctx.controller()
   print('从变量获得 生成块中创建了什么节点 >>  ', nodes)

使用Tag过滤节点
^^^^^^^^^^^^^^^

.. code:: python

   # -*-coding:utf-8 -*-
   from __future__ import print_function, unicode_literals, division
   from rig_core.all import *

   ctx = Ctx()

   # 进入一个新的Tag运行时(不进入其实也能跑,但是这里为了演示就进入了)
   with ctx.enter_new_tag_rt('test_tag_rt'):
       # 创建有one标签的控制器
       one_con_list = ctx.controller(tags=['one'])
       # 创建有two标签的控制器
       two_con_list = ctx.controller(tags=['two'])

       # 创建过滤器
       f = ctx.filter()
       # 过滤节点
       nodes = f.tag_equal('one')
       print('搜索到的节点', list(nodes))

进入一个新的根对象
^^^^^^^^^^^^^^^^^^

.. code:: python

   # -*-coding:utf-8 -*-
   from __future__ import print_function, unicode_literals, division
   from rig_core.all import *

   ctx = Ctx()

   root_con = ctx.controller()
   root_grp = ctx.add_group_to_object(root_con)

   with ctx.enter_new_root_object(root_con):
       child_con = ctx.controller()
       child_grp = ctx.add_group_to_object(child_con)

虚拟骨骼树的使用
^^^^^^^^^^^^^^^^

.. code:: python

   # -*-coding:utf-8 -*-
   from __future__ import print_function, unicode_literals, division
   from rig_core.all import *

   ctx = Ctx()

   # 创建控制器和组
   con_list = ctx.controller_list(tags=['test'], count=10)
   grp_list = ctx.add_group_to_object_list(con_list, tags=['test'])

   # 将控制器添加虚拟骨骼树下面
   ctx.root_joint.add_joint_chain_from_object_list(con_list)

   # 将虚拟骨骼树转化为实体骨骼
   create_real_joints_from_root(ctx.root_joint)

进入一个新的根虚拟关节
^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   # -*-coding:utf-8 -*-
   from __future__ import print_function, unicode_literals, division
   from rig_core.all import *

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
   create_real_joints_from_root(ctx.root_joint)

节点数据库功能
==============

.. code:: python

   # -*-coding:utf-8 -*-
   from __future__ import print_function, unicode_literals, division
   from rig_core.all import *

   ctx = Ctx()

   con = ctx.controller()
   grp = ctx.add_group_to_object(con)
   # 进入一个新的节点数据库运行时(不进入其实也能跑,但是这里为了演示就进入了)
   with ctx.enter_new_all_node_db_rt('test_attributes_name'):
       # 向控制器储存
       ctx.all_node_db_rt[con, 'test_key'] = 'test_all_db_rt_data'
       # 从控制器读取数据
       print('从控制器读取的数据', ctx.all_node_db_rt[con, 'test_key'])

版权说明
--------

该项目签署了Apache-2.0 授权许可，详情请参阅 LICENSE
