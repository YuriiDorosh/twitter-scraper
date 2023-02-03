import os  # import the library to work with the operating system
from dotenv import load_dotenv  # import function load_dotenv to hide data


load_dotenv()  # the function that extract data from .env

'''Location on the PC'''
folder = ...  # location of the folder with screenshot and posts
chrome_path = ...  # if you don`t want to use webdriver.chrome,
# url for downloading file: https://sites.google.com/chromium.org/driver/

'''Scraping settings'''
account = ...  # nickname of the account which will be searched
number_of_posts = ...  # number of scraping posts

'''Bot settings'''
bot_email = str(os.getenv('EMAIL'))  # bot`s email
bot_password = str(os.getenv('PASSWORD'))  # bot`s password
bot_username = str(os.getenv('BOT_USERNAME'))  # bot`s username
