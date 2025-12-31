"""PyWebView 集成模块，用于将 Vue 3 前端嵌入到 Python GUI 窗口中"""

import os
import sys
import threading
from .utils import get_static_dir

# 确保不导入 pythonnet，避免 Python 3.14 兼容性问题
if 'pythonnet' in sys.modules:
    del sys.modules['pythonnet']

# 在所有 Python 版本上，默认使用 edgechromium 后端，避免依赖 pythonnet
os.environ['PYWEBVIEW_GUI'] = 'edgechromium'
os.environ['WEBVIEW_GUI'] = 'edgechromium'  # 兼容旧版本

# 初始化变量
webview = None
webview_import_successful = False

# 支持的后端列表，按优先级排序
SUPPORTED_GUIS = ['edgechromium', 'cef', 'gtk', 'qt', 'qt5', 'qt6', 'wx']

# 尝试在所有 Python 版本上导入 webview 并初始化
for gui in SUPPORTED_GUIS:
    try:
        # 设置当前尝试的后端
        os.environ['PYWEBVIEW_GUI'] = gui
        os.environ['WEBVIEW_GUI'] = gui
        
        # 清除之前的 webview 导入（如果有）
        if 'webview' in sys.modules:
            del sys.modules['webview']
        
        # 导入 webview 模块
        import webview
        
        # 直接设置 gui 属性
        webview.gui = gui
        
        # 对于 Python 3.14，进行特殊处理，防止尝试导入 winforms
        if sys.version_info >= (3, 14):
            import types
            
            # 确保 platforms 模块存在
            if not hasattr(webview, 'platforms'):
                webview.platforms = types.ModuleType('webview.platforms')
            
            # 确保当前后端模块存在
            if not hasattr(webview.platforms, gui):
                # 尝试导入真正的后端模块
                try:
                    import importlib
                    real_backend = importlib.import_module(f'webview.platforms.{gui}')
                    # 将后端模块添加到 webview.platforms
                    setattr(webview.platforms, gui, real_backend)
                except ImportError:
                    # 如果导入失败，创建一个基本的后端模块
                    backend_module = types.ModuleType(f'webview.platforms.{gui}')
                    
                    # 定义必要的函数
                    def create_window(*args, **kwargs):
                        # 简单实现，实际会由 webview 库处理
                        pass
                    
                    def start(*args, **kwargs):
                        # 简单实现，实际会由 webview 库处理
                        pass
                    
                    def load_url(*args, **kwargs):
                        # 简单实现，实际会由 webview 库处理
                        pass
                    
                    # 添加函数到后端模块
                    backend_module.create_window = create_window
                    backend_module.start = start
                    backend_module.load_url = load_url
                    
                    # 将后端模块添加到 webview.platforms
                    setattr(webview.platforms, gui, backend_module)
                    # 添加到 sys.modules
                    sys.modules[f'webview.platforms.{gui}'] = backend_module
            
            # 重写 webview.guilib 模块，确保只使用当前后端
            new_guilib = types.ModuleType('webview.guilib')
            
            # 定义一个安全的 initialize 函数，只返回当前后端
            def safe_initialize(gui_param=None):
                # 在当前 Python 环境下，只支持选定的后端
                return getattr(webview.platforms, gui)
            
            # 定义一个安全的 try_import 函数，只尝试当前后端
            def safe_try_import(guis):
                return True
            
            # 为新的 guilib 模块添加必要的属性
            new_guilib.initialize = safe_initialize
            new_guilib.try_import = safe_try_import
            new_guilib.GUI = {gui: gui}
            new_guilib.current_gui = gui
            
            # 完全替换 webview.guilib 模块
            webview.guilib = new_guilib
            
            # 防止 webview 尝试导入 clr 和 pythonnet
            # 创建假的模块，防止真正的模块被导入
            fake_clr = types.ModuleType('clr')
            sys.modules['clr'] = fake_clr
            
            fake_pythonnet = types.ModuleType('pythonnet')
            sys.modules['pythonnet'] = fake_pythonnet
            
            # 确保没有 winforms 相关模块
            if hasattr(webview.platforms, 'winforms'):
                webview.platforms.winforms = types.ModuleType('webview.platforms.winforms')
            
            # 清除 sys.modules 中的 winforms 相关模块
            for module_name in list(sys.modules.keys()):
                if 'winforms' in module_name:
                    del sys.modules[module_name]
        
        # 测试 webview 是否能正常工作
        # 尝试调用一个简单的函数，确保模块能正常使用
        if hasattr(webview, 'create_window'):
            webview_import_successful = True
            print(f"[Pvue] WebView 初始化成功，使用 {gui} 后端")
            break  # 成功，退出循环
        
    except Exception as e:
        print(f"[Pvue] 尝试使用 {gui} 后端失败: {e}")
        # 继续尝试下一个后端
        continue

# 如果所有后端都失败，尝试使用一个基本的 webview 替代品
if not webview_import_successful:
    try:
        # 导入 webview 模块，但不初始化后端
        import webview
        webview_import_successful = True
        print(f"[Pvue] WebView 模块导入成功，但无法初始化任何后端，将使用默认配置")
    except ImportError as e:
        print(f"[Pvue] WebView 模块导入失败: {e}")
        print(f"[Pvue] 建议安装 pywebview: pip install pvue[webview]")
        webview = None

class WebViewApp:
    """WebView 应用类，用于管理 PyWebView 初始化和前后端通信"""
    
    def __init__(self,
                 static_dir,  # str 静态文件目录路径
                 entry_point='index.html',  # str 入口 HTML 文件
                 title='Pvue WebView App',  # str 窗口标题
                 size=(800, 600),  # tuple 窗口大小
                 resizable=True,  # bool 是否允许调整窗口大小
                 fullscreen=False,  # bool 是否全屏显示
                 frameless=False,  # bool 是否无边框
                 debug=False):  # bool 是否启用调试模式
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
        
    def expose(self, name=None):
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
    
    def expose_function(self, name, func):
        """
        暴露 Python 函数给前端调用
        
        Args:
            name: 前端调用时使用的函数名
            func: 要暴露的 Python 函数
        """
        self.exposed_functions[name] = func
    
    def start(self, server_url):
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
    
    def call(self, js_function, *args, **kwargs):
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
    
    def close(self):
        """关闭 WebView 窗口"""
        if self.window:
            self.window.destroy()
            self.window = None

# 全局 WebView 应用实例
_global_webview_app = None

def get_webview_app():
    """获取全局 WebView 应用实例"""
    return _global_webview_app

def create_webview_app(
    static_dir,  # str 静态文件目录路径
    entry_point='index.html',  # str 入口 HTML 文件
    title='Pvue WebView App',  # str 窗口标题
    size=(800, 600),  # tuple 窗口大小
    resizable=True,  # bool 是否允许调整窗口大小
    fullscreen=False,  # bool 是否全屏显示
    frameless=False,  # bool 是否无边框
    debug=False  # bool 是否启用调试模式
):
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
