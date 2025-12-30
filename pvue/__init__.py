"""Pvue - Vue 3 + Python WebSocket 桌面应用框架"""

__version__ = "0.1.4"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__description__ = "A Python framework that integrates Vue 3 frontend with Python backend using WebSocket"

from .main import PvueApp, run_pvue_app
from .backend.server import WebSocketServer
from .eel import EelApp, create_eel_app, get_eel_app
from .webview import WebViewApp, create_webview_app, get_webview_app
from .utils import get_static_dir

__all__ = [
    "PvueApp",
    "run_pvue_app",
    "WebSocketServer",
    "EelApp",
    "create_eel_app",
    "get_eel_app",
    "WebViewApp",
    "create_webview_app",
    "get_webview_app",
    "get_static_dir",
    "__version__",
    "__author__",
    "__email__",
    "__description__"
]