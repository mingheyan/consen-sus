import sys

from loguru import logger

logger.configure(handlers=[
    {
        "sink": sys.stderr,
        "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} |<lvl>{level:8}</>| {name} : {module}:{line:4} | <cyan>{extra[module_name]}</> | - <lvl>{message}</>",
        "colorize": True,
    },
    {
        "sink": 'first.log',
        "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} |{level:8}| {name} : {module}:{line:4} | {extra[module_name]} | - {message}",
        "colorize": False
    },
])

