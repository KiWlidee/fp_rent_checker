from time import sleep

import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.firefox.options import Options




def buy_account(url: str, time: int):
    options = Options()
    # Отключить загрузку изображений для ускорения
    options.set_preference("permissions.default.image", 2)

    browser = webdriver.Firefox(options=options)


    browser.get(url)

    sleep(0.7)
    settings = browser.find_element(By.CSS_SELECTOR, ".summary.entry-summary")
    select_c = settings.find_element(By.XPATH, ".//select[starts-with(@name, 'option_select_')]")
    select = Select(select_c)

    if time == 7:
        select.select_by_index(0)
    elif time == 14:
        select.select_by_index(1)
    elif time == 21:
        select.select_by_index(2)
    elif time == 28:
        select.select_by_index(3)

    button = browser.find_element(By.CLASS_NAME, "digiseller-button")

    button.click()

    sleep(1)
    handles = browser.window_handles
    browser.switch_to.window(handles[-1])
    WebDriverWait(browser, 15).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


    payment = browser.find_element(By.CLASS_NAME, "payment_method_select")

    emails = payment.find_element(By.CSS_SELECTOR, ".row.row_pn")

    email = emails.find_element(By.ID, "email")
    email.send_keys("mihailgasnikov35@gmail.com")

    email_confirm = emails.find_element(By.ID, "Re_Enter_Email")
    email_confirm.send_keys("mihailgasnikov35@gmail.com")

    pay_button = emails.find_element(By.ID, "pay_btn")
    pay_button.click()

    sleep(1)
    handles = browser.window_handles
    browser.switch_to.window(handles[-1])


    return f""
    

def get_soup(name: str) -> BeautifulSoup:
    """Get soup of page"""

    name = name.replace(" ", "-")

    try:
        link_change = False
        res = requests.get(f"https://gorent.shop/product/{name}-arenda-akkaunta-steam/")
        if res.status_code != 200:
            print("🔄 Link changed")
            res = requests.get(f"https://gorent.shop/product/{name}-arenda-steam/")
            link_change = True
            if res.status_code != 200:
                link = f"https://gorent.shop/product/{name}-arenda-steam/"
                return "Cannot connect to link", link
        soup = BeautifulSoup(res.text, "lxml")
        if link_change:
            return soup, True
        return soup, False
    
    except Exception as e:
        return f"Error {e}"
    

def find_product_info(name: str, soup: BeautifulSoup) -> str:
    button_text = soup[0].find("div", class_="summary entry-summary")
    if "Будет доступен:" in button_text.text:
        return "❌ Аккаунт занят"
        
    if soup[1]:
        print("🔎 Opened changed link")
        link = f"https://gorent.shop/product/{name}-arenda-steam/"
    else:
        print("🌐 Opened link")
        link = f"https://gorent.shop/product/{name}-arenda-akkaunta-steam/"
    return "✅ Аккаунт доступен", link



if __name__  == "__main__":
    name = input("Введите полное название игры: ").strip()
    name = name.replace(" ", "-")
    name = name.replace(":", "").lower()

    soup = get_soup(name)
    if soup[0] != "Cannot connect to link":
        status = find_product_info(name, soup)
        if status[0] != "❌ Аккаунт занят":
            time = int(input("Введите колличество дней аренды (7/14/21/28): "))
            if time == 7 or time == 14 or time == 21 or time == 28:
                buy_account(status[1], time)
            else:
                print(f"Вы неправильно ввели колличество дней аренды: {time}")
    else:
        print(f"⚠️  Не удалось открыть ссылку: {soup[1]}")