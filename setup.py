from setuptools import setup, find_packages
import os

# 读取README.md文件内容
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

# 核心依赖列表，不包含可能导致问题的pywebview
# 选择兼容Python 3.6+的依赖版本
install_requires = [
    'websockets>=9.1',  # websockets 9.1支持Python 3.6+
    'eel>=0.17.0',      # eel 0.17.0支持Python 3.6+
    'proxy_tools>=0.1.0',
    'typing_extensions>=3.7.4.3;python_version<="3.7"',  # 为Python 3.6-3.7添加typing_extensions
]

setup(
    # 包的基本信息
    name="pvue",
    version="0.3.2",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python framework that integrates Vue 3 frontend with Python backend using WebSocket",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pvue",
    license="MIT",
    
    # 包的分类信息
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    
    # Python版本要求
    python_requires=">=3.6",
    
    # 支持Python 3.14的特殊配置
    keywords=["vue", "python", "websocket", "desktop", "gui", "python3.14"],
    
    # 包的依赖
    install_requires=install_requires,
    
    # 可选依赖
    extras_require={
        # webview支持（包含pywebview，但用户可以选择不安装）
        "webview": [
            'pywebview>=6.1',
        ],
        # 完整安装（包含所有可选依赖）
        "full": [
            'pywebview>=6.1',
        ],
    },
    
    # 包的入口点
    entry_points={
        "console_scripts": [
            "pvue=pvue.cli:main",
        ],
    },
    
    # 包含的包
    packages=find_packages(),
    
    # 包含的非Python文件
    include_package_data=True,
    
    # 排除的文件
    exclude_package_data={
        "": ["*.pyc", "__pycache__", "*.log"],
    },
)
