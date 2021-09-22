from env_handler import ATERNOS_ACCOUNT
from time import sleep
from random import randint

import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pyshadow.main import Shadow

from discord.ext import commands

options = uc.ChromeOptions()

options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument(
    '--no-first-run --no-service-autorun --password-store=basic')
options.add_argument("--headless")


DRIVER = uc.Chrome(options=options)
SHADOW = Shadow(DRIVER)
# brave browser: options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

ATERNOS_URL = "https://aternos.org/:en/"
CHROME_PASSWORD_SETTINGS_URL = "chrome://settings/passwords"

DEFAULT_TIMEOUT_IN_SECONDS = 10

OFFLINE_STATUS = "offline"
QUEUEING_STATUS = "queueing"
LOADING_STATUS = "loading"
ONLINE_STATUS = "online"


def perform_web_scraping_actions(actions):
    for action in actions:
        _perform_webscraping_action(action)


def _perform_webscraping_action(action):
    if _check_exists_by_classname("css-1nv9q63"):
        _accept_cookies()

    if _check_exists_by_id("accept-choices"):
        _accept_privacy_policies()

    try:
        action()

    except (ElementClickInterceptedException, TimeoutException):
        _perform_webscraping_action(action)


def get_status_from_element(element):
    element_classes = element.get_attribute("class").split(" ")
    status = element_classes[1]
    return status


def _click_button(selector_form, selector_value, timeout_in_seconds=DEFAULT_TIMEOUT_IN_SECONDS):

    WebDriverWait(DRIVER, timeout_in_seconds).until(
        EC.element_to_be_clickable((selector_form, selector_value))).click()


def _click_button_by_xpath(xpath: str):
    _click_button(By.XPATH, xpath)


def _click_button_by_id(*args):
    _click_button(By.ID, *args)


def _click_button_by_link_text(link_text: str):
    _click_button(By.LINK_TEXT, link_text)


def _click_button_by_class_name(*args):
    _click_button(By.CLASS_NAME, *args)


def _click_button_by_script_selector(script_selector: str):
    element = DRIVER.execute_script(f"return {script_selector}")
    element.click()


def _check_exists_by_something(something_checker, something_value: str):
    return something_checker(something_value)


def _check_exists_by_classname(classname: str):
    classname_checker = DRIVER.find_elements_by_class_name
    return _check_exists_by_something(classname_checker, classname)


def _check_exists_by_id(ID: str):
    id_checker = DRIVER.find_elements_by_id
    return _check_exists_by_something(id_checker, ID)


def _continue_with_ad_blocker():
    _click_button_by_xpath(
        "/html/body/span/div/div/div[2]/div[4]/div[3]/div[1]")


def _accept_cookies():
    _click_button_by_class_name("css-1litn2c")


def _accept_privacy_policies():
    _click_button_by_id("accept-choices")


# def _accept_notifications():
#   _click_button_by_link_text("Okay")

def go_to_aternos_site():
    DRIVER.get(ATERNOS_URL)


def click_play_button():
    play_button = DRIVER.find_element_by_link_text('Play')
    play_button.click()


def fill_login_form():

    WebDriverWait(DRIVER, DEFAULT_TIMEOUT_IN_SECONDS).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[4]/div[3]/div[1]/div[2]/input"))).send_keys(ATERNOS_ACCOUNT["username"])

    WebDriverWait(DRIVER, DEFAULT_TIMEOUT_IN_SECONDS).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[4]/div[3]/div[2]/div[2]/input"))).send_keys(ATERNOS_ACCOUNT["password"])

    _click_button_by_xpath("/html/body/div[3]/div/div/div[4]/div[3]/div[4]")


def enter_server():
    _click_button_by_xpath(
        "/html/body/div[1]/main/section/div/div[2]/div/div[1]")


def click_start_button():
    print("clicking")
    _click_button_by_id("start")


def click_confirm_now():
    _click_button_by_id("confirm", 120)


def disable_password_popup():
    DRIVER.get(CHROME_PASSWORD_SETTINGS_URL)
    sleep(5)
    element = SHADOW.find_element("#passwordToggle")
    element.click()

    # password_settings_script_selector = r"document.getElementsByTagName('settings-ui')[0].shadowRoot.getElementById('main').shadowRoot.querySelector#('settings-basic-page').shadowRoot.querySelector('[page-title=Autofill]').querySelector('settings-autofill-page').shadowRoot.getElementById('pages').getElementsByClassName('iron-selected')[0].querySelector('#passwordManagerButton')"

    # password_popup_toggler_script_selector = r"document.getElementsByTagName('settings-ui')[0].shadowRoot.getElementById('main').shadowRoot.querySelector('settings-basic-page').shadowRoot.querySelector('[page-title=Autofill]').querySelector('settings-autofill-page').shadowRoot.querySelector('settings-animated-pages').querySelector('[page-title=Passwords]').querySelector('#passwordSection').shadowRoot.querySelector('#passwordToggle')"

    # _click_button_by_script_selector(password_popup_toggler_script_selector)


"""
confirm now - info:
button id -> #confirm
status class -> .queueing
"""


@commands.command()
async def start(ctx):
    try:
        await ctx.send("Entering aternos account")

        perform_web_scraping_actions(
            [go_to_aternos_site, click_play_button, fill_login_form, enter_server])

        await ctx.send("Checking server status")

        status_element = WebDriverWait(DRIVER, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "status")))
        status = get_status_from_element(status_element)

        print(status)

        if status == ONLINE_STATUS:
            await ctx.send("The server is already online bruh")
            return

        await ctx.send("Continuing the opening process as the server is indeed not online yet")

        perform_web_scraping_actions([click_start_button])

        if status == QUEUEING_STATUS:
            perform_web_scraping_actions([click_confirm_now()])

        await ctx.send("Server has been successfully put online!🥳")
    except Exception as e:
        print(e)
        await ctx.send("An error has occurred. Pls try again")
