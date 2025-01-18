from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


def save_cookies_to_txt(driver, filename="cookier.txt"):
    """
    SeleniumのWebDriverからCookieを取得し、Netscape HTTP Cookie File形式で保存します。

    Args:
        driver: Selenium WebDriverインスタンス
        filename: 保存するファイル名 (デフォルトは"cookier.txt")
    """
    with open(filename, "w") as f:
        f.write("# Netscape HTTP Cookie File\n")
        for cookie in driver.get_cookies():
            domain = cookie["domain"]
            flag = "TRUE" if domain.startswith(".") else "FALSE"
            path = cookie["path"]
            secure = "TRUE" if cookie["secure"] else "FALSE"
            expiry = int(time.time()) + 3600 * 24 * 7
            name = cookie["name"]
            value = cookie["value"]

            f.write(f"{domain}\t{flag}\t{path}\t{secure}\t{expiry}\t{name}\t{value}\n")


def login_nicovideo(driver, email, password):
    """
    ニコニコ動画にログインします。

    Args:
        driver: Selenium WebDriverインスタンス
        email: ニコニコ動画のメールアドレス
        password: ニコニコ動画のパスワード
    """

    driver.get("https://account.nicovideo.jp/login?site=niconicoq")

    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "input__mailtel"))
    )
    email_field.send_keys(email)

    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "input__password"))
    )
    password_field.send_keys(password)

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login__submit"))
    )

    login_button.click()

    WebDriverWait(driver, 60 * 10).until(EC.title_contains("ニコニコQ"))


def main():
    """
    メイン関数
    """
    driver = webdriver.Chrome()

    email = os.environ.get("NICONICO_EMAIL")
    password = os.environ.get("NICONICO_PASSWORD")

    if not email or not password:
        email = input("ニコニコ動画のメールアドレスを入力してください: ")
        password = input("ニコニコ動画のパスワードを入力してください: ")

    try:
        login_nicovideo(driver, email, password)
        save_cookies_to_txt(driver)
        print("Cookieをcookier.txtに保存しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
