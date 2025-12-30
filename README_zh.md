# Pvue - Python + Vue 3 框架

Pvue 是一个现代化的框架，将 Vue 3 前端与 Python WebSocket 后端相结合，让开发者能够轻松创建桌面应用程序。它提供了 Python 业务逻辑与 Vue 3 UI 之间的无缝集成，支持 Web 和桌面两种部署方式。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/pvue.svg)](https://badge.fury.io/py/pvue)
[![GitHub stars](https://img.shields.io/github/stars/qeill/pvue.svg)](https://github.com/qeill/pvue/stargazers)

[English Version](README.md)

## 功能特性

- **Vue 3 + Python WebSocket**：现代化的前端设计，支持响应式布局和实时通信
- **多种部署模式**：Web 服务器、Eel 桌面应用和 PyWebView 桌面应用
- **插件系统**：可扩展的架构，便于添加新功能
- **简单打包**：支持使用 PyInstaller 创建独立的 EXE 文件
- **响应式设计**：适配不同屏幕尺寸的现代化 UI
- **科学计算器**：内置示例，包含标准和科学两种模式
- **记事本应用**：简单文本编辑器示例

## 安装

### 前置条件

- Python 3.7+ 
- pip（Python 包管理器）

### 从 PyPI 安装

```bash
pip install pvue
```

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/qeill/pvue.git
cd pvue

# 安装依赖
pip install -r requirements.txt

# 以开发模式安装包
pip install -e .
```

## 快速开始

### 创建一个简单的 Pvue 应用

```python
from pvue.main import PvueApp

# 初始化 Pvue 应用
app = PvueApp()

# 定义一个可以从 Vue 调用的 Python 函数
def hello(name):
    return f"你好, {name}!"

# 注册函数
app.register_function(hello)

# 启动应用
app.run()
```

### 访问应用

运行脚本后，打开浏览器并导航到：
```
http://localhost:8000
```

## 使用方法

### Web 模式

```python
from pvue.main import PvueApp

app = PvueApp()
app.run(mode='web')  # 默认模式
```

### Eel 桌面模式

```python
from pvue.eel import PvueEelApp

app = PvueEelApp()
app.run()
```

### PyWebView 桌面模式

```python
from pvue.webview import PvueWebViewApp

app = PvueWebViewApp()
app.run()
```

## 示例应用

### 科学计算器

项目包含一个功能完整的科学计算器，支持标准和科学两种模式：

```bash
cd test
python scientific_calculator.py
```

### Eel 待办事项应用

```bash
cd examples/eel-todo
python main.py
```

### PyWebView 待办事项应用

```bash
cd examples/webview-todo
python main.py
```

## 项目结构

```
pvue/
├── backend/           # Python WebSocket 服务器
│   ├── __init__.py
│   └── server.py
├── frontend/          # Vue 3 前端
│   ├── src/
│   │   ├── components/    # 组件
│   │   ├── plugins/       # 插件
│   │   ├── App.vue        # 主应用组件
│   │   ├── main.js        # 入口文件
│   │   └── style.css      # 样式文件
│   ├── index.html         # HTML 模板
│   └── package.json       # 前端依赖配置
├── pvue/              # 主包代码
│   ├── __init__.py
│   ├── main.py         # Web 模式主文件
│   ├── eel.py          # Eel 模式主文件
│   ├── webview.py      # PyWebView 模式主文件
│   └── static/         # 编译后的前端文件
├── examples/          # 示例应用
│   ├── eel-todo/       # Eel 待办事项示例
│   └── webview-todo/   # PyWebView 待办事项示例
├── test/              # 测试应用
│   └── scientific_calculator.py  # 科学计算器
├── setup.py           # 包配置文件
└── README.md          # 项目文档
```

## 架构设计

### 前端

- **Vue 3**：使用 Composition API 的现代响应式框架
- **WebSocket**：与 Python 后端的实时通信
- **插件系统**：可扩展的架构，便于添加功能
- **响应式设计**：使用 CSS Grid 和 Flexbox 实现布局

### 后端

- **Python 3**：业务逻辑实现
- **WebSocket 服务器**：使用 websockets 库实现实时通信
- **多种模式**：Web 服务器、Eel 和 PyWebView 集成
- **函数注册**：简单注册 Python 函数，以便从 Vue 调用

## 插件开发

Pvue 包含一个插件系统，允许您扩展框架功能。有关详细信息，请参考 [PLUGIN_DEVELOPMENT.md](PLUGIN_DEVELOPMENT.md)。

## 打包应用

### 使用 PyInstaller 创建独立 EXE

```bash
pyinstaller --onefile --windowed your_app.py
```

有关更详细的打包说明，请参考 [PACKAGING_GUIDE.md](PACKAGING_GUIDE.md)。

## 配置

### 服务器配置

```python
app = PvueApp(
    host='localhost',
    port=8000,
    static_dir='path/to/static/files'
)
```

### 前端配置

修改 `frontend/src/App.vue` 中的 Vue 应用，以自定义 UI 和功能。

## 开发

### 构建前端

```bash
cd frontend
npm install
npm run build
```

### 运行开发服务器

```bash
cd frontend
npm run dev
```

### 运行测试

```bash
# 运行后端测试
python -m pytest

# 运行前端测试
cd frontend
npm test
```

## 贡献

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 有关详细信息，请参阅 [LICENSE.txt](LICENSE.txt) 文件。

## 致谢

- Vue 3：现代化的前端框架
- Python：强大的后端语言
- Eel 和 PyWebView：桌面集成
- websockets 库：实时通信支持

## 支持

如果您有任何问题或遇到问题，请在 GitHub 上打开一个 issue 或联系维护者。

---

**愉快编码！** 🚀
