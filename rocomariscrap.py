import time
import random
import requests
import pandas as pd
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from concurrent.futures import ThreadPoolExecutor

# ========= CONFIGURATION ========= #
MAX_WORKERS = 5
HEADLESS = True
BASE_URL = 'https://www.rokomari.com/book/authors'
OUTPUT_EXCEL = 'rokomari_books.xlsx'
df_lock = threading.Lock()
df = pd.DataFrame(columns=['Author', 'Author_Link', 'Followers', 'Image', 'Book_Title', 'Old_Price', 'Current_Price', 'Book_Link'])

# ========= PROXY SECTION ========= #
def collect_proxies():
    driver = webdriver.Chrome()
    driver.get('https://free-proxy-list.net/')
    time.sleep(5)
    proxy_ip_list, port_list = [], []
    for i in range(1, 20):
        try:
            ip = driver.find_element(By.XPATH, f'//*[@id="list"]/div/div[2]/div/table/tbody/tr[{i}]/td[1]').text
            port = driver.find_element(By.XPATH, f'//*[@id="list"]/div/div[2]/div/table/tbody/tr[{i}]/td[2]').text
            https = driver.find_element(By.XPATH, f'//*[@id="list"]/div/div[2]/div/table/tbody/tr[{i}]/td[7]').text
            if https.lower() == 'yes':
                proxy_ip_list.append(ip)
                port_list.append(port)
        except: pass
    driver.quit()
    return [f"{ip}:{port}" for ip, port in zip(proxy_ip_list, port_list)]

# ========= CHROME OPTIONS ========= #
def get_chrome_options(proxy=None):
    options = Options()
    if HEADLESS:
        options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
    if proxy:
        options.add_argument(f'--proxy-server=http://{proxy}')
    return options

# ========= MAIN SCRAPING FUNCTION ========= #
def extract_author_page(author_meta):
    try:
        options = get_chrome_options()
        driver_thread = webdriver.Chrome(options=options)
        driver_thread.get(author_meta['profile_link'])
        time.sleep(2)

        while True:
            books = driver_thread.find_elements(By.XPATH, "//div[@class='books wrapper item']")

            for b in books:
                try:
                    title = b.find_element(By.XPATH, ".//h4[@class='book-title']").text
                    link = b.find_element(By.XPATH, ".//a").get_attribute('href')
                    cur_price = b.find_element(By.XPATH, ".//span[@class='sell-price']").text
                    try:
                        price = b.find_element(By.XPATH, ".//del[@class='original-price mr-2']").text
                    except:
                        price = cur_price

                    with df_lock:
                        df.loc[len(df)] = [
                            author_meta['author_name'], author_meta['profile_link'],
                            author_meta['followers'], author_meta['image_src'],
                            title, price, cur_price, link
                        ]
                except NoSuchElementException:
                    continue

            try:
                nxt = driver_thread.find_element(By.XPATH, "//ul[@class='pagination']/li/a[contains(text(),'Next')]")
                if 'disabled' in nxt.get_attribute('class'):
                    break
                driver_thread.get(nxt.get_attribute('href'))
                time.sleep(1)
            except NoSuchElementException:
                break

        driver_thread.quit()
    except WebDriverException as e:
        print(f"❌ Proxy Failed: {author_meta['profile_link']} - {e}")

# ========= MAIN FUNCTION ========= #
def main():
    proxies = collect_proxies()
    random.shuffle(proxies)
    proxy = proxies[0] if proxies else None
    driver = webdriver.Chrome(options=get_chrome_options(proxy))
    driver.get(BASE_URL)
    time.sleep(3)

    scroll_height = driver.execute_script("return document.body.scrollHeight")
    last_height = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    authors = driver.find_elements(By.XPATH, "//div[@class='author-info-single']")
    author_list = []

    for a in authors:
        try:
            author_name = a.find_element(By.XPATH, ".//h4[@class='author-name']/a").text
            profile_link = a.find_element(By.XPATH, ".//h4[@class='author-name']/a").get_attribute('href')
            followers = a.find_element(By.XPATH, ".//p[@class='followers']/span").text
            img = a.find_element(By.XPATH, ".//img").get_attribute('src')

            author_list.append({
                'author_name': author_name,
                'profile_link': profile_link,
                'followers': followers,
                'image_src': img
            })
        except: continue

    driver.quit()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(extract_author_page, author_list)

    df.to_excel(OUTPUT_EXCEL, index=False)
    print("✅ Done scraping all authors' books!")
