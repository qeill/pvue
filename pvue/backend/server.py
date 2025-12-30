import asyncio
import json
import websockets

class WebSocketServer:
    """WebSocket 服务器类，用于处理前端和后端之间的通信"""
    
    def __init__(self, port=8765):
        """
        初始化 WebSocket 服务器
        
        Args:
            port: WebSocket 服务器端口
        """
        self.port = port
        self.server = None
        self.is_running = False
        self.connected_clients = set()
        # 函数注册表，用于存储前端可以调用的函数
        self.functions = {}
        # 注册默认的文本处理函数
        self.functions['uppercase'] = self.uppercase
        self.functions['lowercase'] = self.lowercase
        self.functions['reverse'] = self.reverse
    
    def expose_function(self, name, func):
        """
        暴露函数给前端调用
        
        Args:
            name: 前端调用时使用的函数名
            func: 要暴露的 Python 函数
        """
        self.functions[name] = func
    
    def uppercase(self, text):
        """将文本转换为大写"""
        return text.upper()
    
    def lowercase(self, text):
        """将文本转换为小写"""
        return text.lower()
    
    def reverse(self, text):
        """反转文本"""
        return text[::-1]
    
    async def handle_connection(self, websocket, path=None):
        """处理客户端连接"""
        client_address = websocket.remote_address
        print(f"\n新连接: {client_address}")
        
        # 添加到已连接客户端集合
        self.connected_clients.add(websocket)
        
        try:
            # 持续接收客户端消息
            async for message in websocket:
                print(f"收到消息: {message}")
                
                try:
                    # 解析 JSON 消息
                    data = json.loads(message)
                    
                    # 检查消息格式
                    if 'function' not in data:
                        raise ValueError('消息缺少 function 字段')
                    
                    function = data['function']
                    params = data.get('params', [])
                    
                    # 检查函数是否存在
                    if function not in self.functions:
                        raise ValueError(f'不支持的功能 "{function}"')
                    
                    # 调用函数
                    func = self.functions[function]
                    result = func(*params)
                    
                    # 构造响应消息
                    response = {
                        'result': result
                    }
                    
                    # 发送响应给客户端
                    await websocket.send(json.dumps(response))
                    print(f"发送响应: {response}")
                    
                except json.JSONDecodeError:
                    # 处理 JSON 解析错误
                    error_response = {
                        'result': '错误：无效的 JSON 格式'
                    }
                    await websocket.send(json.dumps(error_response))
                    print("发送错误响应: 无效的 JSON 格式")
                    
                except Exception as e:
                    # 处理其他异常
                    error_response = {
                        'result': f'错误：{str(e)}'
                    }
                    await websocket.send(json.dumps(error_response))
                    print(f"发送错误响应: {str(e)}")
                    
        except websockets.exceptions.ConnectionClosedOK:
            print(f"连接正常关闭: {client_address}")
        except websockets.exceptions.ConnectionClosedError:
            print(f"连接异常关闭: {client_address}")
        except Exception as e:
            print(f"连接处理错误: {e}")
        finally:
            # 从已连接客户端集合中移除
            self.connected_clients.remove(websocket)
            print(f"连接已关闭: {client_address}")
    
    async def start_server(self):
        """启动 WebSocket 服务器"""
        try:
            self.server = await websockets.serve(
                self.handle_connection,  # 处理函数
                "localhost",              # 主机地址
                self.port                 # 端口号
            )
            self.is_running = True
            
            # 保持服务器运行
            await self.server.wait_closed()
        except Exception as e:
            print(f"WebSocket 服务器启动失败: {e}")
            raise
    
    def start(self):
        """启动 WebSocket 服务器"""
        try:
            # 创建事件循环
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            
            # 运行服务器
            self.loop.run_until_complete(self.start_server())
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """停止 WebSocket 服务器"""
        if self.is_running:
            print(f"\n停止 WebSocket 服务器...")
            
            # 关闭所有连接
            for client in self.connected_clients.copy():
                try:
                    self.loop.run_until_complete(client.close())
                except Exception as e:
                    print(f"关闭客户端连接时出错: {e}")
            
            # 关闭服务器
            if self.server:
                self.server.close()
                self.loop.run_until_complete(self.server.wait_closed())
            
            # 关闭事件循环
            self.loop.close()
            
            self.is_running = False
            print("WebSocket 服务器已停止")