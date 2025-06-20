from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.facebook.com/photo/?fbid=719266390857644&set=a.106510685466554")
time.sleep(5)

scrollbox = driver.find_element(By.XPATH, '//*[@id="mount_0_0_i5"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[2]')
for _ in range(15):
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollbox)
    time.sleep(20)
names = driver.find_elements(By.CSS_SELECTOR, 'span[class*="x1lliihq"]')
comments = driver.find_elements(By.CSS_SELECTOR, 'div[dir="auto"][style="text-align: start;"]')
list = []
for name, comment in zip(names, comments):
    try:
        person = name.text.strip()
        text = comment.text.strip()
        if person and text:  # Avoid empty values
            list.append({
                'name': person,
                'comment': text
            })
            print(f"{person} → {text}")
    except Exception as e:
        print(" Error extracting comment:", e)
        continue
print(f"\n Total Comments + Replies Collected: {len(list)}")
ptint(list) 

driver.quit()
