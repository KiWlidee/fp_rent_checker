from webbrowser import open

import requests

from bs4 import BeautifulSoup


def open_page(name: str):
    """Open page with rent-name"""
    try:
        open(f"https://gorent.shop/product/{name}-arenda-akkaunta-steam/")
        return {"status": "OK"}
    
    except Exception as e:
        return f"Error {e}"
    

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
                return f"Cannot connect to link"
        soup = BeautifulSoup(res.text, "lxml")
        if link_change:
            return soup, True
        return soup, False
    
    except Exception as e:
        return f"Error {e}"
    

def find_product_info(name: str, soup: BeautifulSoup):
    button_text = soup[0].find("div", class_="summary entry-summary")
    if "Будет доступен:" in button_text.text:
        return "❌ Аккаунт занят"
        
    if soup[1]:
        print("🔎 Opened changed link")
        open(f"https://gorent.shop/product/{name}-arenda-steam/")
        return "✅ Аккаунт доступен"
    else:
        print("🌐 Opened link")
        open(f"https://gorent.shop/product/{name}-arenda-akkaunta-steam/")
        return "✅ Аккаунт доступен"



if __name__  == "__main__":
    name = input("Введите полное название игры: ")
    name = name.replace(" ", "-")
    name = name.replace(":", "").lower()
    soup = get_soup(name)
    if soup != "Cannot connect to link":
        print(find_product_info(name, soup))