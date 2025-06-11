from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv

service = Service("chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

base_url = "https://www.ebay.com/sch/i.html?_nkw=laptop&_sop=12&_pgn="
products = []

for page in range(1, 6):  
    url = base_url + str(page)
    print(f" Opening page {page}: {url}")
    driver.get(url)
    time.sleep(3)

    
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    
    items = driver.find_elements(By.CSS_SELECTOR, ".s-item")

    for item in items:
        try:
            title = item.find_element(By.CSS_SELECTOR, ".s-item__title").text
            price = item.find_element(By.CSS_SELECTOR, ".s-item__price").text
            link = item.find_element(By.CSS_SELECTOR, ".s-item__link").get_attribute("href")

            if title and price and link and "Shop on eBay" not in title:
                products.append([title, price, link])
        except:
            continue

driver.quit()


with open("products.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Link"])
    writer.writerows(products)

print(f"\n Done! Saved {len(products)} products from 5 pages in products.csv")
