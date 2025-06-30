import threading
import time
import pandas as pd
import psutil
import multiprocessing
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROMEDRIVER_PATH = "/path/to/chromedriver"
HEADLESS = True 

# Collect Proxy List
def collect_proxies():
    driver = webdriver.Chrome()
    driver.get('https://free-proxy-list.net/')
    time.sleep(5)
    proxy_ip_list = []
    port_list = []
    for i in range(1, 20):
        try:
            ip_address = driver.find_element(By.XPATH, f'//*[@id="list"]/div/div[2]/div/table/tbody/tr[{i}]/td[1]').text
            port_add = driver.find_element(By.XPATH, f'//*[@id="list"]/div/div[2]/div/table/tbody/tr[{i}]/td[2]').text
            https_support = driver.find_element(By.XPATH, f'//*[@id="list"]/div/div[2]/div/table/tbody/tr[{i}]/td[7]').text
            if https_support == "yes":
                proxy_ip_list.append(ip_address)
                port_list.append(port_add)
        except:
            pass
    driver.quit()
    return [f"{ip}:{port}" for ip, port in zip(proxy_ip_list, port_list)]

PROXY_LIST = collect_proxies()

# Get Browser Options with Proxy
def get_chrome_options(proxy=None):
    options = Options()
    if HEADLESS:
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
    options.add_argument("--disable-cache")
    options.add_argument("--incognito")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    if proxy:
        options.add_argument(f"--proxy-server=http://{proxy}")
    return options

# 📊 Shared DataFrame + Lock
columns = [
    'author_name','author_profile','author_followers','author_image',
    'book_title','book_price','book_old_price','book_reviews','book_link','review_comments'
]
df = pd.DataFrame(columns=columns)
df_lock = threading.Lock()

# ✅ System Resource Analysis for Max Thread Calculation
def estimate_max_workers():
    def measure_driver_memory():
        driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=get_chrome_options())
        time.sleep(1)
        process = psutil.Process(driver.service.process.pid)
        mem = process.memory_info().rss
        for child in process.children(recursive=True):
            mem += child.memory_info().rss
        driver.quit()
        return mem / (1024**2)

    selenium_mem = measure_driver_memory()
    logical_cores = multiprocessing.cpu_count()
    ram_gb = psutil.virtual_memory().total / (1024**3)
    max_by_ram = (ram_gb * 1024) / selenium_mem
    max_by_cpu = logical_cores * 1.5
    return int(min(max_by_ram, max_by_cpu))

# 🔍 Book + Comment Extractor Function
def extract_author_page(author_meta):
    proxy = random.choice(PROXY_LIST)
    print(f" Starting extraction for {author_meta['author_name']} with proxy {proxy}")
    chrome_options = get_chrome_options(proxy)
    try:
        driver_thread = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=chrome_options)
        driver_thread.implicitly_wait(5)
        driver_thread.get(author_meta['profile_link'])
        time.sleep(2)
        while True:
            books = driver_thread.find_elements(By.XPATH, "books এর xpath")
            for b in books:
                try:
                    title = b.find_element(By.XPATH, "book title এর xpath").text
                    link = b.find_element(By.XPATH, "book details button xpath").get_attribute('href')
                    price = b.find_element(By.XPATH, "book old price xpath").text if b.find_elements(By.XPATH, "book old price xpath") else ""
                    cur_price = b.find_element(By.XPATH, "book current price xpath").text
                    reviews = b.find_element(By.XPATH, "book reviews xpath").text

                    driver_thread.execute_script("window.open();")
                    driver_thread.switch_to.window(driver_thread.window_handles[-1])
                    driver_thread.get(link)
                    time.sleep(1)
                    comments = ""
                    try:
                        WebDriverWait(driver_thread, 3).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".media-body .media-heading")))
                        comm_elems = driver_thread.find_elements(By.CSS_SELECTOR, ".media-body .media-heading")
                        comments = "\n".join([c.text for c in comm_elems])
                    except:
                        pass
                    driver_thread.close()
                    driver_thread.switch_to.window(driver_thread.window_handles[0])

                    with df_lock:
                        df.loc[len(df)] = [
                            author_meta['author_name'], author_meta['profile_link'],
                            author_meta['followers'], author_meta['image_src'],
                            title, cur_price, price, reviews, link, comments
                        ]
                except NoSuchElementException:
                    continue

            try:
                nxt = driver_thread.find_element(By.XPATH, "author এর book এর window এর pagination")
                if 'disabled' in nxt.get_attribute('class'):
                    break
                driver_thread.get(nxt.get_attribute('href'))
                time.sleep(1)
            except NoSuchElementException:
                break
    except WebDriverException as e:
        print(f"❌ Proxy Failed: {proxy} - {e}")
    finally:
        try:
            driver_thread.quit()
        except:
            pass

# 🔰 Scrape All Authors + Their Books
def main():
    global df
    chrome_options = get_chrome_options()
    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=chrome_options)
    driver.implicitly_wait(5)
    driver.get("https://www.rokomari.com")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, "লেখক subcategory Xpath"))).click()
    time.sleep(2)

    authors_to_scan = []
    while True:
        items = driver.find_elements(By.XPATH, "author block এর Xpath")
        for a in items:
            try:
                author_meta = {
                    'author_name': a.find_element(By.XPATH, "author name xpath").text,
                    'image_src': a.find_element(By.XPATH, "author image xpath").get_attribute('src'),
                    'followers': a.find_element(By.XPATH, "author follower count xpath").text,
                    'profile_link': a.find_element(By.XPATH, "author profile link xpath").get_attribute('href'),
                }
                authors_to_scan.append(author_meta)
            except NoSuchElementException:
                continue
        try:
            next_page = driver.find_element(By.XPATH, "author pagination xpath")
            if 'disabled' in next_page.get_attribute('class'):
                break
            driver.get(next_page.get_attribute('href'))
            time.sleep(2)
        except NoSuchElementException:
            break
    driver.quit()

    max_workers = min(estimate_max_workers(), 10)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for meta in authors_to_scan:
            executor.submit(extract_author_page, meta)

    df.to_excel("rokomari_authors_books_with_proxies.xlsx", index=False)

if __name__ == "__main__":
    main()
