# encoding: utf-8
# @Time : 2023/10/30 17:26
# @Auther : ISLEY
# @File : pathutil.py
# @DESC : 文件路径相关工具
import os

"""
    获取项目根目录的绝对路径
    @DESC:  该方法通过获取脚本绝对路径间接获取项目根目录
        其中../.. 表示向上移动两级目录
        因此本方法不能通用在任何项目中 , 还需手动修改
"""


def get_root_path():
    # 获取当前脚本的绝对路径
    script_path = os.path.abspath(__file__)

    # 获取当前脚本所在目录的绝对路径
    script_directory = os.path.dirname(script_path)

    # 获取根目录的绝对路径
    root_directory = os.path.abspath(os.path.join(script_directory, '../..'))
    # print(root_directory)
    return root_directory


"""
    输入相对根目录的相对路径 返回绝对路径
    @relative_path 相对根目录的路径
    @return 绝对路径
"""


def get_abs_path(relative_path):
    return os.path.join(get_root_path(), relative_path)
