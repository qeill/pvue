"""Pvue 科学计算器应用"""

from pvue import PvueApp
import os
import math

# 处理 PyInstaller 打包后的静态文件路径
def get_static_dir():
    import sys
    if hasattr(sys, '_MEIPASS'):
        # 打包后的临时目录
        return os.path.join(sys._MEIPASS, 'calculator-frontend')
    else:
        # 开发环境
        return os.path.join(os.path.dirname(__file__), 'calculator-frontend')

# 创建 Pvue 应用实例
app = PvueApp(
    web_port=8081,
    ws_port=9001,
    static_dir=get_static_dir(),
    mode='webview',  # 使用 PyWebView 桌面应用模式
    webview_options={
        'title': 'Pvue 科学计算器',  # 窗口标题
        'size': (800, 600),  # 窗口大小
        'resizable': True,  # 允许调整窗口大小
        'debug': False  # 关闭调试模式
    }
)

# 暴露科学计算函数给前端调用

@app.expose('calculate')
def calculate(expression):
    """计算表达式的值"""
    try:
        # 替换数学函数为 Python 可执行的形式
        expression = expression.replace('sin', 'math.sin')
        expression = expression.replace('cos', 'math.cos')
        expression = expression.replace('tan', 'math.tan')
        expression = expression.replace('asin', 'math.asin')
        expression = expression.replace('acos', 'math.acos')
        expression = expression.replace('atan', 'math.atan')
        expression = expression.replace('log', 'math.log10')
        expression = expression.replace('ln', 'math.log')
        expression = expression.replace('sqrt', 'math.sqrt')
        expression = expression.replace('^', '**')
        expression = expression.replace('π', 'math.pi')
        expression = expression.replace('e', 'math.e')
        
        # 执行计算
        result = eval(expression)
        return {'success': True, 'result': result}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.expose('factorial')
def factorial(n):
    """计算阶乘"""
    try:
        n = int(n)
        result = math.factorial(n)
        return {'success': True, 'result': result}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.expose('power')
def power(base, exponent):
    """计算幂"""
    try:
        base = float(base)
        exponent = float(exponent)
        result = math.pow(base, exponent)
        return {'success': True, 'result': result}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.expose('root')
def root(base, n):
    """计算n次方根"""
    try:
        base = float(base)
        n = float(n)
        result = math.pow(base, 1/n)
        return {'success': True, 'result': result}
    except Exception as e:
        return {'success': False, 'error': str(e)}

# 启动应用
if __name__ == '__main__':
    app.start()