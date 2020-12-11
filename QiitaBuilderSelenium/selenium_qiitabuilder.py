import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import selenium
from QiitaBuilderSelenium import config
from logging import getLogger
import json
import pyperclip

wait_time = 5


class SeleniumQiitaBuilder:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def close(self):
        self.driver.quit()

    def login_test(self):
        logger = getLogger("QiitaBuilder").getChild("login")

        logger.debug("===================login begin===================")

        login_data = json.load(open('./test_case_data/login.json', 'r'))

        user_name = login_data['username']
        password = login_data['password']

        self.driver.get(config.base_url() + 'login')
        time.sleep(5)
        rp_login_button = self.driver.find_element_by_id('rp_login_btn')
        rp_login_button.click()

        time.sleep(5)

        # seleniumで操作できるwindowの配列
        handle_array = self.driver.window_handles

        # Google loginのウィンドウに切り替え
        self.driver.switch_to.window(handle_array[1])

        # IDを入力
        input_email_id = 'identifierId'
        WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located((By.ID, input_email_id)))
        self.driver.find_element_by_id(input_email_id).send_keys(user_name, Keys.ENTER)
        logger.debug('input email')

        # パスワードを入力
        WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located((By.NAME, 'password')))
        time.sleep(1)
        self.driver.find_element_by_name('password').send_keys(password, Keys.ENTER)
        logger.debug('input password')

        time.sleep(5)

        self.driver.switch_to.window(handle_array[0])

        if self.driver.current_url == config.base_url() + 'article':
            logger.debug('ログイン後記事一覧に遷移完了')

        logger.debug("===================login end===================")

    def article_new(self):

        # ロギング初期設定
        logger = getLogger("QiitaBuilder").getChild("article_new")

        # 記事新規作成画面のURL
        article_new_url = config.base_url() + 'article/new'

        # headerの記事投稿ボタンのxpath
        button_to_article_new_xpath = '//*[@id="app"]/div/div/header/div/div[3]/button[2]'

        # headerの新規投稿ボタンが表示されるまで待機
        WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, button_to_article_new_xpath)))
        time.sleep(1)

        logger.debug('===================article_new begin===================')

        self.driver.find_element_by_xpath(button_to_article_new_xpath).click()

        # タイトルのinputのxpath
        input_title_xpath = '//*[@placeholder="タイトル"]'
        # 記事内容のinputのxpath
        input_content_xpath = '//*[@placeholder="markdown記法で書いてください"]'
        # タグのinputのxpath
        input_tags_xpath = '/html/body/div/div[1]/main/div/div/div/form/div[1]/div[1]/div[2]/div/div[1]/div[1]/' \
                           'div[1]/input'
        # 記事を公開ボタンのxpath
        save_button_xpath = '/html/body/div/div/main/div/div/div/form/div[1]/div[2]/div/div[1]/button'

        # 新規投稿画面のタイトルのinputが表示されるまで待機
        WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, input_title_xpath)))
        time.sleep(1)

        if self.driver.current_url == article_new_url:
            logger.info('ヘッダーから記事新規作成画面への遷移完了')

        # 入力データの読み込み
        article_new_data = json.load(open('./test_case_data/article_new.json', 'r'))

        # comboboxのxpath
        combobox_xpath = '/html/body/div/div[1]/main/div/div/div/form/div[1]/div[1]/div[2]/div/div[1]/div[1]/div[1]'

        # タイトルのエラーメッセージ
        input_title_blank_error_text = '必ず入力してください'
        input_title_over_error_text = '255文字以内で入力してください'

        # タグのエラーメッセージ
        input_tags_blank_error_text = '1つ以上入力してください'
        input_tags_over_error_text = '5つまで入力してください'

        # 記事内容のエラーメッセージ
        input_content_blank_error_text = '必ず入力してください'
        input_content_over_error_text = '20000字以内で入力してください'

        # テストケースを実行するfunction
        def run_tc(tc):
            time.sleep(0.5)
            # 初期化
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, input_title_xpath)))
            time.sleep(0.5)

            self.driver.find_element_by_xpath(input_title_xpath).send_keys(Keys.COMMAND, 'a')
            self.driver.find_element_by_xpath(input_title_xpath).send_keys(Keys.DELETE)
            self.driver.find_element_by_xpath(input_title_xpath).send_keys(tc["title"])
            pyperclip.copy(tc['content'])
            self.driver.find_element_by_xpath(input_content_xpath).send_keys(Keys.COMMAND, 'a')
            self.driver.find_element_by_xpath(input_content_xpath).send_keys(Keys.DELETE)
            self.driver.find_element_by_xpath(input_content_xpath).send_keys(Keys.COMMAND, 'v')
            self.driver.find_element_by_xpath(combobox_xpath).click()
            for tag in tc['tags']:
                self.driver.find_element_by_xpath(input_tags_xpath).send_keys(tag, Keys.ENTER)
                time.sleep(0.1)
            self.driver.find_element_by_xpath(save_button_xpath).click()
            time.sleep(0.5)

        logger.debug('-------------------TC1-------------------')
        run_tc(article_new_data['TC1'])
        if self.driver.find_element_by_xpath(
                '/html/body/div/div/main/div/div/div/form/div[1]/div[1]/div[1]/div/div[2]/div[1]/div/div').text == input_title_blank_error_text:
            logger.info('Pass')
        else:
            logger.error('Error')

        logger.debug('-------------------TC2-------------------')
        run_tc(article_new_data['TC2'])
        time.sleep(1)
        # エラーメッセージの確認
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div/div/main/div/div/div/form/div[3]/div[1]/div[1]/div/div[2]/div[1]/div/div')
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        # 投稿後の画面遷移
        time.sleep(1)
        if self.driver.current_url == config.base_url() + 'article':
            logger.info('投稿後、画面遷移')
        elif self.driver.current_url == article_new_url:
            logger.error('画面遷移失敗')
        else:
            logger.error('予期しない画面遷移')
            logger.error(self.driver.current_url)

        if self.driver.current_url != article_new_url:
            self.driver.find_element_by_xpath(button_to_article_new_xpath).click()
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, input_title_xpath)))

        logger.debug('-------------------TC3-------------------')
        run_tc(article_new_data['TC3'])
        # エラーメッセージの確認
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div/div/main/div/div/div/form/div[3]/div[1]/div[1]/div/div[2]/div[1]/div/div')
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        # 投稿後の画面遷移
        time.sleep(1)
        if self.driver.current_url == config.base_url() + 'article':
            logger.info('画面正常遷移')
        elif self.driver.current_url == article_new_url:
            logger.error('画面遷移失敗')
        else:
            logger.error('予期しない画面遷移')
            logger.error(self.driver.current_url)
        time.sleep(1)
        if self.driver.current_url != article_new_url:
            self.driver.find_element_by_xpath(button_to_article_new_xpath).click()
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, input_title_xpath)))

        logger.debug('-------------------TC4-------------------')
        run_tc(article_new_data['TC4'])
        time.sleep(1)
        # エラーメッセージの確認
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div/div/main/div/div/div/form/div[3]/div[1]/div[1]/div/div[2]/div[1]/div/div')
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        # 投稿後の画面遷移
        time.sleep(1)
        if self.driver.current_url == config.base_url() + 'article':
            logger.info('画面正常遷移')
        elif self.driver.current_url == article_new_url:
            logger.error('画面遷移失敗')
        else:
            logger.error('予期しない画面遷移')
            logger.error(self.driver.current_url)
        time.sleep(1)
        if self.driver.current_url != article_new_url:
            self.driver.find_element_by_xpath(button_to_article_new_xpath).click()
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, input_title_xpath)))

        logger.debug('-------------------TC5-------------------')
        run_tc(article_new_data['TC5'])
        if self.driver.find_element_by_xpath(
                '/html/body/div/div/main/div/div/div/form/div[1]/div[1]/div[1]/div/div[2]/div[1]/div/div').text \
                == input_title_over_error_text:
            logger.info('Pass')
        else:
            logger.error('Error')

        logger.debug('-------------------TC6-------------------')
        run_tc(article_new_data['TC6'])
        if self.driver.find_element_by_xpath(
                '/html/body/div/div/main/div/div/div/form/div[1]/div[1]/div[1]/div/div[2]/div[1]/div/div').text \
                == input_title_over_error_text:
            logger.info('Pass')
        else:
            logger.error('Error')

        logger.debug('-------------------TC7-------------------')
        run_tc(article_new_data['TC7'])
        if self.driver.find_element_by_xpath(
                '/html/body/div/div[1]/main/div/div/div/form/div[3]/main/div/div/div/div/div[2]/div[1]/div/div').text \
                == input_content_blank_error_text:
            logger.info('Pass')
        else:
            logger.error('Error')

        logger.debug('-------------------TC8-------------------')
        run_tc(article_new_data['TC8'])
        time.sleep(1)
        # エラーメッセージの確認
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div/div[1]/main/div/div/div/form/div[3]/main/div/div/div/div/div[2]/div[1]/div/div')
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        # 投稿後の画面遷移
        time.sleep(1)
        if self.driver.current_url == config.base_url() + 'article':
            logger.info('画面正常遷移')
        elif self.driver.current_url == article_new_url:
            logger.error('画面遷移失敗')
        else:
            logger.error('予期しない画面遷移')
            logger.error(self.driver.current_url)
        time.sleep(1)
        if self.driver.current_url != article_new_url:
            self.driver.find_element_by_xpath(button_to_article_new_xpath).click()
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, input_title_xpath)))

        logger.debug('-------------------TC9-------------------')
        run_tc(article_new_data['TC9'])
        time.sleep(1)
        # エラーメッセージの確認
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div/div[1]/main/div/div/div/form/div[3]/main/div/div/div/div/div[2]/div[1]/div/div')
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        # 投稿後の画面遷移
        time.sleep(1)
        if self.driver.current_url == config.base_url() + 'article':
            logger.info('画面正常遷移')
        elif self.driver.current_url == article_new_url:
            logger.error('画面遷移失敗')
        else:
            logger.error('予期しない画面遷移')
            logger.error(self.driver.current_url)
        time.sleep(1)
        if self.driver.current_url != article_new_url:
            self.driver.find_element_by_xpath(button_to_article_new_xpath).click()
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, input_title_xpath)))

        logger.debug('-------------------TC10-------------------')
        run_tc(article_new_data['TC10'])
        time.sleep(1)
        # エラーメッセージの確認
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div/div[1]/main/div/div/div/form/div[3]/main/div/div/div/div/div[2]/div[1]/div/div')
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        # 投稿後の画面遷移
        time.sleep(1)
        if self.driver.current_url == config.base_url() + 'article':
            logger.info('画面正常遷移')
        elif self.driver.current_url == article_new_url:
            logger.error('画面遷移失敗')
        else:
            logger.error('予期しない画面遷移')
            logger.error(self.driver.current_url)
        time.sleep(1)
        if self.driver.current_url != article_new_url:
            self.driver.find_element_by_xpath(button_to_article_new_xpath).click()
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, input_title_xpath)))

        logger.debug('-------------------TC11-------------------')
        run_tc(article_new_data['TC11'])

        if self.driver.find_element_by_xpath(
                '/html/body/div/div[1]/main/div/div/div/form/div[3]/main/div/div/div/div/div[2]/div[1]/div/div').text \
                == input_content_over_error_text:
            logger.info('Pass')
        else:
            logger.error('Error')

        logger.debug('-------------------TC12-------------------')
        self.driver.get(article_new_url)
        run_tc(article_new_data['TC12'])

        if self.driver.find_element_by_xpath(
                '/html/body/div/div[1]/main/div/div/div/form/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div').text \
                == input_tags_blank_error_text:
            logger.info('Pass')
        else:
            logger.error('Error')

        logger.debug('-------------------TC13-------------------')
        run_tc(article_new_data['TC13'])
        time.sleep(1)
        # エラーメッセージの確認
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div/div[1]/main/div/div/div/form/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div')
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        # 投稿後の画面遷移
        time.sleep(1)
        if self.driver.current_url == config.base_url() + 'article':
            logger.info('画面正常遷移')
        elif self.driver.current_url == article_new_url:
            logger.error('画面遷移失敗')
        else:
            logger.error('予期しない画面遷移')
            logger.error(self.driver.current_url)
        time.sleep(1)
        if self.driver.current_url != article_new_url:
            self.driver.find_element_by_xpath(button_to_article_new_xpath).click()
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, input_title_xpath)))

        logger.debug('-------------------TC14-------------------')
        run_tc(article_new_data['TC14'])
        time.sleep(1)
        # エラーメッセージの確認
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div/div[1]/main/div/div/div/form/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div')
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        # 投稿後の画面遷移
        time.sleep(1)
        if self.driver.current_url == config.base_url() + 'article':
            logger.info('画面正常遷移')
        elif self.driver.current_url == article_new_url:
            logger.error('画面遷移失敗')
        else:
            logger.error('予期しない画面遷移')
            logger.error(self.driver.current_url)
        time.sleep(1)
        if self.driver.current_url != article_new_url:
            self.driver.find_element_by_xpath(button_to_article_new_xpath).click()
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, input_title_xpath)))

        logger.debug('-------------------TC15-------------------')
        run_tc(article_new_data['TC15'])
        time.sleep(1)
        # エラーメッセージの確認
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div/div[1]/main/div/div/div/form/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div')
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        # 投稿後の画面遷移
        time.sleep(1)
        if self.driver.current_url == config.base_url() + 'article':
            logger.info('画面正常遷移')
        elif self.driver.current_url == article_new_url:
            logger.error('画面遷移失敗')
        else:
            logger.error('予期しない画面遷移')
            logger.error(self.driver.current_url)
        time.sleep(1)
        if self.driver.current_url != article_new_url:
            self.driver.find_element_by_xpath(button_to_article_new_xpath).click()
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, input_title_xpath)))

        logger.debug('-------------------TC16-------------------')
        run_tc(article_new_data['TC16'])

        if self.driver.find_element_by_xpath(
                '/html/body/div/div[1]/main/div/div/div/form/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div').text \
                == input_tags_over_error_text:
            logger.info('Pass')
        else:
            logger.error('Error')

        logger.debug('-------------------TC17-------------------')
        run_tc(article_new_data['TC17'])

        if self.driver.find_element_by_xpath(
                '/html/body/div/div[1]/main/div/div/div/form/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div').text \
                == input_tags_over_error_text:
            logger.info('Pass')
        else:
            logger.error('Error')

        logger.debug('===================article_new end===================')

    def article_edit(self):
        self.driver.get(config.base_url() + 'article/')

        def to_edit_from_detail():
            WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable((By.XPATH, title_xpath)))
            self.driver.find_element_by_xpath(title_xpath).click()
            WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable((By.XPATH, edit_hamburger_menu_xpath)))
            self.driver.find_element_by_xpath(edit_hamburger_menu_xpath).click()
            WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable((By.XPATH, edit_button)))
            self.driver.find_element_by_xpath(edit_button).click()
            time.sleep(2)

        # ロギング初期設定
        logger = getLogger("QiitaBuilder").getChild("article_edit")

        # 記事新規作成画面のURL
        article_edit_url = config.base_url() + 'article/193/edit'

        # 既存の記事のタイトルのxpath
        title_xpath = '/html/body/div/div[1]/main/div/div/div[4]/div[1]/div[2]/div/div/div[3]/div[1]/div[1]'
        edit_hamburger_menu_xpath = '/html/body/div/div[1]/main/div/div/div/div[8]/div[2]/div/div[1]/div/div[1]/div' \
                                    '[1]/div[5]/button'
        edit_button = '/html/body/div/div[2]/div/div[1]/div'

        # 既存の記事のタイトルが表示されるまで待機
        WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, title_xpath)))
        time.sleep(1)

        logger.debug('===================article_edit begin===================')

        to_edit_from_detail()

        # タイトルのinputのxpath
        input_title_xpath = '//*[@placeholder="タイトル"]'
        # 記事内容のinputのxpath
        input_content_xpath = '//*[@placeholder="markdown記法で書いてください"]'
        # タグのinputのxpath
        input_tags_xpath = '/html/body/div/div[1]/main/div/div/div/form/div[1]/div[1]/div[2]/div/div[1]/div[1]/' \
                           'div[1]/input'
        # 記事を公開ボタンのxpath
        save_button_xpath = '/html/body/div/div[1]/main/div/div/div[3]/form/div[1]/div[2]/div/div[1]/button'

        # 新規投稿画面のタイトルのinputが表示されるまで待機
        WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, input_title_xpath)))
        time.sleep(1)

        if self.driver.current_url == article_edit_url:
            logger.info('ヘッダーから記事新規作成画面への遷移完了')

        # 入力データの読み込み
        article_new_data = json.load(open('./test_case_data/article_new.json', 'r'))

        # comboboxのxpath
        combobox_xpath = '/html/body/div/div[1]/main/div/div/div/form/div[1]/div[1]/div[2]/div/div[1]/div[1]/div[1]'

        # タイトルのエラーメッセージ
        input_title_blank_error_text = '必ず入力してください'
        input_title_over_error_text = '255文字以内で入力してください'

        # タグのエラーメッセージ
        input_tags_blank_error_text = '1つ以上入力してください'
        input_tags_over_error_text = '5つまで入力してください'

        # 記事内容のエラーメッセージ
        input_content_blank_error_text = '必ず入力してください'
        input_content_over_error_text = '20000字以内で入力してください'

        # テストケースを実行するfunction
        def run_tc(tc):
            time.sleep(0.5)
            # 初期化
            WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable((By.XPATH, input_title_xpath)))
            time.sleep(0.5)

            self.driver.find_element_by_xpath(input_title_xpath).send_keys(Keys.COMMAND, 'a')
            self.driver.find_element_by_xpath(input_title_xpath).send_keys(Keys.DELETE)
            self.driver.find_element_by_xpath(input_title_xpath).send_keys(tc["title"])
            pyperclip.copy(tc['content'])
            self.driver.find_element_by_xpath(input_content_xpath).send_keys(Keys.COMMAND, 'a')
            self.driver.find_element_by_xpath(input_content_xpath).send_keys(Keys.DELETE)
            self.driver.find_element_by_xpath(input_content_xpath).send_keys(Keys.COMMAND, 'v')
            self.driver.find_element_by_xpath(combobox_xpath).click()
            for i in range(20):
                self.driver.find_element_by_xpath(input_tags_xpath).send_keys(Keys.DELETE)

            for tag in tc['tags']:
                self.driver.find_element_by_xpath(input_tags_xpath).send_keys(tag, Keys.ENTER)
            self.driver.find_element_by_xpath(save_button_xpath).click()
            time.sleep(0.5)

        logger.debug('-------------------TC1-------------------')
        run_tc(article_new_data['TC1'])
        if self.driver.find_element_by_xpath(
                '/html/body/div/div/main/div/div/div/form/div[1]/div[1]/div[1]/div/div[2]/div[1]/div/div').text == input_title_blank_error_text:
            logger.info('Pass')
        else:
            logger.error('Error')

        logger.debug('-------------------TC2-------------------')
        run_tc(article_new_data['TC2'])
        time.sleep(1)
        # エラーメッセージの確認
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div/div/main/div/div/div/form/div[3]/div[1]/div[1]/div/div[2]/div[1]/div/div')
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        # 投稿後の画面遷移
        time.sleep(1)
        if self.driver.current_url == config.base_url() + 'article':
            logger.info('投稿後、画面遷移')
        elif self.driver.current_url == article_edit_url:
            logger.error('画面遷移失敗')
        else:
            logger.error('予期しない画面遷移')
            logger.error(self.driver.current_url)

        if self.driver.current_url != article_edit_url:
            to_edit_from_detail()

        WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, input_title_xpath)))

        logger.debug('-------------------TC3-------------------')
        run_tc(article_new_data['TC3'])
        # エラーメッセージの確認
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div/div/main/div/div/div/form/div[3]/div[1]/div[1]/div/div[2]/div[1]/div/div')
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        # 投稿後の画面遷移
        time.sleep(1)
        if self.driver.current_url == config.base_url() + 'article':
            logger.info('画面正常遷移')
        elif self.driver.current_url == article_edit_url:
            logger.error('画面遷移失敗')
        else:
            logger.error('予期しない画面遷移')
            logger.error(self.driver.current_url)
        time.sleep(1)
        if self.driver.current_url != article_edit_url:
            to_edit_from_detail()
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, input_title_xpath)))

        logger.debug('-------------------TC4-------------------')
        run_tc(article_new_data['TC4'])
        time.sleep(1)
        # エラーメッセージの確認
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div/div/main/div/div/div/form/div[3]/div[1]/div[1]/div/div[2]/div[1]/div/div')
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        # 投稿後の画面遷移
        time.sleep(1)
        if self.driver.current_url == config.base_url() + 'article':
            logger.info('画面正常遷移')
        elif self.driver.current_url == article_edit_url:
            logger.error('画面遷移失敗')
        else:
            logger.error('予期しない画面遷移')
            logger.error(self.driver.current_url)
        time.sleep(1)
        if self.driver.current_url != article_edit_url:
            to_edit_from_detail()
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, input_title_xpath)))

        logger.debug('-------------------TC5-------------------')
        run_tc(article_new_data['TC5'])
        if self.driver.find_element_by_xpath(
                '/html/body/div/div/main/div/div/div/form/div[1]/div[1]/div[1]/div/div[2]/div[1]/div/div').text \
                == input_title_over_error_text:
            logger.info('Pass')
        else:
            logger.error('Error')

        logger.debug('-------------------TC6-------------------')
        run_tc(article_new_data['TC6'])
        if self.driver.find_element_by_xpath(
                '/html/body/div/div/main/div/div/div/form/div[1]/div[1]/div[1]/div/div[2]/div[1]/div/div').text \
                == input_title_over_error_text:
            logger.info('Pass')
        else:
            logger.error('Error')

        logger.debug('-------------------TC7-------------------')
        run_tc(article_new_data['TC7'])
        if self.driver.find_element_by_xpath(
                '/html/body/div/div[1]/main/div/div/div/form/div[3]/main/div/div/div/div/div[2]/div[1]/div/div').text \
                == input_content_blank_error_text:
            logger.info('Pass')
        else:
            logger.error('Error')

        logger.debug('-------------------TC8-------------------')
        run_tc(article_new_data['TC8'])
        time.sleep(1)
        # エラーメッセージの確認
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div/div[1]/main/div/div/div/form/div[3]/main/div/div/div/div/div[2]/div[1]/div/div')
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        # 投稿後の画面遷移
        time.sleep(1)
        if self.driver.current_url == config.base_url() + 'article':
            logger.info('画面正常遷移')
        elif self.driver.current_url == article_edit_url:
            logger.error('画面遷移失敗')
        else:
            logger.error('予期しない画面遷移')
            logger.error(self.driver.current_url)
        time.sleep(1)
        if self.driver.current_url != article_edit_url:
            to_edit_from_detail()
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, input_title_xpath)))

        logger.debug('-------------------TC9-------------------')
        run_tc(article_new_data['TC9'])
        time.sleep(1)
        # エラーメッセージの確認
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div/div[1]/main/div/div/div/form/div[3]/main/div/div/div/div/div[2]/div[1]/div/div')
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        # 投稿後の画面遷移
        time.sleep(1)
        if self.driver.current_url == config.base_url() + 'article':
            logger.info('画面正常遷移')
        elif self.driver.current_url == article_edit_url:
            logger.error('画面遷移失敗')
        else:
            logger.error('予期しない画面遷移')
            logger.error(self.driver.current_url)
        time.sleep(1)
        if self.driver.current_url != article_edit_url:
            to_edit_from_detail()
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, input_title_xpath)))

        logger.debug('-------------------TC10-------------------')
        run_tc(article_new_data['TC10'])
        time.sleep(1)
        # エラーメッセージの確認
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div/div[1]/main/div/div/div/form/div[3]/main/div/div/div/div/div[2]/div[1]/div/div')
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        # 投稿後の画面遷移
        time.sleep(1)
        if self.driver.current_url == config.base_url() + 'article':
            logger.info('画面正常遷移')
        elif self.driver.current_url == article_edit_url:
            logger.error('画面遷移失敗')
        else:
            logger.error('予期しない画面遷移')
            logger.error(self.driver.current_url)
        time.sleep(1)
        if self.driver.current_url != article_edit_url:
            to_edit_from_detail()
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, input_title_xpath)))

        logger.debug('-------------------TC11-------------------')
        run_tc(article_new_data['TC11'])

        if self.driver.find_element_by_xpath(
                '/html/body/div/div[1]/main/div/div/div/form/div[3]/main/div/div/div/div/div[2]/div[1]/div/div').text \
                == input_content_over_error_text:
            logger.info('Pass')
        else:
            logger.error('Error')

        logger.debug('-------------------TC12-------------------')

        self.driver.get(article_edit_url)
        WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, input_title_xpath)))
        run_tc(article_new_data['TC12'])

        if self.driver.find_element_by_xpath(
                '/html/body/div/div/main/div/div/div[3]/form/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div').text \
                == input_tags_blank_error_text:
            logger.info('Pass')
        else:
            logger.error('Error')

        logger.debug('-------------------TC13-------------------')
        run_tc(article_new_data['TC13'])
        time.sleep(1)
        # エラーメッセージの確認
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div/div/main/div/div/div[3]/form/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div')
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        # 投稿後の画面遷移
        time.sleep(1)
        if self.driver.current_url == config.base_url() + 'article':
            logger.info('画面正常遷移')
        elif self.driver.current_url == article_edit_url:
            logger.error('画面遷移失敗')
        else:
            logger.error('予期しない画面遷移')
            logger.error(self.driver.current_url)
        time.sleep(1)
        if self.driver.current_url != article_edit_url:
            to_edit_from_detail()
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, input_title_xpath)))

        logger.debug('-------------------TC14-------------------')
        run_tc(article_new_data['TC14'])
        time.sleep(1)
        # エラーメッセージの確認
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div/div/main/div/div/div[3]/form/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div')
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        # 投稿後の画面遷移
        time.sleep(1)
        if self.driver.current_url == config.base_url() + 'article':
            logger.info('画面正常遷移')
        elif self.driver.current_url == article_edit_url:
            logger.error('画面遷移失敗')
        else:
            logger.error('予期しない画面遷移')
            logger.error(self.driver.current_url)
        time.sleep(1)
        if self.driver.current_url != article_edit_url:
            to_edit_from_detail()
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, input_title_xpath)))

        logger.debug('-------------------TC15-------------------')
        run_tc(article_new_data['TC15'])
        time.sleep(1)
        # エラーメッセージの確認
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div/div/main/div/div/div[3]/form/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div')
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        # 投稿後の画面遷移
        time.sleep(1)
        if self.driver.current_url == config.base_url() + 'article':
            logger.info('画面正常遷移')
        elif self.driver.current_url == article_edit_url:
            logger.error('画面遷移失敗')
        else:
            logger.error('予期しない画面遷移')
            logger.error(self.driver.current_url)
        time.sleep(1)
        if self.driver.current_url != article_edit_url:
            to_edit_from_detail()
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, input_title_xpath)))

        logger.debug('-------------------TC16-------------------')
        run_tc(article_new_data['TC16'])

        if self.driver.find_element_by_xpath(
                '/html/body/div/div/main/div/div/div[3]/form/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div').text \
                == input_tags_over_error_text:
            logger.info('Pass')
        else:
            logger.error('Error')

        logger.debug('-------------------TC17-------------------')
        run_tc(article_new_data['TC17'])

        if self.driver.find_element_by_xpath(
                '/html/body/div/div/main/div/div/div[3]/form/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div').text \
                == input_tags_over_error_text:
            logger.info('Pass')
        else:
            logger.error('Error')

        logger.debug('===================article_edit end===================')

    def feedback(self):
        driver = self.driver
        feedback_button_xpath = '/html/body/div/div[1]/main/div/div/div/div[8]/div[3]/span[2]/button'
        feedback_textarea_xpath = '/html/body/div/div[1]/main/div/div/div/div[8]/div[3]/span[1]/div/div[3]/form/div/div/div/div[1]/div/textarea'
        feedback_save_button_xpath = '/html/body/div/div[1]/main/div/div/div/div[8]/div[3]/span[1]/div/div[3]/div[2]/button'
        feedback_input_error_message_xpath = '/html/body/div/div[1]/main/div/div/div/div[8]/div[3]/span[1]/div/div[3]/form/div/div/div/div[2]/div/div/div'

        blank_error_message = 'テキストを入力してください'
        over_error_message = '2万文字以内で入力してください'

        logger = getLogger("QiitaBuilder").getChild("feedback")

        driver.get(config.base_url() + 'article/256')

        # テストケースを実行するfunction
        def run_tc(tc):
            try:
                WebDriverWait(self.driver, wait_time).until(
                    EC.element_to_be_clickable((By.XPATH, feedback_button_xpath)))
                driver.find_element_by_xpath(feedback_button_xpath).click()
            except Exception:
                pass

            # テキストをクリップボードにcopy
            pyperclip.copy(tc['content'])

            focus_script = 'document.getElementsByTagName("textarea")[0].focus();'
            driver.execute_script(focus_script);

            WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable((By.XPATH, feedback_textarea_xpath)))
            driver.find_element_by_xpath(feedback_textarea_xpath).send_keys(Keys.COMMAND, 'v')

            focus_script = 'document.getElementsByTagName("textarea")[0].blur();'
            driver.execute_script(focus_script);

            if driver.find_element_by_xpath(feedback_save_button_xpath).is_enabled():
                logger.debug('button clicked')
                driver.find_element_by_xpath(feedback_save_button_xpath).click()
            else:
                logger.debug('disable button')

        logger.debug('===================feedback begin===================')
        feedback_data = json.load(open('./test_case_data/feedback.json', 'r'))

        logger.debug('-------------------TC1-------------------')
        run_tc(feedback_data["TC1"])
        try:
            driver.find_element_by_xpath(feedback_input_error_message_xpath)
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        logger.debug('-------------------TC2-------------------')
        run_tc(feedback_data["TC2"])
        try:
            driver.find_element_by_xpath(feedback_input_error_message_xpath)
            logger.error('Error')
        except selenium.common.exceptions.NoSuchElementException:
            logger.info('Pass')

        logger.debug('-------------------TC3-------------------')
        run_tc(feedback_data["TC3"])
        if driver.find_element_by_xpath(feedback_input_error_message_xpath).text == blank_error_message:
            logger.info('Pass')
        else:
            logger.error('Error')

        logger.debug('-------------------TC4-------------------')
        run_tc(feedback_data["TC4"])
        if driver.find_element_by_xpath(feedback_input_error_message_xpath).text == blank_error_message:
            logger.info('Pass')
        else:
            logger.error('Error')

        logger.debug('-------------------TC5-------------------')
        run_tc(feedback_data["TC5"])
        if driver.find_element_by_xpath(feedback_input_error_message_xpath).text == over_error_message:
            logger.info('Pass')
        else:
            logger.error('Error')

    def check_screen_transition(self):
        logger = getLogger("QiitaBuilder").getChild("画面遷移")
        driver = self.driver
        logger.debug('===================画面遷移 header begin===================')
        logger.debug('-------------------to ranking-------------------')

        ranking_button_in_header_xpath = '/html/body/div/div[1]/div/header/div/div[3]/button[3]'
        WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.XPATH, ranking_button_in_header_xpath)))
        driver.find_element_by_xpath(ranking_button_in_header_xpath).click()
        # ランキング項目のxpath
        ranking_item_select_xpath = '/html/body/div/div[1]/main/div/div/div[1]/div[1]/div[1]/div[1]'
        WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, ranking_item_select_xpath)))

        if driver.current_url == config.base_url() + 'user/ranking':
            logger.info('ranking画面に遷移')
        else:
            logger.error('ranking画面に遷移失敗')

        logger.debug('-------------------to article list-------------------')

        article_list_button_in_header_xpath = '/html/body/div/div[1]/div/header/div/div[3]/button[1]'
        WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, article_list_button_in_header_xpath)))
        driver.find_element_by_xpath(article_list_button_in_header_xpath).click()

        article_list_search_form_path = '/html/body/div/div/main/div/div/div[3]/div/div/form'
        WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, article_list_search_form_path)))

        if driver.current_url == config.base_url() + 'article':
            logger.info('記事一覧画面に遷移')
        else:
            logger.error('記事一覧画面に遷移失敗')
