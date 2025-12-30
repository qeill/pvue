"""Pvue 工具函数模块"""

import os
import sys

def get_static_dir():
    """获取静态文件目录路径"""
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 向上两级目录，到达pvue包根目录
    parent_dir = os.path.dirname(os.path.dirname(current_dir))
    # 拼接静态文件目录路径
    static_dir = os.path.join(parent_dir, 'static')
    return static_dir
