"""PyWebView 集成模块，用于将 Vue 3 前端嵌入到 Python GUI 窗口中"""

import os
import sys
import webview
import threading
from typing import Dict, Callable, Any, Optional
from .utils import get_static_dir

class WebViewApp:
    """WebView 应用类，用于管理 PyWebView 初始化和前后端通信"""
    
    def __init__(self,
                 static_dir: str,
                 entry_point: str = 'index.html',
                 title: str = 'Pvue WebView App',
                 size: tuple = (800, 600),
                 resizable: bool = True,
                 fullscreen: bool = False,
                 frameless: bool = False,
                 debug: bool = False):
        """
        初始化 WebView 应用
        
        Args:
            static_dir: 静态文件目录路径
            entry_point: 入口 HTML 文件
            title: 窗口标题
            size: 窗口大小，默认为 (800, 600)
            resizable: 是否允许调整窗口大小
            fullscreen: 是否全屏显示
            frameless: 是否无边框
            debug: 是否启用调试模式
        """
        self.static_dir = static_dir
        self.entry_point = entry_point
        self.title = title
        self.size = size
        self.resizable = resizable
        self.fullscreen = fullscreen
        self.frameless = frameless
        self.debug = debug
        
        # WebView 窗口实例
        self.window = None
        # 暴露的函数映射
        self.exposed_functions = {}
        # WebSocket URL
        self.ws_url = None
        
    def expose(self, name: Optional[str] = None) -> Callable:
        """
        暴露 Python 函数给前端调用
        
        Args:
            name: 前端调用时使用的函数名，默认为原函数名
            
        Returns:
            装饰器函数
        """
        def decorator(func):
            # 使用函数名作为默认名称
            func_name = name or func.__name__
            self.exposed_functions[func_name] = func
            return func
        return decorator
    
    def expose_function(self, name: str, func: Callable) -> None:
        """
        暴露 Python 函数给前端调用
        
        Args:
            name: 前端调用时使用的函数名
            func: 要暴露的 Python 函数
        """
        self.exposed_functions[name] = func
    
    def start(self, server_url: str) -> None:
        """
        启动 WebView 应用
        
        Args:
            server_url: 服务器 URL
        """
        # 创建 WebView 窗口
        self.window = webview.create_window(
            title=self.title,
            url=server_url,
            width=self.size[0],
            height=self.size[1],
            resizable=self.resizable,
            fullscreen=self.fullscreen,
            frameless=self.frameless,
            js_api=self.exposed_functions
        )
        
        # 启动 WebView 主循环（必须在主线程中运行）
        webview.start(debug=self.debug)
    
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
        if self.window:
            return self.window.evaluate_js(f"{js_function}({','.join(map(str, args))})")
        return None
    
    def close(self) -> None:
        """关闭 WebView 窗口"""
        if self.window:
            self.window.destroy()
            self.window = None

# 全局 WebView 应用实例
_global_webview_app = None

def get_webview_app() -> Optional[WebViewApp]:
    """获取全局 WebView 应用实例"""
    return _global_webview_app

def create_webview_app(
    static_dir: str,
    entry_point: str = 'index.html',
    title: str = 'Pvue WebView App',
    size: tuple = (800, 600),
    resizable: bool = True,
    fullscreen: bool = False,
    frameless: bool = False,
    debug: bool = False
) -> WebViewApp:
    """
    创建 WebView 应用实例
    
    Args:
        static_dir: 静态文件目录路径
        entry_point: 入口 HTML 文件
        title: 窗口标题
        size: 窗口大小，默认为 (800, 600)
        resizable: 是否允许调整窗口大小
        fullscreen: 是否全屏显示
        frameless: 是否无边框
        debug: 是否启用调试模式
        
    Returns:
        WebViewApp 实例
    """
    global _global_webview_app
    _global_webview_app = WebViewApp(
        static_dir=static_dir,
        entry_point=entry_point,
        title=title,
        size=size,
        resizable=resizable,
        fullscreen=fullscreen,
        frameless=frameless,
        debug=debug
    )
    return _global_webview_app
