from loguru import logger

# 自定义日志格式
logger.add("my_log_file.log", format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {file}:{line} - {message}")

# 定义日志级别对应的图标
class CustomIcon:
    SUCCESS = "✅"
    ERROR = "❌"
    INFO = "🚀"

# 使用自定义图标
def log_with_icon(level, message):
    icon = CustomIcon.SUCCESS if level == "SUCCESS" else CustomIcon.ERROR if level == "ERROR" else CustomIcon.INFO
    logger.log(level, f"{icon} {message}")

# 定义一个包装器，用于添加图标到所有日志消息
def icon_wrapper(func):
    def wrapper(*args, **kwargs):
        if len(args) > 0 and isinstance(args[0], str):
            level = func.__name__.upper()
            icon = CustomIcon.SUCCESS if level == "SUCCESS" else CustomIcon.ERROR if level == "ERROR" else CustomIcon.INFO
            return func(f"{icon} {args[0]}", **kwargs)
        else:
            return func(*args, **kwargs)
    return wrapper

# 应用包装器到 logger 的所有方法
for name in ['success', 'error', 'info', 'warning', 'debug', 'trace']:
    setattr(logger, name, icon_wrapper(getattr(logger, name)))

# 现在，所有日志消息都会自动包含图标
logger.success("This is a success message")
logger.error("This is an error message")
logger.info("This is an info message")