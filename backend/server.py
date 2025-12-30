import asyncio
import json
import websockets
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('websocket_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 连接管理
connected_clients = set()

# 文本处理函数
async def process_text(text: str, func: str) -> str:
    """根据指定功能处理文本"""
    try:
        if func == 'uppercase':
            return text.upper()
        elif func == 'lowercase':
            return text.lower()
        elif func == 'reverse':
            return text[::-1]
        else:
            return f'错误：不支持的功能 "{func}"，请使用 uppercase, lowercase 或 reverse'
    except Exception as e:
        logger.error(f"处理文本时发生错误: {str(e)}")
        return f'错误：{str(e)}'

# WebSocket服务器处理函数
async def handle_connection(websocket, path):
    client_address = websocket.remote_address
    client_id = id(websocket)
    
    # 添加到连接集合
    connected_clients.add(client_id)
    logger.info(f"新连接: {client_address} (ID: {client_id}), 当前连接数: {len(connected_clients)}")
    
    try:
        # 持续接收客户端消息
        async for message in websocket:
            logger.info(f"收到消息 from {client_id}: {message}")
            
            try:
                # 解析JSON消息
                data = json.loads(message)
                text = data.get('text', '')
                function = data.get('function', 'uppercase')
                
                # 处理文本
                result = await process_text(text, function)
                
                # 构造响应消息
                response = {
                    'result': result
                }
                
                # 发送响应给客户端
                await websocket.send(json.dumps(response))
                logger.info(f"发送响应 to {client_id}: {response}")
                
            except json.JSONDecodeError:
                # 处理JSON解析错误
                error_response = {
                    'result': '错误：无效的JSON格式'
                }
                await websocket.send(json.dumps(error_response))
                logger.error(f"发送错误响应 to {client_id}: 无效的JSON格式")
                
            except Exception as e:
                # 处理其他异常
                error_response = {
                    'result': f'错误：{str(e)}'
                }
                await websocket.send(json.dumps(error_response))
                logger.error(f"发送错误响应 to {client_id}: {str(e)}")
                
    except websockets.exceptions.ConnectionClosedOK:
        logger.info(f"连接正常关闭: {client_id}")
    except websockets.exceptions.ConnectionClosedError:
        logger.error(f"连接异常关闭: {client_id}")
    except Exception as e:
        logger.error(f"连接处理错误 {client_id}: {str(e)}")
    finally:
        # 从连接集合中移除
        connected_clients.remove(client_id)
        logger.info(f"连接已关闭: {client_id}, 当前连接数: {len(connected_clients)}")

async def main():
    # 创建WebSocket服务器
    server = await websockets.serve(
        handle_connection,  # 处理函数
        "localhost",        # 主机地址
        8765                # 端口号
    )
    
    logger.info("WebSocket服务器正在运行...")
    logger.info("地址: ws://localhost:8765")
    logger.info("支持的功能: uppercase, lowercase, reverse")
    
    # 保持服务器运行
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n服务器已停止")
    except Exception as e:
        logger.critical(f"服务器启动失败: {str(e)}")