#!/usr/bin/python
# -*-coding:utf-8 -*-
from __future__ import unicode_literals, print_function
import setuptools

lib_name = 'maya_rig_core'

author = 'cpcgskill',
author_email = 'cpcgskill@outlook.com'

version = '0.1.2'

description = '一个好用的绑定核心库'
with open("README.md", "rb") as f:
    long_description = f.read().decode(encoding='utf-8')

project_homepage = 'https://github.com/cpcgskill/maya_rig_core'
project_urls = {
    'Bug Tracker': 'https://github.com/cpcgskill/maya_rig_core/issues',
}
license = 'Apache Software License (Apache 2.0)'

python_requires = '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*'
install_requires = [
    'maya-test-tools==0.1.0',
    'cpmel==3.4.1',
]

setuptools.setup(
    name=lib_name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=project_homepage,
    project_urls=project_urls,
    license=license,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    package_dir={"": "src"},
    # # 使用自动搜索
    # packages=setuptools.find_packages(where="src"),
    packages=['rig_core'],
    python_requires=python_requires,
    # 指定依赖
    install_requires=install_requires,
)
