import os
from builtins import dict

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def take_screenshot(driver, name):
    os.makedirs("screenshots", exist_ok=True)
    file_path = f"screenshots/{name}.png"
    driver.save_screenshot(file_path)
    print(f"Screenshot Saved : {file_path}")


def test_login_pageTitle(driver):
    # file_path = os.path.abspath("yourcity/login.html")
    # driver.get("file://" + file_path)
    driver.get("file:///Users/khosruzzaman/Desktop/end2endProject/yourcity/login.html")
    print("Page title is :" + driver.title)


def test_login_valid_credentials(driver):
    # Load website
    driver.get("file:///Users/khosruzzaman/Desktop/end2endProject/yourcity/login.html")
    # Credentials operations
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("adm123")
    driver.find_element(By.XPATH, "//*[@id='loginForm']/button").click()

    # Take a screenshots
    take_screenshot(driver, "HomePge")

    # Sync and assertions
    WebDriverWait(driver, 10).until(EC.title_is("YourCity - City Finder"))
    actual_title = driver.title
    assert actual_title == "YourCity - City Finder", f"Title Doenst Match. found : {actual_title}"
    print("Title is : "+actual_title)

    # chek logOut

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/header/button"))).click()