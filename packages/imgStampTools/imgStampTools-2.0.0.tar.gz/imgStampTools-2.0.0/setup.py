#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "imgStampTools",      #这里是pip项目发布的名称
    version = "2.0.0",  #版本号，数值大的会优先被pip
    keywords = ["pip", "imgStampTools"],			# 关键字
    description = "lz's private utils.",	# 描述
    long_description = "lz's private utils.",
    license = "MIT Licence",		# 许可证

    url = "https://github.com/yazheng0307",     #项目相关文件地址，一般是github项目地址即可
    author = "lz",			# 作者
    author_email = "981638732@qq.com",

    package_data={'imgStampTools': ['font/*'], },

    packages = find_packages(),
    include_package_data = False,
    platforms = "any",
    install_requires = ["pillow"]          #这个项目依赖的第三方库
)
