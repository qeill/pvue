# PyInstaller 打包指南

本指南将详细介绍如何使用 PyInstaller 将基于 Pvue 框架开发的程序打包为单文件 EXE。

## 目录

- [1. 准备工作](#1-准备工作)
- [2. 修改程序代码](#2-修改程序代码)
- [3. 创建 spec 文件](#3-创建-spec-文件)
- [4. 编辑 spec 文件](#4-编辑-spec-文件)
- [5. 执行打包](#5-执行打包)
- [6. 测试打包结果](#6-测试打包结果)
- [7. 常见问题及解决方案](#7-常见问题及解决方案)

## 1. 准备工作

### 1.1 安装 PyInstaller

```bash
pip install pyinstaller
```

### 1.2 确保程序可以正常运行

在打包前，确保你的 Pvue 程序可以正常运行：

```bash
python your_program.py
```

## 2. 修改程序代码

为了让 Pvue 程序在打包后能够正确找到静态文件目录，需要修改程序代码，添加对 PyInstaller 打包后环境的支持。

### 2.1 修改静态文件路径处理

在你的主程序文件（如 `your_program.py`）中，修改静态文件目录的获取方式：

```python
from pvue import PvueApp
import os
import sys

# 处理 PyInstaller 打包后的路径
if getattr(sys, 'frozen', False):
    # 打包后的路径
    current_dir = sys._MEIPASS
else:
    # 开发环境路径
    current_dir = os.path.dirname(os.path.abspath(__file__))

# 静态文件目录
static_dir = os.path.join(current_dir, 'your-frontend-dir')

# 创建 Pvue 应用实例
app = PvueApp(
    static_dir=static_dir,
    web_port=3000,
    ws_port=8765,
    mode='webview'
)

# 启动应用
if __name__ == '__main__':
    app.start()
```

## 3. 创建 spec 文件

使用 PyInstaller 生成初始的 spec 文件：

```bash
pyi-makespec -F -w your_program.py
```

参数说明：
- `-F`：生成单文件 EXE
- `-w`：窗口模式运行，不显示命令行窗口
- `your_program.py`：你的主程序文件名

执行后，会生成一个 `your_program.spec` 文件。

## 4. 编辑 spec 文件

### 4.1 打开 spec 文件

使用文本编辑器打开生成的 `your_program.spec` 文件。

### 4.2 添加静态文件

在 `a = Analysis()` 部分的 `datas` 列表中添加你的静态文件目录：

```python
a = Analysis(
    ['your_program.py'],
    pathex=[],
    binaries=[],
    datas=[('your-frontend-dir', 'your-frontend-dir')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
```

其中：
- `'your-frontend-dir'`：你的前端代码目录名
- 第一个参数是源目录，第二个参数是打包后的目标目录

### 4.3 添加 hidden imports（可选）

如果打包后运行时出现缺少模块的错误，可以在 `hiddenimports` 列表中添加缺少的模块：

```python
hiddenimports=['pvue', 'websockets', 'webview'],
```

## 5. 执行打包

使用修改后的 spec 文件执行打包：

```bash
pyinstaller your_program.spec
```

## 6. 测试打包结果

打包完成后，在 `dist` 目录下会生成一个 `your_program.exe` 文件。

### 6.1 运行 EXE 文件

双击 `your_program.exe` 文件，或在命令行中运行：

```bash
dist\your_program.exe
```

### 6.2 验证功能

确保程序能够正常启动，所有功能正常工作。

## 7. 常见问题及解决方案

### 7.1 静态文件找不到

**错误信息**：
```
ValueError: Static directory not found: C:\Users\username\AppData\Local\Temp\_MEIxxxxxx\your-frontend-dir
```

**解决方案**：
- 确保你已经修改了程序代码，添加了对 PyInstaller 打包后路径的处理
- 确保你已经在 spec 文件的 `datas` 列表中添加了静态文件目录

### 7.2 缺少模块

**错误信息**：
```
ModuleNotFoundError: No module named 'xxx'
```

**解决方案**：
- 在 spec 文件的 `hiddenimports` 列表中添加缺少的模块
- 例如：`hiddenimports=['xxx', 'yyy'],`

### 7.3 程序启动后立即关闭

**解决方案**：
- 尝试使用非窗口模式打包（去掉 `-w` 参数），查看命令行中的错误信息
- 根据错误信息进行修复

### 7.4 WebSocket 端口被占用

**错误信息**：
```
WebSocket 服务器启动失败: [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8765): [winerror 10048] 通常每个套接字地址(协议/网络地址/端口)只允许使用一次。
```

**解决方案**：
- 修改程序中的 WebSocket 端口号，使用一个不常用的端口
- 或在程序中添加端口占用检测和自动切换功能

## 示例

以下是一个完整的示例，展示如何打包一个基于 Pvue 框架的科学计算器程序。

### 示例程序结构

```
caculator/
├── calculator-frontend/      # 前端代码目录
│   ├── index.html
│   ├── style.css
│   └── app.js
├── calcx.py                  # 主程序文件
└── calcx.spec                # spec 文件
```

### 示例 calcx.py

```python
from pvue import PvueApp
import os
import sys

# 处理 PyInstaller 打包后的路径
if getattr(sys, 'frozen', False):
    # 打包后的路径
    current_dir = sys._MEIPASS
else:
    # 开发环境路径
    current_dir = os.path.dirname(os.path.abspath(__file__))

# 静态文件目录
static_dir = os.path.join(current_dir, 'calculator-frontend')

# 创建 Pvue 应用实例
app = PvueApp(
    static_dir=static_dir,
    web_port=3000,
    ws_port=8766,
    mode='webview'
)

# 启动应用
if __name__ == '__main__':
    app.start()
```

### 示例 calcx.spec

```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['calcx.py'],
    pathex=[],
    binaries=[],
    datas=[('calculator-frontend', 'calculator-frontend')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='calcx',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

## 总结

通过以上步骤，你可以成功将基于 Pvue 框架开发的程序打包为单文件 EXE。

打包过程中遇到问题时，可以参考常见问题及解决方案，或查看 PyInstaller 的官方文档。

祝你打包顺利！
