from selenium import webdriver 
import time 
import requests#this is a library 
driver=webdriver.Chrome() 
driver.get('https://www.daraz.com.bd/')
link=driver.find_element(By.XPATH,' sth Xpath  ').get_attribute('href')
img=driver.find_element(By.XPATH,'  sth Xpath  ').get_attribute('src')
responce=requests.get(img)
with open('imiges/download_image.jpg', 'wb') as f:#imiges folder  এsave  করা
  f.write(responce.content)
  # আরেকটা পদ্ধতি হচ্ছে import urllib.request then লিখব urllib.request.urlretrieve(img,'download_image.jpg')

  time.sleep(20)

#এতক্ষণ কোন একটা পেজের  কোন নির্দিষ্ট  element এর inspect করে then just ওই element এর text আর attributeযেমন:href,src এর এর attribite কে call করে just ওই element এর under এ scrap করে আনতাম এখন ওই catagory এর পেজের সব কিছু কে scrap করব 
tittle_list=[ ]
for page in range(1,3):
  driver.get(f'https://www.daraz.com.bd/page={page}')
  for i in range(1,41):
    j=str(i)
    tittle=driver.find_element(By.XPATH,'----div[+j+]---')
    tittle_list.append(tittle)
print(tittle_list)
ptint(len(tittle_list))
#সেই interesting part টা শুরু করি প্রথমে XPath টা এতটু বলি '//tag[@attribute="value"]'বা একাধিক থাকলে '//tag[@attribute(যেটাvariable value)and contains(@attribute,"value")]' এটাই নিয়ম
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Setup
chromedriver_path = r"C:\Users\hp\PycharmProject\chromedriver.exe"
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)

# particular Category এর urlবসান but page number ছাড়া 
daraz catagory url ta = "https://www.daraz.com.bd/laptops/"  
driver.get(daraz category url ta )
time.sleep(5)  

# Step 2: Pagination থেকে সর্বশেষ page নম্বর বের করো
try:
    # এটা just একটা html এর X path locator যার মধ্যে 2 nd method of Xpath থাকে যেমন এখানে title attribute এর value টা variable ওই variable এর value টা just declare করিনি 
    page_numbers = driver.find_elements(By.XPATH, '//li[@title and contains(@class, "ant-pagination-item")]')
    
    # last এর পেজ নম্বরটা নেই এখানে.text লিখলে just ওই last এর page number টা print হবে কারণ anchor tag এর ভিতরে page number টা লিখা থাকে।
    last_pages = int(page_numbers[-1].text)
    print(f"Total Pages Found: {total_pages}")
except Exception as e: # এটা একটা error catching systemমাসে যদি upper code এ যদি ভুল বা error আসে যেমন pagination নাই  তাহলে except block run হবে এটা একটা backup plan হিসেবে ধরা যায় //
    total_pages = 1  # যদি pagination না থাকে, তাহলে ধরে নিই একটাই পেজ
    print("Pagination or pagenumber not found, assuming that there's one page.")

# Step 3: পেজে পেজে ঘুরে data scrape করি
for page in range(1, total_pages + 1):
    print(f"\n--- Scrapeq করা মোট Page {page} ---")
    driver.get(f"{daraz category url ta}?page={page}")
    time.sleep(3)

    # এখন প্রতিটা পণ্যের title বের করি
    titles = driver.find_elements(By.XPATH, '//div[@class="title--wFj93"]')
    
    for title in titles:
        print(title.text)

driver.quit()
#এখন একটু button এclick করে করে আগানো  যায় কীভাবে সেটার process
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException

chromedriver_path = r"C:\Users\hp\PycharmProject\chromedriver.exe"
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)

driver.get("https://www.daraz.com.bd/category-name/")
time.sleep(3)

