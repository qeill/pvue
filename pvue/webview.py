"""PyWebView 集成模块，用于将 Vue 3 前端嵌入到 Python GUI 窗口中"""

import os
import sys
import threading
from typing import Dict, Callable, Any, Optional
from .utils import get_static_dir

# 对于 Python 3.14，在导入 webview 模块之前就设置好环境变量，确保完全避免使用需要 pythonnet 的后端
webview_import_successful = False

# 确保不导入 pythonnet，避免 Python 3.14 兼容性问题
if 'pythonnet' in sys.modules:
    del sys.modules['pythonnet']

# 在导入 webview 之前，先设置环境变量，强制使用 edgechromium 后端
os.environ['PYWEBVIEW_GUI'] = 'edgechromium'

# 对于 Python 3.14，使用更严格的兼容性处理
if sys.version_info >= (3, 14):
    try:
        # 1. 强制设置环境变量，确保在 webview 模块导入前生效
        os.environ['PYWEBVIEW_GUI'] = 'edgechromium'
        os.environ['WEBVIEW_GUI'] = 'edgechromium'  # 兼容旧版本
        
        # 2. 现在导入 webview 模块
        import webview
        
        # 3. 直接设置 gui 属性
        webview.gui = 'edgechromium'
        
        # 4. 重写 webview.guilib 模块，完全替换它，防止尝试导入 winforms
        import types
        
        # 创建一个完整的 guilib 模块替代品
        new_guilib = types.ModuleType('webview.guilib')
        
        # 定义一个安全的 initialize 函数，只返回 edgechromium 后端
        def safe_initialize(gui=None):
            # 在 Python 3.14 环境下，只支持 edgechromium 后端
            if not hasattr(webview, 'platforms'):
                webview.platforms = types.ModuleType('webview.platforms')
            
            # 确保 edgechromium 后端模块存在
            if not hasattr(webview.platforms, 'edgechromium'):
                # 创建一个功能完整的 edgechromium 模块
                edgechromium_module = types.ModuleType('webview.platforms.edgechromium')
                
                # 导入真正的 edgechromium 模块内容
                try:
                    # 使用安全的方式导入 edgechromium 模块，避免在函数内使用 import *
                    import importlib
                    real_edgechromium = importlib.import_module('webview.platforms.edgechromium')
                    # 复制所有属性到新模块
                    for attr in dir(real_edgechromium):
                        if not attr.startswith('_'):
                            setattr(edgechromium_module, attr, getattr(real_edgechromium, attr))
                except ImportError:
                    # 如果导入失败，定义必要的函数
                    def create_window(*args, **kwargs):
                        # 简单实现，实际会由 webview 库处理
                        pass
                    
                    def start(*args, **kwargs):
                        # 简单实现，实际会由 webview 库处理
                        pass
                    
                    def load_url(*args, **kwargs):
                        # 简单实现，实际会由 webview 库处理
                        pass
                    
                    edgechromium_module.create_window = create_window
                    edgechromium_module.start = start
                    edgechromium_module.load_url = load_url
                
                # 添加到 platforms 模块和 sys.modules
                webview.platforms.edgechromium = edgechromium_module
                sys.modules['webview.platforms.edgechromium'] = edgechromium_module
            
            return webview.platforms.edgechromium
        
        # 定义一个安全的 try_import 函数，不尝试导入 winforms
        def safe_try_import(guis):
            # 在 Python 3.14 环境下，只尝试导入 edgechromium
            return True
        
        # 为新的 guilib 模块添加必要的属性
        new_guilib.initialize = safe_initialize
        new_guilib.try_import = safe_try_import
        new_guilib.GUI = {'edgechromium': 'edgechromium'}
        new_guilib.current_gui = 'edgechromium'
        
        # 完全替换 webview.guilib 模块
        webview.guilib = new_guilib
        
        # 5. 防止 webview 尝试导入 clr 和 pythonnet
        # 创建一个假的 clr 模块，防止真正的 clr 被导入
        import sys
        fake_clr = types.ModuleType('clr')
        sys.modules['clr'] = fake_clr
        
        # 创建一个假的 pythonnet 模块，防止真正的 pythonnet 被导入
        fake_pythonnet = types.ModuleType('pythonnet')
        sys.modules['pythonnet'] = fake_pythonnet
        
        # 6. 确保 webview.platforms 中没有 winforms 模块
        if hasattr(webview.platforms, 'winforms'):
            # 如果存在，替换为一个空模块
            webview.platforms.winforms = types.ModuleType('webview.platforms.winforms')
        
        # 7. 确保 sys.modules 中没有 winforms 相关模块
        for module_name in list(sys.modules.keys()):
            if 'winforms' in module_name:
                del sys.modules[module_name]
        
        webview_import_successful = True
        print(f"[Pvue] Python 3.14 WebView 兼容性处理成功，使用 edgechromium 后端")
        
    except Exception as e:
        print(f"[Pvue] Python 3.14 WebView 兼容性处理出错: {e}")
        print(f"[Pvue] webview 库在 Python 3.14 环境下无法正常工作，因为它依赖的 pythonnet 不支持 Python 3.14")
        print(f"[Pvue] 建议使用 web 模式运行应用: app = PvueApp(mode='web')")
        # 在 Python 3.14 环境下，如果 webview 导入失败，就直接设置为 None
        webview = None
else:
    # 对于 Python 3.14 以下的版本，正常导入 webview
    try:
        import webview
        webview_import_successful = True
    except ImportError:
        webview = None

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
        # 检查 webview 是否可用
        if webview is None:
            raise RuntimeError("WebView is not available in Python 3.14. Please use web mode instead: app = PvueApp(mode='web')")
        
        try:
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
        except AttributeError as e:
            if "'NoneType' object has no attribute" in str(e):
                raise RuntimeError("WebView is not properly initialized in Python 3.14. Please use web mode instead: app = PvueApp(mode='web')")
            raise
    
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
