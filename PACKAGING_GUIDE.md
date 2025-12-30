# Pvue 框架打包指南

本指南详细介绍了如何将 Vue 前端和 Python 后端整合的 Pvue 框架打包成一个可通过 pip 安装的 Python 包。

## 1. 环境准备

### 1.1 安装必要的工具

- Python 3.8+ 和 pip
- Node.js 和 npm
- 代码编辑器（如 VS Code）
- Git（可选，用于版本控制）

### 1.2 安装 Python 包

```bash
# 安装构建工具
pip install setuptools wheel twine

# 安装项目依赖
pip install -r requirements.txt
```

### 1.3 安装 Node.js 依赖

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
```

## 2. Vue 前端打包

### 2.1 配置 Vite 打包选项

确保 `vite.config.js` 中的打包配置正确：

```javascript
export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: '../pvue/pvue/static', // 打包输出目录设置为 Python 包的 static 目录
    assetsDir: 'assets',
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: undefined
      }
    }
  }
})
```

### 2.2 执行打包命令

```bash
# 进入前端目录
cd frontend

# 执行打包
npm run build
```

打包完成后，前端静态文件将被输出到 `pvue/pvue/static` 目录中。

## 3. Python 包结构

确保项目结构符合以下要求：

```
pvue/
├── pvue/                 # 主包目录
│   ├── __init__.py       # 包初始化文件
│   ├── main.py           # 主入口文件
│   ├── cli.py            # 命令行工具
│   ├── static/           # 前端静态文件
│   │   ├── index.html    # 前端入口HTML
│   │   ├── assets/       # 静态资源文件
│   │   └── ...           # 其他静态文件
│   ├── backend/          # 后端代码
│   │   └── server.py     # WebSocket服务器
│   └── utils/            # 工具函数
├── setup.py              # 打包配置文件
├── MANIFEST.in           # 非Python文件包含配置
├── requirements.txt      # 依赖文件
├── LICENSE.txt           # 许可证文件
├── README.md             # 项目说明
└── PACKAGING_GUIDE.md    # 打包指南
```

## 4. 配置文件检查

### 4.1 检查 setup.py

确保 `setup.py` 中的配置正确，包括：
- 包名、版本、作者等元数据
- 依赖列表
- 入口点配置
- 静态文件包含配置

### 4.2 检查 MANIFEST.in

确保 `MANIFEST.in` 正确包含了所有非Python文件：

```
# 包含前端静态文件
recursive-include pvue/static *

# 包含README和其他文档
include README.md
include LICENSE.txt
include requirements.txt

# 包含配置文件
include setup.py
```

## 5. 本地打包测试

### 5.1 构建 Python 包

```bash
# 在项目根目录执行
python setup.py sdist bdist_wheel
```

这将生成两个文件：
- `dist/pvue-0.1.0.tar.gz`（源代码分发包）
- `dist/pvue-0.1.0-py3-none-any.whl`（Wheel 分发包）

### 5.2 本地安装测试

```bash
# 安装本地构建的包
pip install dist/pvue-0.1.0-py3-none-any.whl

# 验证安装
pip show pvue

# 测试命令行工具
pvue --version
```

### 5.3 运行应用测试

```bash
# 启动 Pvue 应用
pvue

# 或使用 Python API
python -c "from pvue import run_pvue_app; run_pvue_app()"
```

打开浏览器访问 `http://localhost:3000`，验证应用是否正常运行。

### 5.4 卸载测试

```bash
# 卸载包
pip uninstall -y pvue
```

## 6. 发布到 PyPI

### 6.1 注册 PyPI 账号

如果还没有 PyPI 账号，需要先注册：
- 访问 [PyPI](https://pypi.org/) 注册账号
- 访问 [Test PyPI](https://test.pypi.org/) 注册测试账号（可选，用于测试）

### 6.2 配置 PyPI 认证

创建 `~/.pypirc` 文件，配置 PyPI 账号信息：

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcCJ...

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHlwaS5vcmcCJ...
```

### 6.3 发布到 Test PyPI（可选）

```bash
# 上传到 Test PyPI
twine upload --repository testpypi dist/*

# 从 Test PyPI 安装测试
pip install --index-url https://test.pypi.org/simple/ --no-deps pvue
```

### 6.4 发布到 PyPI

```bash
# 上传到 PyPI
twine upload dist/*
```

## 7. 使用示例

### 7.1 命令行使用

```bash
# 启动默认配置的应用
pvue

# 指定端口
pvue --web-port 8080 --ws-port 9000

# 查看版本
pvue --version
```

### 7.2 Python API 使用

```python
from pvue import PvueApp, run_pvue_app

# 方法一：使用便捷函数
run_pvue_app(web_port=8080, ws_port=9000)

# 方法二：使用 PvueApp 类
app = PvueApp(web_port=8080, ws_port=9000)
app.start()
```

## 8. 版本更新流程

### 8.1 更新版本号

- 修改 `pvue/__init__.py` 中的 `__version__`
- 修改 `setup.py` 中的 `version`

### 8.2 重新打包

```bash
# 清理旧的打包文件
rm -rf dist build pvue.egg-info

# 重新打包
python setup.py sdist bdist_wheel
```

### 8.3 重新发布

```bash
# 上传新版本
twine upload dist/*
```

## 9. 最佳实践

### 9.1 代码组织

- 保持 Python 代码和前端代码分离
- 使用清晰的目录结构
- 遵循 PEP 8 编码规范

### 9.2 版本控制

- 使用 Git 进行版本控制
- 遵循语义化版本控制规范（SemVer）
- 定期创建发布标签

### 9.3 文档

- 编写清晰的 README.md
- 提供详细的使用示例
- 保持文档与代码同步

### 9.4 测试

- 编写单元测试
- 进行集成测试
- 在不同环境下测试安装和运行

## 10. 常见问题

### 10.1 静态文件找不到

确保：
- Vue 打包输出目录正确
- `MANIFEST.in` 正确包含了静态文件
- 安装时使用了 `--include-package-data` 选项

### 10.2 依赖冲突

- 使用虚拟环境进行开发和测试
- 明确指定依赖版本范围
- 定期更新依赖

### 10.3 打包失败

- 检查 Python 版本是否符合要求
- 确保所有依赖都已安装
- 检查配置文件是否正确

## 11. 总结

通过本指南，您可以将 Vue 前端和 Python 后端整合的 Pvue 框架成功打包成一个可通过 pip 安装的 Python 包。打包后的包可以轻松分发给用户，用户只需通过 `pip install pvue` 即可安装并使用。

祝您打包顺利！

---

**Pvue 框架 - Vue 3 + Python WebSocket 桌面应用框架**
