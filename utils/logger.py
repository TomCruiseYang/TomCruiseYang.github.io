import os
import sys
from loguru import logger

# 移除默认配置（避免重复输出）
logger.remove()

# 控制台输出配置（带高亮）
logger.add(
    sink=sys.stdout,
    format="<g>{time:YYYY-MM-DD HH:mm:ss}</g> | <level>{level:^8}</level> | <cyan>{module}:{line}</cyan> - <level>{message}</level>",
    colorize=True,
    level="DEBUG",
    enqueue=True  # 关键：确保异步安全
)

# 文件输出配置（按天轮转）
log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)  # 自动创建日志目录

logger.add(
    sink=os.path.join(log_dir, "OLS_AGENT_{time:YYYY-MM-DD}.log"),  # 按天命名文件
    rotation="00:00",           # 每日零点轮转
    retention="7 days",         # 保留7天日志
    format="{time:YYYY-MM-DD HH:mm:ss} | {level:^8} | {module}:{line} - {message}",
    level="INFO",
    enqueue=True,               # 异步安全写入
    backtrace=True,             # 记录异常堆栈
    diagnose=False              # 生产环境关闭敏感信息
)