from logging import getLogger, StreamHandler, FileHandler, DEBUG, Formatter

from datetime import datetime
from selenium import webdriver


def logging_init():
    now = datetime.now()

    logfile = './logfiles/QiitaBuilder-' + now.strftime("%Y-%m-%d-%H%M") + '.log'

    open(logfile, 'w')

    logger = getLogger("QiitaBuilder")

    # consoleへの出力
    stream_handler = StreamHandler()
    logger.addHandler(stream_handler)
    stream_handler.setLevel(DEBUG)

    # fileへの出力
    file_handler = FileHandler(logfile)
    logger.addHandler(file_handler)
    file_handler.setLevel(DEBUG)

    # フォーマットの設定
    formatter = Formatter('%(asctime)s:%(name)s:%(lineno)d:%(levelname)s:%(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # DEBUGレベルでの出力
    logger.setLevel(DEBUG)
    logger.propagate = False

    logger.info('complete test init')


def base_url():
    return 'http://localhost:8081/'