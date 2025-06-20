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


for _ in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

# STEP 5: Extract comment/reply authors & texts
names = driver.find_elements(By.CSS_SELECTOR, 'span[class*="x1lliihq"]')
comments = driver.find_elements(By.CSS_SELECTOR, 'div[dir="auto"][style="text-align: start;"]')

structured = []

for name, comment in zip(names, comments):
    try:
        person = name.text.strip()
        text = comment.text.strip()
        if person and text:  # Avoid empty values
            structured.append({
                'name': person,
                'comment': text
            })
            print(f"🗣️ {person} → {text}")
    except Exception as e:
        print("❌ Error extracting comment:", e)
        continue

# STEP 6: Print summary
print(f"\n✅ Total Comments + Replies Collected: {len(structured)}")

# STEP 7: (Optional) Save to JSON file
with open("facebook_comments.json", "w", encoding='utf-8') as f:
    json.dump(structured, f, ensure_ascii=False, indent=2)

driver.quit()
