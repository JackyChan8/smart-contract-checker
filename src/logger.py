import sys

from loguru import logger

# Логирование
logger.add(
    sys.stderr,
    colorize=True,
    format='<blue>{time}</blue> <green>{level}</green> <red>{message}</red>',
    filter='my_module',
    level='INFO',
)
logger.add(f'./logs/file_1.log', rotation='100 MB', compression='zip')
