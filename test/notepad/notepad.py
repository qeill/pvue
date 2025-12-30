"""Pvue 记事本应用"""

from pvue import PvueApp
import os
import sys
import json

# 处理 PyInstaller 打包后的静态文件路径
def get_static_dir():
    if hasattr(sys, '_MEIPASS'):
        # 打包后的临时目录
        return os.path.join(sys._MEIPASS, 'notepad-frontend')
    else:
        # 开发环境
        return os.path.join(os.path.dirname(__file__), 'notepad-frontend')

# 创建 Pvue 应用实例
app = PvueApp(
    web_port=8080,
    ws_port=9000,
    static_dir=get_static_dir(),
    mode='webview',  # 使用 PyWebView 桌面应用模式
    webview_options={
        'title': 'Pvue 记事本',  # 窗口标题
        'size': (1000, 700),  # 窗口大小
        'resizable': True,  # 允许调整窗口大小
        'debug': False  # 关闭调试模式，不默认打开开发者工具
    }
)

# 笔记数据存储
notes = [
    {
        'id': 1,
        'title': '欢迎使用 Pvue 记事本',
        'content': '这是您的第一条笔记。\n您可以：\n1. 添加新笔记\n2. 编辑现有笔记\n3. 删除不需要的笔记\n4. 保存所有更改',
        'created_at': '2025-12-30 13:00:00',
        'updated_at': '2025-12-30 13:00:00'
    }
]

# 暴露函数：获取笔记列表
@app.expose('get_notes')
def get_notes():
    """获取所有笔记"""
    return notes

# 暴露函数：添加新笔记
@app.expose('add_note')
def add_note(title, content):
    """添加新笔记"""
    # 生成新的 ID
    new_id = max(note['id'] for note in notes) + 1 if notes else 1
    # 创建新笔记
    new_note = {
        'id': new_id,
        'title': title,
        'content': content,
        'created_at': '2025-12-30 13:00:00',
        'updated_at': '2025-12-30 13:00:00'
    }
    # 添加到笔记列表
    notes.append(new_note)
    return new_note

# 暴露函数：更新笔记
@app.expose('update_note')
def update_note(id, title, content):
    """更新笔记"""
    for note in notes:
        if note['id'] == id:
            note['title'] = title
            note['content'] = content
            note['updated_at'] = '2025-12-30 13:00:00'
            return note
    return None

# 暴露函数：删除笔记
@app.expose('delete_note')
def delete_note(id):
    """删除笔记"""
    global notes
    # 过滤掉要删除的笔记
    notes = [note for note in notes if note['id'] != id]
    return True

# 暴露函数：保存笔记到文件
@app.expose('save_notes')
def save_notes():
    """保存笔记到文件"""
    try:
        # 这里可以添加保存到文件的逻辑
        # with open('notes.json', 'w', encoding='utf-8') as f:
        #     json.dump(notes, f, ensure_ascii=False, indent=2)
        return {'success': True, 'message': '笔记保存成功'}
    except Exception as e:
        return {'success': False, 'message': f'保存失败：{str(e)}'}

# 暴露函数：从文件加载笔记
@app.expose('load_notes')
def load_notes():
    """从文件加载笔记"""
    try:
        # 这里可以添加从文件加载的逻辑
        # if os.path.exists('notes.json'):
        #     with open('notes.json', 'r', encoding='utf-8') as f:
        #         global notes
        #         notes = json.load(f)
        return {'success': True, 'notes': notes, 'message': '笔记加载成功'}
    except Exception as e:
        return {'success': False, 'message': f'加载失败：{str(e)}'}

# 启动应用
if __name__ == '__main__':
    app.start()
