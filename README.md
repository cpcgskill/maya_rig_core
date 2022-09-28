# maya_rig_core

一个好用的绑定核心库

## 目录

- [快速开始](#快速开始)
    * [安装](#安装)
    * [使用](#使用)
- [版权说明](#版权说明)

## 快速开始

### 安装

注意下方的python是你的Python, 正常情况下可以直接通过python调用, 而Maya的python一般是C:\Program
Files\Autodesk\<Maya版本>\bin\mayapy.exe

```commandline
python -m pip install maya-rig-core
```

在windows下maya的安装例子

注意:

1. 请将Maya路径替换为自己的。
2. 请使用cmd

```commandline
"C:\Program Files\Autodesk\Maya2018\bin\mayapy.exe" -m pip install cpmel
```

### 使用

#### 创建控制器与组

```python
from rig_core.all import *

ctx = Ctx()
con = ctx.controller()
grp = ctx.add_group_to_object(con)
```

#### 创建名称空间上下文

```python
from rig_core.all import *

ctx = Ctx()
with ctx.enter_new_name_space(prefix='prefix_')
    '''your code'''
```

## 版权说明

该项目签署了Apache-2.0 授权许可，详情请参阅 LICENSE




