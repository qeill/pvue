# PyInstaller 打包指南：将 Pvue 应用打包为单文件 EXE

本指南详细介绍了如何使用 PyInstaller 将 Pvue 框架开发的应用打包成单个可执行文件（EXE），包括如何处理静态文件、添加 hook 文件以及解决常见问题。

## 1. 环境准备

### 1.1 安装 PyInstaller

```bash
# 安装 PyInstaller
pip install pyinstaller

# 验证安装
pyinstaller --version
```

### 1.2 准备应用代码

确保你的 Pvue 应用已经完成开发，并且可以正常运行。以下是一个典型的 Pvue 应用结构：

```
your_app/
├── your_app.py          # 主应用文件
├── your_frontend/       # 前端静态文件
│   ├── index.html       # 前端入口
│   ├── app.js           # JavaScript 代码
│   └── style.css        # 样式文件
└── requirements.txt     # 依赖文件
```

## 2. 基本打包方法

### 2.1 简单打包命令

```bash
# 基本打包命令
pyinstaller --onefile --windowed your_app.py
```

参数说明：
- `--onefile`：打包成单个 EXE 文件
- `--windowed`：不显示控制台窗口（GUI 应用使用）
- `your_app.py`：你的主应用文件

### 2.2 处理静态文件

Pvue 应用需要访问前端静态文件，在打包后需要特殊处理。在你的应用代码中添加以下逻辑：

```python
import os
import sys

# 处理 PyInstaller 打包后的静态文件路径
def get_static_dir():
    if hasattr(sys, '_MEIPASS'):
        # 打包后的临时目录
        return os.path.join(sys._MEIPASS, 'your_frontend')
    else:
        # 开发环境
        return os.path.join(os.path.dirname(__file__), 'your_frontend')

# 在 PvueApp 初始化时使用
def main():
    static_dir = get_static_dir()
    app = PvueApp(
        static_dir=static_dir,
        # 其他配置...
    )
    app.start()

if __name__ == '__main__':
    main()
```

### 2.3 使用 spec 文件打包

对于复杂应用，建议使用 spec 文件进行更精细的配置：

```bash
# 生成 spec 文件
pyinstaller --onefile --windowed --name your_app_name your_app.py
```

这将生成 `your_app_name.spec` 文件，你可以编辑这个文件来添加静态文件、hook 等配置。

## 3. 添加 Hook 文件

Hook 文件用于告诉 PyInstaller 如何处理特定的 Python 模块，尤其是那些使用动态导入或需要特殊处理的模块。

### 3.1 什么是 Hook 文件？

Hook 文件是 PyInstaller 用来确定如何打包特定模块的 Python 脚本。它们通常位于 PyInstaller 的 hooks 目录中，或者你可以创建自定义 hook 文件。

### 3.2 创建自定义 Hook 文件

对于 Pvue 应用，你可能需要为特定模块创建 hook 文件。例如，创建一个 `hook-pvue.py` 文件：

```python
# hook-pvue.py
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# 收集 pvue 模块的所有子模块
hiddenimports = collect_submodules('pvue')

# 收集 pvue 模块的静态文件
datas = collect_data_files('pvue', include_py_files=False)
```

### 3.3 使用 Hook 文件

#### 方法一：命令行参数

```bash
pyinstaller --onefile --windowed --additional-hooks-dir=. your_app.py
```

#### 方法二：编辑 spec 文件

在 spec 文件的 `Analysis` 部分添加 hook 文件路径：

```python
a = Analysis(
    ['your_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        # 添加你的静态文件
        ('your_frontend', 'your_frontend'),
    ],
    hiddenimports=[
        # 添加需要的隐藏导入
        'pvue',
        'websockets',
        'eel',
        'webview',
    ],
    hookspath=['.'],  # 指定 hook 文件目录
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
```

### 3.4 常见模块的 Hook 处理

#### 3.4.1 Webview 模块

对于 PyWebView 模块，你可能需要添加以下 hook：

```python
# hook-webview.py
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

# 收集 webview 的所有子模块
hiddenimports = collect_submodules('webview')

# 收集 webview 的 DLL 文件和其他资源
datas = collect_data_files('webview')
binaries = collect_dynamic_libs('webview')
```

#### 3.4.2 Eel 模块

对于 Eel 模块，你可能需要添加以下 hook：

