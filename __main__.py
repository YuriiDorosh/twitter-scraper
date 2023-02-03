# selenium`s imports
from selenium import webdriver  # import webdriver for starting the Chrome page
from selenium.webdriver.common.by import By  # import By for using xpath
from selenium.webdriver.common.keys import Keys  # import Keys for ENTER the data
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # import Options to prevent session expiration
from webdriver_manager.chrome import ChromeDriverManager  # import ChromeDriverManager for download driver
# others imports
from settings import *  # import all from settings.py
from paths import *  # import all from paths.py
from bs4 import BeautifulSoup  # import BeautifulSoup for scraping
import time  # import time for take a break of process

"Settings of driver"
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
s = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=s, chrome_options=chrome_options)
driver.get(twitter_link)


def very_short_pause():
    return time.sleep(1)


def short_pause():
    return time.sleep(3)


def long_pause():
    return time.sleep(10)


def login() -> None:
    driver.find_element(By.XPATH, log_in_button_path).click()  # search and click on the login button
    short_pause()
    send_email = driver.find_element(By.XPATH, send_email_path)  # search email input field
    send_email.send_keys(bot_email)  # input email
    very_short_pause()
    driver.find_element(By.XPATH, next_button_path).click()  # finish authorization login and click to next page
    short_pause()


def verification() -> None:
    verify_button = driver.find_element(By.XPATH, verify_button_path)  # search verification input field
    if verify_button:
        verify_button.send_keys(bot_username)  # if Twitter ask us to verification - input username
        very_short_pause()
        driver.find_element(By.XPATH, next_button_verify_path).click()  # finish verification and click to next page
        short_pause()


def password() -> None:
    short_pause()
    send_password = driver.find_element(By.XPATH, send_password_path)  # search password input field
    if not send_password:  # if send password field cannot be found -
        verification()  # the verification window does not allow you to enter a password
    send_password.send_keys(bot_password)  # input password
    very_short_pause()
    driver.find_element(By.XPATH, send_all_data_path).click()  # finish verification - send all data


def search_account() -> None:
    short_pause()
    search_twitter_button = driver.find_element(By.XPATH, search_twitter_button_path)  # search button to search
    if not search_twitter_button:  # if search button cannot be found -
        driver.find_element(By.XPATH,
                            close_two_factor_authentication_path).click()  # - close two-factor authentication window
        very_short_pause()
    search_twitter_button.click()  # click button for activate input field
    very_short_pause()
    search_twitter_button.send_keys(account)  # input nickname of account
    very_short_pause()
    search_twitter_button.send_keys(Keys.ENTER)  # press enter to finish searching
    very_short_pause()
    driver.find_element(By.XPATH, select_people_button_path).click()  # select people button to find people
    short_pause()
    driver.find_element(By.XPATH, select_first_account_path).click()  # click on the most popular account
    short_pause()


def take_screenshot() -> None:
    # take screenshot for first post on the page and save it
    driver.find_element(By.XPATH, last_post_path).screenshot(
        folder + f'{account}.png')  # with account nickname name`s + png extension


def parsing_page() -> list:
    soup = BeautifulSoup(driver.page_source, 'lxml')  # getting html of the page
    postings = soup.find_all('div', class_=class_path)  # find all posts of the account
    tweets = []  # make an empty list for adding post to it
    while True:
        for post in postings:
            tweets.append(post.text)  # add post to list
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # scroll to the end of page
        very_short_pause()

        if len(tweets) > number_of_posts:  # limit the number of posts
            break
    return tweets


def writing_data(tweets_list) -> None:
    f = open(folder + f'{account}.txt', 'w')  # open txt file for writing with name of the account
    try:
        for item in tweets_list:
            f.write("%s\n" % item)  # write the list elements to a file(posts)
            f.write('*' * 100 + '\n')
    finally:
        f.close()  # close the file in any case


def main() -> None:
    long_pause()
    '''Authorization stage'''
    login()
    password()
    '''After authorizations'''
    search_account()
    '''On the account`s page'''
    take_screenshot()
    writing_data(parsing_page())


if __name__ == '__main__':
    main()
