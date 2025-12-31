import argparse
import os
import re

def get_version():
    """直接从__init__.py文件读取版本号，避免触发完整导入链"""
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建__init__.py文件路径
    init_file = os.path.join(current_dir, '__init__.py')
    
    # 读取__init__.py文件内容
    with open(init_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式提取版本号
    version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if version_match:
        return version_match.group(1)
    return 'unknown'

def main():
    """Pvue 命令行工具主函数"""
    parser = argparse.ArgumentParser(
        description='Pvue - Vue 3 + Python WebSocket 桌面应用框架'
    )
    
    # 添加命令行参数
    parser.add_argument(
        '--web-port',
        type=int,
        default=3000,
        help='静态文件服务端口，默认为 3000'
    )
    
    parser.add_argument(
        '--ws-port',
        type=int,
        default=8765,
        help='WebSocket 服务器端口，默认为 8765'
    )
    
    parser.add_argument(
        '--static-dir',
        type=str,
        default=None,
        help='静态文件目录，默认为框架内置的静态文件'
    )
    
    parser.add_argument(
        '--version',
        action='store_true',
        help='显示 Pvue 版本信息'
    )
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 显示版本信息
    if args.version:
        version = get_version()
        print(f'Pvue 版本: {version}')
        return
    
    # 启动 Pvue 应用 - 只在需要时导入，避免不必要的依赖加载
    from .main import run_pvue_app
    run_pvue_app(
        web_port=args.web_port,
        ws_port=args.ws_port,
        static_dir=args.static_dir
    )

if __name__ == '__main__':
    main()