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

