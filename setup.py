from setuptools import setup, find_packages
import os

# 读取README.md文件内容
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

# 读取requirements.txt文件内容
with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), 'r', encoding='utf-8') as f:
    install_requires = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    # 包的基本信息
    name="pvue",
    version="0.1.1",
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    
    # Python版本要求
    python_requires=">=3.8",
    
    # 包的依赖
    install_requires=install_requires,
    
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
