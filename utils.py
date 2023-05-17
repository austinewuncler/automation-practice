import os

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

from dotenv import load_dotenv

load_dotenv()

WEBPAGE = "http://automationpractice.pl/index.php"
EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
PASSWORD = os.environ["PASSWORD"]


def sign_in() -> WebDriver:
    # create chrome web driver service
    service = Service(executable_path="chromedriver.exe")

    # create and return them chrome webdriver instance from service
    driver = webdriver.Chrome(service=service)

    # navigate to webpage
    driver.get(WEBPAGE)

    # wait for the elements to load
    driver.implicitly_wait(1)

    # find and click on 'Sign in' link
    sign_in_link = driver.find_element(by=By.LINK_TEXT, value="Sign in")
    sign_in_link.click()

    # find sign in form
    sign_in_form = driver.find_element(by=By.ID, value="login_form")

    # find sign in form elements
    email_input = driver.find_element(by=By.ID, value="email")
    password_input = driver.find_element(by=By.ID, value="passwd")

    # fill in sign in form
    email_input.send_keys(EMAIL_ADDRESS)
    password_input.send_keys(PASSWORD)

    # submit form
    sign_in_form.submit()

    # navigate to landing page
    home_link = driver.find_element(by=By.CSS_SELECTOR, value="a.home")
    home_link.click()

    return driver


def parse_money(amount: str) -> float:
    return float(amount.split("$")[1])
