"""Pvue WebView Todo App - 示例应用"""

from pvue import PvueApp
import os

# 创建 Pvue 应用实例，使用 WebView 模式
app = PvueApp(
    web_port=8080,
    ws_port=9000,
    static_dir=os.path.dirname(__file__),
    mode='webview',  # 使用 WebView 桌面应用模式
    webview_options={
        'title': 'Pvue WebView Todo App',
        'size': (600, 500),
        'resizable': True,
        'debug': True
    }
)

# 待办事项数据存储
todos = [
    {'id': 1, 'text': '学习 Vue 3', 'completed': False},
    {'id': 2, 'text': '学习 Python', 'completed': True},
    {'id': 3, 'text': '开发 Pvue 应用', 'completed': False}
]

# 暴露函数：获取待办事项列表
@app.expose('get_todos')
def get_todos():
    """获取待办事项列表"""
    return todos

# 暴露函数：添加待办事项
@app.expose('add_todo')
def add_todo(text):
    """添加新的待办事项"""
    # 生成新的 ID
    new_id = max(todo['id'] for todo in todos) + 1 if todos else 1
    # 添加新的待办事项
    todos.append({
        'id': new_id,
        'text': text,
        'completed': False
    })
    return todos

# 暴露函数：更新待办事项
@app.expose('update_todo')
def update_todo(id, completed):
    """更新待办事项的完成状态"""
    for todo in todos:
        if todo['id'] == id:
            todo['completed'] = completed
            break
    return todos

# 暴露函数：删除待办事项
@app.expose('delete_todo')
def delete_todo(id):
    """删除待办事项"""
    global todos
    todos = [todo for todo in todos if todo['id'] != id]
    return todos

# 暴露函数：清除已完成的待办事项
@app.expose('clear_completed_todos')
def clear_completed_todos():
    """清除已完成的待办事项"""
    global todos
    todos = [todo for todo in todos if not todo['completed']]
    return todos

# 暴露函数：获取应用信息
@app.expose('get_app_info')
def get_app_info():
    """获取应用信息"""
    return {
        'name': 'Pvue WebView Todo App',
        'version': '1.0.0',
        'description': '基于 Pvue 框架开发的 WebView 桌面应用',
        'author': 'Pvue Team',
        'todo_count': len(todos),
        'completed_count': sum(1 for todo in todos if todo['completed']),
        'mode': 'webview'
    }

# 启动应用
if __name__ == '__main__':
    app.start()
