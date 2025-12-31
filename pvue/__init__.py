"""Pvue - Vue 3 + Python WebSocket 桌面应用框架

Pvue是一个将Vue 3前端与Python后端通过WebSocket集成的桌面应用框架，支持多种运行模式：
- web模式：传统Web服务器
- eel模式：基于Eel的桌面应用
- webview模式：基于PyWebView的桌面应用

主要特性：
- 前后端通过WebSocket实时通信
- 支持多种桌面应用运行模式
- 自动处理静态文件服务
- 支持Python 3.6+，包括Python 3.14
- 灵活的日志系统
- 完善的错误处理和用户反馈

快速开始：
```python
from pvue import PvueApp

app = PvueApp(
    web_port=3000,
    ws_port=8765,
    mode='web'  # 或 'eel' 或 'webview'
)

# 暴露Python函数给前端调用
@app.expose()
def hello_world():
    return "Hello from Python!"

if __name__ == "__main__":
    app.start()
```
"""

# 先定义基本的模块变量，这些不需要任何导入
__version__ = "0.4.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__description__ = "A Python framework that integrates Vue 3 frontend with Python backend using WebSocket"

import os

# 只导入核心功能，不导入可选的webview模块
from .utils import get_static_dir
from .backend.server import WebSocketServer

# 定义__all__，只包含核心功能
__all__ = [
    "get_static_dir",
    "WebSocketServer",
    "__version__",
    "__author__",
    "__email__",
    "__description__"
]

# 延迟导入PvueApp和run_pvue_app，直到它们被实际使用
# 这样在执行pvue --version时就不会触发webview的导入
import sys

# 检查是否正在执行CLI命令
# 1. 检查当前脚本是否是cli.py
# 2. 检查sys.argv中是否包含--version或其他CLI特定参数
is_cli_command = False

# 检查当前脚本名称
current_script = os.path.basename(sys.argv[0]) if sys.argv else ""
is_cli_command = current_script == "pvue" or "pvue.exe" in current_script

# 检查命令行参数
if not is_cli_command:
    for arg in sys.argv:
        if arg in ["--version", "-v", "--web-port", "--ws-port", "--static-dir"]:
            is_cli_command = True
            break

# 只有在非CLI命令情况下才导入额外功能
if not is_cli_command:
    from .eel import EelApp, create_eel_app, get_eel_app
    __all__.extend(["EelApp", "create_eel_app", "get_eel_app"])
    
    # 尝试导入WebView相关功能，如果失败则跳过
    webview_imported = False
    try:
        from .main import PvueApp, run_pvue_app
        __all__.extend(["PvueApp", "run_pvue_app"])
        
        # 只有在导入PvueApp后才尝试导入webview
        try:
            from .webview import WebViewApp, create_webview_app, get_webview_app
            __all__.extend(["WebViewApp", "create_webview_app", "get_webview_app"])
            webview_imported = True
        except ImportError:
            # 如果pywebview未安装，只提供核心功能
            pass
    except ImportError:
        # 如果导入失败，仍然提供核心功能
        pass