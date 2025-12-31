"""Pvue 日志模块

提供灵活的日志功能，支持不同的日志级别和格式化输出

日志级别（从低到高）：
- DEBUG: 调试信息，用于开发和调试
- INFO: 常规信息，用于记录正常运行状态
- WARNING: 警告信息，用于记录潜在问题
- ERROR: 错误信息，用于记录错误事件
- CRITICAL: 严重错误信息，用于记录导致程序崩溃的事件

使用示例：
```python
from pvue.logger import info, error, warning, debug, set_log_level

# 设置日志级别
set_log_level('INFO')

# 记录不同级别的日志
debug("这是一个调试信息")  # 不会输出，因为日志级别设置为INFO
info("这是一个普通信息")  # 会输出
warning("这是一个警告信息")  # 会输出
error("这是一个错误信息")  # 会输出到stderr
critical("这是一个严重错误信息")  # 会输出到stderr

# 支持格式化
info("访问地址: {}", "http://localhost:3000")
error("错误: {}", Exception("发生了一个错误"))
"""

import sys
import time

# 日志级别定义
class LogLevel:
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

# 默认日志级别
_current_log_level = LogLevel.INFO

# 日志级别名称映射
_log_level_names = {
    LogLevel.DEBUG: "DEBUG",
    LogLevel.INFO: "INFO",
    LogLevel.WARNING: "WARNING",
    LogLevel.ERROR: "ERROR",
    LogLevel.CRITICAL: "CRITICAL"
}

def set_log_level(level):
    """设置日志级别
    
    Args:
        level: 日志级别，可以是 LogLevel 枚举值或字符串
    """
    global _current_log_level
    if isinstance(level, str):
        # 从字符串转换为 LogLevel 枚举
        level = level.upper()
        for log_level, name in _log_level_names.items():
            if name == level:
                _current_log_level = log_level
                return
        raise ValueError(f"无效的日志级别: {level}")
    else:
        _current_log_level = level

def _log(level, message, *args, **kwargs):
    """内部日志函数
    
    Args:
        level: 日志级别
        message: 日志消息
        args: 格式化参数
        kwargs: 关键字参数
    """
    if level < _current_log_level:
        return
    
    # 格式化消息
    if args or kwargs:
        message = message.format(*args, **kwargs)
    
    # 获取当前时间
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # 构建日志行
    log_line = f"[{timestamp}] [Pvue] [{_log_level_names[level]}] {message}"
    
    # 根据日志级别选择输出流
    if level >= LogLevel.ERROR:
        print(log_line, file=sys.stderr)
    else:
        print(log_line, file=sys.stdout)

def debug(message, *args, **kwargs):
    """调试级别日志
    
    Args:
        message: 日志消息
        args: 格式化参数
        kwargs: 关键字参数
    """
    _log(LogLevel.DEBUG, message, *args, **kwargs)

def info(message, *args, **kwargs):
    """信息级别日志
    
    Args:
        message: 日志消息
        args: 格式化参数
        kwargs: 关键字参数
    """
    _log(LogLevel.INFO, message, *args, **kwargs)

def warning(message, *args, **kwargs):
    """警告级别日志
    
    Args:
        message: 日志消息
        args: 格式化参数
        kwargs: 关键字参数
    """
    _log(LogLevel.WARNING, message, *args, **kwargs)

def error(message, *args, **kwargs):
    """错误级别日志
    
    Args:
        message: 日志消息
        args: 格式化参数
        kwargs: 关键字参数
    """
    _log(LogLevel.ERROR, message, *args, **kwargs)

def critical(message, *args, **kwargs):
    """严重错误级别日志
    
    Args:
        message: 日志消息
        args: 格式化参数
        kwargs: 关键字参数
    """
    _log(LogLevel.CRITICAL, message, *args, **kwargs)

def exception(message, *args, **kwargs):
    """异常日志，自动包含异常信息
    
    Args:
        message: 日志消息
        args: 格式化参数
        kwargs: 关键字参数
    """
    import traceback
    _log(LogLevel.ERROR, message, *args, **kwargs)
    _log(LogLevel.ERROR, "异常详情:")
    traceback.print_exc(file=sys.stderr)
