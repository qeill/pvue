"""Eel 集成模块，用于将 Vue 3 前端嵌入到 Python 桌面窗口中"""

import os
import sys
import eel
from typing import Dict, Callable, Any, Optional

class EelApp:
    """Eel 应用类，用于管理 Eel 初始化和前后端通信"""
    
    def __init__(self,
                 static_dir: str,
                 entry_point: str = 'index.html',
                 size: tuple = (800, 600),
                 app_mode: str = 'chrome',
                 port: int = 0,
                 dev_mode: bool = False):
        """
        初始化 Eel 应用
        
        Args:
            static_dir: 静态文件目录路径
            entry_point: 入口 HTML 文件
            size: 窗口大小，默认为 (800, 600)
            app_mode: 浏览器模式，可选值：chrome, edge, electron, kiosk, default
            port: 服务器端口，0 表示随机端口
            dev_mode: 是否启用开发模式
        """
        self.static_dir = static_dir
        self.entry_point = entry_point
        self.size = size
        self.app_mode = app_mode
        self.port = port
        self.dev_mode = dev_mode
        self.functions = {}
        
    def expose(self, name: Optional[str] = None) -> Callable:
        """
        暴露 Python 函数给前端调用
        
        Args:
            name: 前端调用时使用的函数名，默认为原函数名
            
        Returns:
            装饰器函数
        """
        return eel.expose(name)
    
    def expose_function(self, name: str, func: Callable) -> None:
        """
        暴露 Python 函数给前端调用
        
        Args:
            name: 前端调用时使用的函数名
            func: 要暴露的 Python 函数
        """
        self.functions[name] = func
        # 使用装饰器方式暴露函数
        exposed_func = eel.expose(name)(func)
        return exposed_func
    
    def init(self) -> None:
        """初始化 Eel"""
        # 初始化 Eel
        eel.init(self.static_dir)
        
        # 暴露内置函数
        self._expose_builtin_functions()
    
    def _expose_builtin_functions(self) -> None:
        """暴露内置函数给前端"""
        @self.expose('get_app_info')
        def get_app_info():
            return {
                'name': 'Pvue Eel App',
                'version': '0.1.0',
                'mode': self.app_mode,
                'dev_mode': self.dev_mode
            }
    
    def start(self, **kwargs) -> None:
        """
        启动 Eel 应用
        
        Args:
            **kwargs: 传递给 eel.start 的额外参数
        """
        # 初始化 Eel
        self.init()
        
        # 启动 Eel 应用
        eel.start(
            self.entry_point,
            size=self.size,
            mode=self.app_mode,
            port=self.port,
            **kwargs
        )
    
    def call(self, js_function: str, *args, **kwargs) -> Any:
        """
        调用前端 JavaScript 函数
        
        Args:
            js_function: JavaScript 函数名
            *args: 传递给 JavaScript 函数的参数
            **kwargs: 额外参数
            
        Returns:
            JavaScript 函数的返回值
        """
        return eel.eval_js(f"{js_function}({','.join(map(str, args))})")
    
    def add_js_function(self, name: str, func: Callable) -> None:
        """
        添加 JavaScript 函数到前端
        
        Args:
            name: JavaScript 函数名
            func: 函数实现
        """
        eel.add_js_function(name, func)

# 全局 Eel 应用实例
_global_eel_app = None

def get_eel_app() -> Optional[EelApp]:
    """获取全局 Eel 应用实例"""
    return _global_eel_app

def create_eel_app(
    static_dir: str,
    entry_point: str = 'index.html',
    size: tuple = (800, 600),
    app_mode: str = 'chrome',
    port: int = 0,
    dev_mode: bool = False
) -> EelApp:
    """
    创建 Eel 应用实例
    
    Args:
        static_dir: 静态文件目录路径
        entry_point: 入口 HTML 文件
        size: 窗口大小，默认为 (800, 600)
        app_mode: 浏览器模式
        port: 服务器端口
        dev_mode: 是否启用开发模式
        
    Returns:
        EelApp 实例
    """
    global _global_eel_app
    _global_eel_app = EelApp(
        static_dir=static_dir,
        entry_point=entry_point,
        size=size,
        app_mode=app_mode,
        port=port,
        dev_mode=dev_mode
    )
    return _global_eel_app
