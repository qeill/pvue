import argparse
from .main import run_pvue_app

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
        from pvue import __version__
        print(f'Pvue 版本: {__version__}')
        return
    
    # 启动 Pvue 应用
    run_pvue_app(
        web_port=args.web_port,
        ws_port=args.ws_port,
        static_dir=args.static_dir
    )

if __name__ == '__main__':
    main()