from QiitaBuilderSelenium.selenium_qiitabuilder import SeleniumQiitaBuilder
import QiitaBuilderSelenium.config as config


def main():
    print('start selenium')
    # 初期設定
    config.logging_init()
    sq = SeleniumQiitaBuilder()
    sq.login_test()
    sq.feedback()
    # sq.article_new()
    # sq.article_edit()
    # sq.check_screen_transition()
    sq.close()


# ガター内の緑色のボタンを押すとスクリプトを実行します。
if __name__ == '__main__':
    main()

# PyCharm のヘルプは https://www.jetbrains.com/help/pycharm/ を参照してください
