# Pvue Eel Todo App 示例

这是一个使用 Pvue 框架开发的 Eel 桌面应用示例，展示了如何将 Vue 3 前端与 Python 后端通过 Eel 集成，构建桌面应用程序。

## 功能特性

- ✅ Vue 3 前端框架
- ✅ Python 后端逻辑
- ✅ Eel 桌面应用集成
- ✅ 待办事项管理（添加、删除、更新、清除）
- ✅ 前后端实时通信
- ✅ 现代化的 UI 设计

## 快速开始

### 1. 安装依赖

```bash
# 安装 pvue 框架
pip install -e ../../

# 安装其他依赖
pip install eel
```

### 2. 运行应用

```bash
python main.py
```

应用将在 Chrome 浏览器中打开一个桌面窗口，显示待办事项应用。

## 项目结构

```
eel-todo/
├── index.html          # 主 HTML 文件
├── style.css           # 样式文件
├── app.js              # Vue 3 应用逻辑
├── main.py             # Python 后端逻辑
└── README.md           # 项目说明文档
```

## 核心代码解析

### 前端代码（Vue 3）

```javascript
// app.js
const { createApp, ref, computed, onMounted } = Vue;

createApp({
  setup() {
    // 状态管理
    const todos = ref([]);
    const newTodo = ref('');
    
    // 从后端获取待办事项
    const fetchTodos = async () => {
      const result = await eel.get_todos()();
      todos.value = result;
    };
    
    // 添加待办事项
    const addTodo = async () => {
      if (newTodo.value.trim()) {
        const result = await eel.add_todo(newTodo.value)();
        todos.value = result;
        newTodo.value = '';
      }
    };
    
    // 其他方法...
    
    return {
      todos,
      newTodo,
      addTodo,
      // 其他返回值...
    };
  }
}).mount('#app');
```

### 后端代码（Python）

```python
# main.py
from pvue import PvueApp
import os

# 创建 Pvue 应用实例，使用 Eel 模式
app = PvueApp(
    web_port=8080,
    ws_port=9000,
    static_dir=os.path.dirname(__file__),
    use_eel=True,
    eel_options={
        'size': (600, 500),
        'app_mode': 'chrome',
        'dev_mode': True
    }
)

# 暴露函数给前端调用
@app.expose('get_todos')
def get_todos():
    return todos

# 其他暴露的函数...

# 启动应用
if __name__ == '__main__':
    app.start()
```

## 打包成可执行文件

使用 PyInstaller 可以将 Eel 应用打包成单个可执行文件，方便分发和使用。

### 1. 安装 PyInstaller

```bash
pip install pyinstaller
```

### 2. 创建 PyInstaller 配置文件

创建一个名为 `eel_todo.spec` 的文件，内容如下：

```python
# eel_todo.spec

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 分析主程序
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('index.html', '.'),
        ('style.css', '.'),
        ('app.js', '.'),
    ],
    hiddenimports=['bottle_websocket'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 生成可执行文件
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PvueTodoApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 设置为 True 可以显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加图标文件，如 'icon.ico'
)
```

### 3. 执行打包命令

```bash
pyinstaller eel_todo.spec
```

或者使用命令行参数：

```bash
pyinstaller --onefile --windowed --add-data "index.html;." --add-data "style.css;." --add-data "app.js;." --hidden-import bottle_websocket main.py
```

### 4. 测试打包后的应用

打包完成后，可执行文件将生成在 `dist` 目录下。双击运行 `PvueTodoApp.exe`（Windows）或 `PvueTodoApp`（Linux/macOS）即可启动应用。

## 打包选项说明

| 选项 | 说明 |
|------|------|
| `--onefile` | 生成单个可执行文件 |
| `--windowed` | 不显示控制台窗口（仅 GUI 应用） |
| `--add-data` | 添加静态文件到打包中 |
| `--hidden-import` | 添加隐藏的依赖 |
| `--icon` | 指定应用图标 |
| `--name` | 指定可执行文件名称 |

## 常见问题及解决方案

### 1. 打包后应用无法启动

**解决方案：**
- 检查是否缺少依赖，使用 `--hidden-import` 添加缺少的依赖
- 尝试使用 `--console` 选项生成带控制台的版本，查看错误信息
- 确保所有静态文件都已正确添加

### 2. 应用启动后无法加载静态文件

**解决方案：**
- 确保所有静态文件都已通过 `--add-data` 选项添加
- 检查文件路径是否正确
- 在代码中使用相对路径或动态获取文件路径

### 3. WebSocket 连接失败

**解决方案：**
- 确保 `bottle_websocket` 已被正确添加为隐藏依赖
- 检查防火墙设置，确保端口未被阻止
- 尝试使用不同的端口

## 许可证

MIT License

## 作者

Pvue Team