```python
# hook-eel.py
from PyInstaller.utils.hooks import collect_data_files

# 收集 eel 的资源文件
datas = collect_data_files('eel')
```

## 4. 完整打包示例：Notepad 应用

以下是打包 Pvue 记事本应用的完整示例：

### 4.1 准备应用代码

确保 `notepad.py` 中包含静态文件处理逻辑：

```python
import os
import sys
from pvue import PvueApp

# 处理 PyInstaller 打包后的静态文件路径
def get_static_dir():
    if hasattr(sys, '_MEIPASS'):
        # 打包后的临时目录
        return os.path.join(sys._MEIPASS, 'notepad-frontend')
    else:
        # 开发环境
        return os.path.join(os.path.dirname(__file__), 'notepad-frontend')

def main():
    # 创建 Pvue 应用
    static_dir = get_static_dir()
    app = PvueApp(
        static_dir=static_dir,
        web_port=0,  # 自动选择端口
        ws_port=0,
        title="Pvue Notepad",
        mode="webview"  # 使用 WebView 模式
    )
    
    # 暴露函数给前端
    @app.expose
    def save_file(content, filename):
        # 保存文件逻辑
        pass
    
    # 启动应用
    app.start()

if __name__ == "__main__":
    main()
```

### 4.2 运行打包命令

```bash
# 创建 hook 文件
cat > hook-pvue.py << 'EOF'
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# 收集 pvue 模块的所有子模块
hiddenimports = collect_submodules('pvue')

# 收集 pvue 模块的静态文件
datas = collect_data_files('pvue', include_py_files=False)
EOF

# 打包命令
pyinstaller --onefile --windowed --additional-hooks-dir=. --add-data "notepad-frontend;notepad-frontend" notepad.py
```

### 4.3 验证打包结果

打包完成后，在 `dist` 目录中会生成 `notepad.exe` 文件。双击运行该文件，验证应用是否正常工作。

## 5. 常见问题和解决方案

### 5.1 静态文件找不到

**问题**：打包后应用无法找到静态文件

**解决方案**：
1. 确保使用了 `get_static_dir()` 函数处理静态文件路径
2. 确保在打包命令中添加了 `--add-data` 参数
3. 检查 spec 文件中的 `datas` 配置是否正确

### 5.2 缺少模块或 DLL

**问题**：运行 EXE 时提示缺少模块或 DLL 文件

**解决方案**：
1. 添加相应的 `hiddenimports` 到 spec 文件
2. 创建自定义 hook 文件
3. 使用 `--collect-all` 参数收集所有依赖

### 5.3 应用启动慢

**问题**：单文件 EXE 启动速度慢

**解决方案**：
1. 考虑使用 `--onedir` 模式（多文件模式），启动速度更快
2. 优化应用代码，减少启动时的资源加载
3. 使用 `--noconsole` 而不是 `--windowed`（Windows 系统）

### 5.4 无法启动 WebView

**问题**：WebView 模式下应用无法启动

**解决方案**：
1. 确保添加了 webview 的 DLL 文件到打包中
2. 创建 `hook-webview.py` 文件
3. 检查 WebView 版本是否兼容

## 6. 高级配置

### 6.1 自定义图标

```bash
pyinstaller --onefile --windowed --icon=your_icon.ico your_app.py
```

### 6.2 压缩级别

```bash
pyinstaller --onefile --windowed --upx-dir=upx-4.0.2 --compress=9 your_app.py
```

### 6.3 排除不必要的模块

```bash
pyinstaller --onefile --windowed --exclude-module=tkinter --exclude-module=matplotlib your_app.py
```

## 7. 总结

使用 PyInstaller 打包 Pvue 应用为单文件 EXE 需要注意以下几点：

1. **静态文件处理**：使用 `_MEIPASS` 处理打包后的静态文件路径
2. **Hook 文件**：为特殊模块创建自定义 hook 文件
3. **隐藏导入**：添加所有需要的 `hiddenimports`
4. **DLL 文件**：确保包含所有必要的 DLL 文件
5. **测试**：在不同环境下测试打包后的应用

通过本指南，你应该能够成功将 Pvue 应用打包为单个可执行文件，方便分发给用户使用。

## 8. 相关资源

- [PyInstaller 官方文档](https://pyinstaller.org/en/stable/)
- [PyWebView 文档](https://pywebview.flowrl.com/)
- [Eel 文档](https://github.com/ChrisKnott/Eel)
- [Pvue 框架文档](README.md)