from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.google.com")

search = driver.find_element(By.XPATH, '//*[@id="APJFgb"]')
search.send_keys("Laptop Shop near Mirpur")
search.send_keys(Keys.ENTER)

time.sleep(2)

recaptcha_checkbox = driver.find_element(By.CLASS_NAME, 'g_recaptcha')
action = ActionChains(driver)
action.move_to_element(recaptcha_checkbox).click().perform()

driver.maximize_window()

maps_tab = driver.find_element(By.XPATH, '//*[@id="hdtb-sc"]/div/div[1]/div[1]/div/div[2]/a/div')
maps_tab.click()
time.sleep(3)

leads = []
base_xpath = '//*[@id="QAOSzd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{}]/div/a'

for i in range(3, 201, 2):
    try:
        j = str(i)
        shop = driver.find_element(By.XPATH, base_xpath.format(j))
        driver.execute_script("arguments[0].scrollIntoView();", shop)
        time.sleep(10)
        shop.click()
        time.sleep(30)

        name = driver.find_element(By.CLASS_NAME, 'DUwDvf').text

        try:
            phone = driver.find_element(By.CLASS_NAME, 'lo6YTe').text
        except:
            phone = "Not Found"

        leads.append((name, phone))
        print(f"{len(leads)} → {name} : {phone}")

        if len(leads) >= 100:
            break

    except Exception as e:
        print(f"Skipping shop at index {i}: {e}")
        continue

print("\n--- All Leads Collected ---\n")
for idx, (n, p) in enumerate(leads, start=1):
    print(f"{idx}. {n} → {p}")
