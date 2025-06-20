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

height=driver. execute_script('return document.body.scrollHeight)
print(height)
for i in range(0,height+834,28):
   driver.execute_script(f"window.scrollTo(0,{i})")
   time.sleep(10)
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
