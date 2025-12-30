@echo off

echo ========================================
echo         Pvue - Vue3 + Python WebSocket
echo ========================================
echo.
echo 正在启动后端 WebSocket 服务器...
start "Backend Server" cmd /k "cd backend && python server.py"

echo 正在启动前端开发服务器...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo 服务器启动完成！
echo 前端地址: http://localhost:3000
echo 后端地址: ws://localhost:8765
echo ========================================
echo.
echo 按任意键关闭此窗口...
pause > nul