while True:#চালিয়ে যাও যতক্ষণ পর্যন্ত না থামাই বা argument সত্য না হয় 
    # এখানে আপনি প্রতিটা পেজ থেকে data extract করতে পারেন
    print("Scraping this page...")

    try:
        # next page button খুজে বের করে তাহলে খুজে বের করে আর যদি না পায় তাহলে error না দিয়ে break দিয়ে শান্তভাবে break দিয়ে সোটি বন্ধ করে একে বলে error handling with try-expect 
        next_button = driver.find_element(By.XPATH, '//li[@title="Next Page"]/a')
        next_button.click()
        time.sleep(3)
    except NoSuchElementException: # এটা selenium এর  builtin exception error type মানে যে element টি খুজছিলাম সেটি যদি না পাওয়া যায় তাহলে error না দিয়ে শান্তভাবে break দিয়ে loop বন্ধ করে 
        print("No more pages.")
        break
  #scroll height টা একচু দেখি 
driver. get (যে page এ scrollheight load হয় সেখানের url নিব html পর্যন্ত)
height=driver. execute_script('return document.body.scrollHeight)
print(height)
for i in range(0,height+1200,30)
   driver.execute_script(f"window.scrollTo(0,{i})")
   time.sleep(10)
comment =driver. dind_elements(By.Class_name, 'content')
comment_list=[ ]
for i in comment 
  comment_list.appand(i)
print(comment_list)
# উপরের same code টাই আবার দেখি
# scroll loop শুরু
for i in range(0, height + 1200, 30):
    driver.execute_script(f"window.scrollTo(0, {i})")
    time.sleep(1)  # ⬅️ এগুলো scroll loop-এর ভিতরে

# scroll শেষ → নতুন ব্লক: comment নেওয়া শুরু
comments = driver.find_elements(By.CLASS_NAME, 'content')
comment_list = []

# comment list-এ যোগ করার loop
for c in comments:
    comment_list.append(c.text)  # ⬅️ এটা এই loop-এর ভিতরে

# সব comment print করা (সবচেয়ে বাইরের লেভেলে)
print(comment_list)
# send keys দিয়ে কাজ করা 
from selenium.webdriver.common.keys import Keys
driver.get(www.google.com) 
google_input=driver.find_elements(By.NAME,'q') 
google_input.send_keys("laptop shop near mirpur")
google_input.send_keys("Keys.RETURN)
# recapcha handle করা -- recapcha checkbox এ যেকোন জায়গায় ক্লিক করলেই checkbox এ rightclickহয়ে যায় এই পুরোটা checkbox সহ পুরো box টা একটা particular class_name =g_recapcha এর under এ থাকে  তখন সেটাকে খজে পেতে হলে inspect করে search করতে হয় এখন এটা কিন্তু একটক div উপর ক্লিক করছি কারণ input tag link tag ackchor tag এর ভিতরে ওই recaptcha checkbox নাই তাই actionvhaims use করতে হবে 

from selenium.webdriver. chrome. options import Options
chrome_options=Options() 
chrome_options.add-argumment("--disable-blink-features=AutomationControlled")
chrome_options.add-arguments("user-agent=Mozilla/5.0(Windows NT 10.0; win64;x64)")
driver=webdriver.Chrome(options=chrome_options)
driver.get(https://www.google.com)
#এখন এটা দেই আর উপরের send_keys দিয়ে কাজ ও তারপরে করি 
recaptcha_checkbox=driver.find_element(By.CLASS_NAME, 'g_recaptcha) 
from selenium.webdriver. common. action_chains import ActionChains
action=ActionChains(driver)
action.move_to_element(recaptcha_checkbox).click(). perform()

driver.maximize_window() 
# headless mode এ data collect করতে াি করা লাগে 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Chrome options
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")

# Start browser
driver = webdriver.Chrome(options=options)

# Open a page
driver.get("https://www.google.com")

# Take screenshot
driver.save_screenshot("google_homepage.png")  #  এটা PNG ফাইল বানিয়ে দিবে আমার excepted folder এ 

# Close browser
driver.quit()
#গুরুত্বপূর্ণ কিছু features 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Step 1: Chrome Options তৈরি করুন
chrome_options = Options()

# Step 2: আপনি যা যোগ করতে চান:
chrome_options.add_argument("--disable-cache")   # ক্যাশ বন্ধ রাখে
chrome_options.add_argument("--incognito")       # ইনকগনিটো মোডে চালায়
chrome_options.add_argument("--headless")        # 👉 Headless মোড চালু করার জন্য এটা যোগ করুন
chrome_options.add_argument("--window-size=1920,1080")  # Headless হলে স্ক্রিন সাইজ দিতে হয়

# Step 3: WebDriver তৈরি করুন
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.google.com")
print(driver.title)# লেখা উঠবে google কারণ html এ লেখা আছে <tittle>goolgle</tittle>

driver.quit()
#excepted conditions হলো এমন একটি selenium এর টুলবক্স যেখানে বলে দেয় কোন একটা জিনিস লোড হওয়া পর্যন্ত অপেক্ষা করুন। 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# অপেক্ষা করো যতক্ষণ না 'submit' বাটনটা উপস্থিত হয়
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "submit"))
) #এখানে EC.presence_of_element_located() হলো একটি expected condition.এটা Selenium কে বলে:> "ভাই, ১০ সেকেন্ড পর্যন্ত চেক করে দেখো ওই ID ওয়ালা বাটনটা আসছে কিনা, তারপর proceed করো।"
#daraz এর ওই list এর 42 নম্বর পন্যটা স্ক্রল করে এনে দেন 
product = driver.find_element(By.XPATH, "//div[@class='product'][42]") #এই 42 টা নিজে দিতে হবে 

driver.execute_script("arguments[0].scrollIntoView();", product)
print("Product visible now!") #এখন চাচ্ছি যে loop চালাব তাই পরের কোডটা হলো 
products = driver.find_elements(By.XPATH, "//div[@class='product']")

for product in products:
    driver.execute_script("arguments[0].scrollIntoView();", product)
    print(product.text)
#এরকমই একটা কোড interesting
for product in products:
    driver.execute_script("arguments[0].scrollIntoView();", product)
    time.sleep(1)
    
    try:
        title = product.find_element(By.CLASS_NAME, "title-class").text
        price = product.find_element(By.CLASS_NAME, "price-class").text
        print(f"{title} → {price}")
    except:
        print("Error reading product")

#এটা just java script এর argument নিবে আর প্রিন্ট করবে 
driver.execute_script(
    "console.log(arguments[0], arguments[1], arguments[2]);",
    "🍎", "🍌", "🍇"
)
#দুইটা different scrolltop এর example নিজে থেকেই বুঝবে 
driver.execute_script(
    "arguments[0].scrollTop = arguments[0].scrollHeight;",
    box
)
#দুইটা javascript এর argument pass করলাম এবং আমি mention করে দিচ্ছি যে কতটুক পর্য্ত করবে 
driver.execute_script(
    "arguments[0].scrollTop = arguments[0].scrollHeight;",
    box
)
#আরেকটু broad ভাবো 
div1 = driver.find_element(By.ID, "box1")
div2 = driver.find_element(By.ID, "box2")

driver.execute_script(
    "arguments[0].scrollTop = arguments[1]; arguments[2].scrollTop = arguments[3];",
    div1, 300,
    div2, 500
)
# আচ্ছা এটা কিন্তু আবতর একটু remind করিয়ে দিচ্ছি এই argument এর কিন্তু power আছে নিজেরই scrollhight difine করার

box = driver.find_element(By.XPATH, '//div[@class="scrollable-div"]')

driver.execute_script(
    "arguments[0].scrollTop = arguments[0].scrollHeight;",
    box
)
# এবার click নিয়ে কাজ করব 
product = driver.find_element(By.XPATH, "//div[@class='product'][42]")

# স্ক্রল করে আনবে
driver.execute_script("arguments[0].scrollIntoView();", product)
time.sleep(1)

# Click করতে চাইলে
product.click()

# অথবা Title ও Price নিতে চাইলে:
title = product.find_element(By.CLASS_NAME, "title").text
price = product.find_element(By.CLASS_NAME, "price").text

print("Title:", title)
print("Price:", price)

# treadpool এর use 
from concurrent.futures import treadPoolExecutor 
import treading
link_list=[কমা দিয়ে দিয়ে লেখব url গুলো]
define scrape_func(link):
  driver=webdriver.Chrome() 
  driver.get(link)
  print(f" {treading.current_tread().name} scraped")
with TreadPoolExecutor(max_workers=2) as executor
   execute=[executor.submit{scrape_func,link} for link in link_list]

