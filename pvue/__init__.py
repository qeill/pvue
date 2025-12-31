"""Pvue - Vue 3 + Python WebSocket 桌面应用框架"""

__version__ = "0.1.9"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__description__ = "A Python framework that integrates Vue 3 frontend with Python backend using WebSocket"

from .main import PvueApp, run_pvue_app
from .backend.server import WebSocketServer
from .eel import EelApp, create_eel_app, get_eel_app
from .utils import get_static_dir

# 尝试导入WebView相关功能，如果失败则跳过
__all__ = [
    "PvueApp",
    "run_pvue_app",
    "WebSocketServer",
    "EelApp",
    "create_eel_app",
    "get_eel_app",
    "get_static_dir",
    "__version__",
    "__author__",
    "__email__",
    "__description__"
]

# 尝试导入WebView相关功能
webview_imported = False
try:
    from .webview import WebViewApp, create_webview_app, get_webview_app
    __all__.extend(["WebViewApp", "create_webview_app", "get_webview_app"])
    webview_imported = True
except ImportError:
    # 如果pywebview未安装，只提供核心功能
    pass