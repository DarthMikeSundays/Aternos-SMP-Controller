from env_handler import ATERNOS_ACCOUNT
from time import sleep
from random import randint

import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

options = Options()

options.add_argument("--disable-notifications")

MILLISSECONDS_IN_A_SECOND = 1000
DRIVER = uc.Chrome(options=options)
# options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

ATERNOS_URL = "https://aternos.org/:en/"
CHROME_PASSWORD_SETTINGS_URL = "chrome://settings/passwords"


def perform_web_scraping_actions(actions):
    for action in actions:
        perform_webscraping_action(action)


def perform_webscraping_action(action):
    sleep(10)
    if _check_exists_by_classname("css-1nv9q63"):
        print("hey1")
        _accept_cookies()

    if _check_exists_by_id("accept-choices"):
        print("hey2")
        _accept_privacy_policies()

    try:
        action()

    except TimeoutException:
        perform_webscraping_action(action)


def _click_element(selector_form, selector_value):

    WebDriverWait(DRIVER, 10).until(
        EC.element_to_be_clickable((selector_form, selector_value))).click()


def _click_button_by_xpath(xpath: str):
    _click_element(By.XPATH, xpath)


def _click_button_by_id(ID: str):
    _click_element(By.ID, ID)


def _click_button_by_link_text(link_text: str):
    _click_element(By.LINK_TEXT, link_text)


def _click_button_by_script_selector(script_selector: str):
    element = DRIVER.execute_script(f"return {script_selector}")
    element.click()


def _check_exists_by_something(something_checker, something_value: str):
    print(something_checker(something_value))
    return something_checker(something_value)


def _check_exists_by_classname(classname: str):
    classname_checker = DRIVER.find_elements_by_class_name
    return _check_exists_by_something(classname_checker, classname)


def _check_exists_by_id(ID: str):
    id_checker = DRIVER.find_elements_by_id
    return _check_exists_by_something(id_checker, ID)


def _go_to_aternos_site():
    DRIVER.get(ATERNOS_URL)


def _click_play_button():
    play_button = DRIVER.find_element_by_link_text('Play')
    play_button.click()


def _fill_login_form():
    username_input_element = DRIVER.find_element_by_xpath(
        "/html/body/div[3]/div/div/div[4]/div[3]/div[1]/div[2]/input")
    password_input_element = DRIVER.find_element_by_xpath(
        "/html/body/div[3]/div/div/div[4]/div[3]/div[2]/div[2]/input")

    username_input_element.send_keys(ATERNOS_ACCOUNT["username"])
    password_input_element.send_keys(ATERNOS_ACCOUNT["password"])

    _click_button_by_xpath("/html/body/div[3]/div/div/div[4]/div[3]/div[4]")


def _enter_server():
    print("entering server")
    _click_button_by_xpath(
        "/html/body/div[1]/main/section/div/div[2]/div/div[1]")


def _continue_with_ad_blocker():
    _click_button_by_xpath(
        "/html/body/span/div/div/div[2]/div[4]/div[3]/div[1]")


def _accept_cookies():
    print("accepting cookies")
    _click_button_by_xpath(
        "/html/body/div[1]/div/div/div/div[2]/div/button[2]")


def _accept_privacy_policies():
    print("accepting privacy policy")
    _click_button_by_xpath(
        "/html/body/div[3]/div/div/div/div[3]/div[2]/div[2]")


# def _accept_notifications():
 #   _click_button_by_link_text("Okay")


def _click_start_button():
    _click_button_by_id("start")


def _click_confirm_now():
    try:
        _click_button_by_xpath(
            "/html/body/div[3]/main/section/div[3]/div[4]/div[6]")
    except TimeoutException:
        pass


def _disable_password_popup():
    DRIVER.get(CHROME_PASSWORD_SETTINGS_URL)

    # password_settings_script_selector = r"document.getElementsByTagName('settings-ui')[0].shadowRoot.getElementById('main').shadowRoot.querySelector#('settings-basic-page').shadowRoot.querySelector('[page-title=Autofill]').querySelector('settings-autofill-page').shadowRoot.getElementById('pages').getElementsByClassName('iron-selected')[0].querySelector('#passwordManagerButton')"

    password_popup_toggler_script_selector = r"document.getElementsByTagName('settings-ui')[0].shadowRoot.getElementById('main').shadowRoot.querySelector('settings-basic-page').shadowRoot.querySelector('[page-title=Autofill]').querySelector('settings-autofill-page').shadowRoot.querySelector('settings-animated-pages').querySelector('[page-title=Passwords]').querySelector('#passwordSection').shadowRoot.querySelector('#passwordToggle')"

    _click_button_by_script_selector(password_popup_toggler_script_selector)


def start():
    perform_web_scraping_actions([_disable_password_popup, _go_to_aternos_site,
                                 _click_play_button, _fill_login_form, _enter_server, _click_start_button, _click_confirm_now])

    sleep(60)


if __name__ == '__main__':
    start()
