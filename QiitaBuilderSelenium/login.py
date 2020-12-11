import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from QiitaBuilderSelenium import config

from logging import getLogger


def partners_login_test():
    logger = getLogger("QiitaBuilder").getChild("login")

    logger.debug("===================login begin===================")

    # 最大待機時間（秒）
    wait_time = 30

    # user_name = input('ex) shono.ishibashi \n mail_address:')
    # password = input('password:')

    user_name = 'shono.ishibashi'
    password = 'Sogeking1484?'

    driver = webdriver.Chrome()
    driver.get(config.base_url() + 'login')
    time.sleep(5)
    rp_login_button = driver.find_element_by_id('rp_login_btn')
    rp_login_button.click()

    time.sleep(5)

    # seleniumで操作できるwindowの配列
    handle_array = driver.window_handles

    # Google loginのウィンドウに切り替え
    driver.switch_to.window(handle_array[1])

    # IDを入力
    input_email_id = 'identifierId'
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.ID, input_email_id)))
    driver.find_element_by_id(input_email_id).send_keys(user_name, Keys.ENTER)
    logger.debug('input email')

    # パスワードを入力
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.NAME, 'password')))
    driver.find_element_by_name('password').send_keys(password, Keys.ENTER)
    logger.debug('input password')

    time.sleep(10)

    driver.switch_to.window(handle_array[0])

    if driver.current_url == config.base_url() + 'article':
        logger.debug('ログイン後記事一覧に遷移完了')

    logger.debug("===================login end===================")
