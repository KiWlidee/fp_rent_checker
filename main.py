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
        res = requests.get(f"https://gorent.shop/product/{name}-arenda-akkaunta-steam/")
        soup = BeautifulSoup(res.text, "lxml")
        return soup
    
    except Exception as e:
        return f"Error {e}"
    

def find_product_info(name: str, soup: BeautifulSoup):
    button_text = soup.find("div", class_="summary entry-summary")
    if "Будет доступен:" in button_text.text:
        return "❌ Аккаунт занят"
        
    open(f"https://gorent.shop/product/{name}-arenda-akkaunta-steam/")
    return "✅ Аккаунт доступен"


    

if __name__  == "__main__":
    name = input("Введи полное название игры: ")
    name = name.replace(" ", "-")
    soup = get_soup(name)
    print(find_product_info(name, soup))