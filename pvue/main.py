import os
import sys
import threading
import time
from wsgiref.simple_server import make_server
from .backend.server import WebSocketServer
from .eel import EelApp, create_eel_app
from .webview import WebViewApp, create_webview_app
from .utils import get_static_dir

class PvueApp:
    """Pvue 应用类，用于管理前端静态文件和后端 WebSocket 服务器"""
    
    def __init__(self, web_port=3000, ws_port=8765, static_dir=None, mode='web', eel_options=None, webview_options=None):
        """
        初始化 Pvue 应用
        
        Args:
            web_port: 静态文件服务端口
            ws_port: WebSocket 服务器端口
            static_dir: 静态文件目录，默认为框架内置的静态文件
            mode: 运行模式，可选值：'web'（传统 Web 服务器）、'eel'（Eel 桌面应用）、'webview'（PyWebView 桌面应用）
            eel_options: Eel 应用选项，包括 size, app_mode, port, dev_mode 等
            webview_options: PyWebView 应用选项，包括 title, size, resizable, fullscreen, frameless, debug 等
        """
        self.web_port = web_port
        self.ws_port = ws_port
        self.static_dir = static_dir or get_static_dir()
        self.mode = mode
        self.eel_options = eel_options or {}
        self.webview_options = webview_options or {}
        self.web_server = None
        self.ws_server = None
        self.eel_app = None
        self.webview_app = None
        self.is_running = False
        
        # 确保静态文件目录存在
        if not os.path.exists(self.static_dir):
            raise ValueError(f"Static directory not found: {self.static_dir}")
        
        # 确保运行模式有效
        if self.mode not in ['web', 'eel', 'webview']:
            raise ValueError(f"Invalid mode: {self.mode}. Valid modes are: 'web', 'eel', 'webview'")
    
    def _static_file_handler(self, environ, start_response):
        """静态文件处理函数"""
        path = environ['PATH_INFO']
        
        # 默认返回 index.html
        if path == '/':
            path = '/index.html'
        
        # 构建文件路径
        file_path = os.path.join(self.static_dir, path[1:])
        
        # 处理文件请求
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                
            # 根据文件扩展名设置 Content-Type
            content_type = 'text/plain'
            if path.endswith('.html'):
                content_type = 'text/html; charset=utf-8'
            elif path.endswith('.css'):
                content_type = 'text/css; charset=utf-8'
            elif path.endswith('.js'):
                content_type = 'application/javascript; charset=utf-8'
            elif path.endswith('.json'):
                content_type = 'application/json; charset=utf-8'
            elif path.endswith('.png'):
                content_type = 'image/png'
            elif path.endswith('.jpg') or path.endswith('.jpeg'):
                content_type = 'image/jpeg'
            elif path.endswith('.gif'):
                content_type = 'image/gif'
            
            start_response('200 OK', [('Content-Type', content_type)])
            return [content]
            
        except FileNotFoundError:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return [b'404 Not Found']
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [f'Error: {str(e)}'.encode('utf-8')]
    
    def start_web_server(self):
        """启动静态文件服务器"""
        try:
            self.web_server = make_server('', self.web_port, self._static_file_handler)
            print(f"\n静态文件服务器正在运行...")
            print(f"访问地址: http://localhost:{self.web_port}")
            self.web_server.serve_forever()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"静态文件服务器启动失败: {e}")
            sys.exit(1)
    
    def start_ws_server(self):
        """启动 WebSocket 服务器"""
        try:
            # 使用已经初始化并注册了函数的 WebSocketServer 实例
            if not self.ws_server:
                self.ws_server = WebSocketServer(self.ws_port)
            print(f"WebSocket 服务器正在运行...")
            print(f"WebSocket 地址: ws://localhost:{self.ws_port}")
            self.ws_server.start()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"WebSocket 服务器启动失败: {e}")
            sys.exit(1)
    
    def expose(self, name=None):
        """
        暴露 Python 函数给前端调用
        
        Args:
            name: 前端调用时使用的函数名，默认为原函数名
            
        Returns:
            装饰器函数
        """
        def decorator(func):
            # 获取函数名
            func_name = name or func.__name__
            
            # 在所有模式下，都将函数注册到 WebSocket 服务器
            if self.ws_server:
                self.ws_server.expose_function(func_name, func)
            else:
                # 否则，将函数添加到待注册列表
                if not hasattr(self, '_pending_functions'):
                    self._pending_functions = []
                self._pending_functions.append((func_name, func))
            
            # 对于 Eel 和 WebView 模式，还需要将函数暴露给对应的应用
            if self.mode in ['eel', 'webview']:
                if self.eel_app or self.webview_app:
                    if self.eel_app:
                        self.eel_app.expose_function(func_name, func)
                    elif self.webview_app:
                        self.webview_app.expose_function(func_name, func)
            
            return func
        return decorator
    
    def start(self):
        """启动 Pvue 应用"""
        if self.is_running:
            print("Pvue 应用已经在运行中")
            return
        
        self.is_running = True
        
        print(f"\n=== Pvue 应用启动中 ===")
        print(f"版本: {__import__('pvue').__version__}")
        print(f"运行模式: {self._get_mode_description()}")
        
        # 初始化 WebSocket 服务器（不启动）
        self.ws_server = WebSocketServer(self.ws_port)
        
        # 先注册待处理的函数到 WebSocket 服务器
        if hasattr(self, '_pending_functions'):
            for name, func in self._pending_functions:
                self.ws_server.expose_function(name, func)
            delattr(self, '_pending_functions')
        
        # 启动 WebSocket 服务器线程（在所有模式下都需要）
        ws_thread = threading.Thread(target=self.start_ws_server, daemon=True)
        ws_thread.start()
        
        # 等待 WebSocket 服务器启动
        time.sleep(0.5)
        
        # 构建服务器 URL
        server_url = f"http://localhost:{self.web_port}"
        
        if self.mode == 'eel':
            # Eel 模式：启动 Eel 应用
            self.eel_app = create_eel_app(
                static_dir=self.static_dir,
                port=self.web_port,
                **self.eel_options
            )
            
            # 暴露待处理的函数
            if hasattr(self, '_pending_functions'):
                for name, func in self._pending_functions:
                    self.eel_app.expose_function(name, func)
                delattr(self, '_pending_functions')
            
            print(f"\n=== Pvue Eel 应用启动成功 ===")
            print(f"WebSocket地址: ws://localhost:{self.ws_port}")
            print(f"应用将在桌面窗口中打开...")
            print(f"\n按窗口关闭按钮或 Ctrl+C 停止应用...")
            
            # 启动 Eel 应用（会阻塞当前线程）
            try:
                self.eel_app.start()
            except KeyboardInterrupt:
                self.stop()
        elif self.mode == 'webview':
            # WebView 模式：先启动静态文件服务器，再启动 WebView 窗口
            # 启动静态文件服务器线程
            web_thread = threading.Thread(target=self.start_web_server, daemon=True)
            web_thread.start()
            
            # 等待静态文件服务器启动
            time.sleep(0.5)
            
            # 创建 WebView 应用
            self.webview_app = create_webview_app(
                static_dir=self.static_dir,
                **self.webview_options
            )
            
            # 暴露待处理的函数
            if hasattr(self, '_pending_functions'):
                for name, func in self._pending_functions:
                    self.webview_app.expose_function(name, func)
                delattr(self, '_pending_functions')
            
            print(f"\n=== Pvue WebView 应用启动成功 ===")
            print(f"前端地址: {server_url}")
            print(f"WebSocket地址: ws://localhost:{self.ws_port}")
            print(f"应用将在桌面窗口中打开...")
            print(f"\n按窗口关闭按钮或 Ctrl+C 停止应用...")
            
            # 直接在主线程中启动 WebView 应用（PyWebView 要求必须在主线程中运行）
            try:
                self.webview_app.start(server_url)
            except KeyboardInterrupt:
                self.stop()
        else:
            # 传统 Web 模式：启动静态文件服务器
            web_thread = threading.Thread(target=self.start_web_server, daemon=True)
            web_thread.start()
            
            # 等待服务器启动
            time.sleep(0.5)
            
            print(f"\n=== Pvue 应用启动成功 ===")
            print(f"前端地址: {server_url}")
            print(f"WebSocket地址: ws://localhost:{self.ws_port}")
            print(f"\n按 Ctrl+C 停止应用...")
            
            try:
                # 保持主线程运行
                while self.is_running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop()
    
    def _get_mode_description(self):
        """
        获取运行模式描述
        
        Returns:
            str: 运行模式描述
        """
        mode_map = {
            'web': '传统 Web 服务器',
            'eel': 'Eel 桌面应用',
            'webview': 'PyWebView 桌面应用'
        }
        return mode_map.get(self.mode, '未知模式')
    
    def stop(self):
        """停止 Pvue 应用"""
        print(f"\n=== Pvue 应用正在停止 ===")
        
        # 停止 WebSocket 服务器
        if self.ws_server:
            self.ws_server.stop()
        
        # 停止静态文件服务器
        if self.web_server:
            self.web_server.shutdown()
        
        # 停止 Eel 应用
        if self.eel_app:
            # Eel 应用会在窗口关闭时自动停止，这里不需要额外处理
            pass
        
        # 停止 WebView 应用
        if self.webview_app:
            self.webview_app.close()
        
        self.is_running = False
        print(f"Pvue 应用已停止")

def run_pvue_app(web_port=3000, ws_port=8765, static_dir=None):
    """
    快速启动 Pvue 应用的便捷函数
    
    Args:
        web_port: 静态文件服务端口
        ws_port: WebSocket 服务器端口
        static_dir: 静态文件目录
    """
    app = PvueApp(web_port, ws_port, static_dir)
    app.start()