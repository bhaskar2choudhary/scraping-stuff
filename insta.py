import warnings
warnings.filterwarnings("ignore")

from selenium import webdriver
import pandas as pd
import time
import re
from selenium.webdriver.common.keys import Keys
from random import shuffle
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--window-size=800x800')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('log-level=3')
# options.add_argument('--proxy-server=45.76.226.206:3128')

driver = webdriver.Chrome('C:\\Users\\bhask\\Downloads\\chromedriver', chrome_options=options)

url = 'https://www.instagram.com/'
driver.get(url)

WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, "input")))
inputs = driver.find_elements_by_tag_name('input')
for input in inputs:
    if input.get_attribute('name') == 'username':
        input.send_keys('flibo.ai')
    if input.get_attribute('name') == 'password':
        input.send_keys('password')
print(driver.title)
input.send_keys(Keys.ENTER)
time.sleep(5)

url = 'https://www.instagram.com/flibo.ai/'
driver.get(url)

counter = 0
while counter < 5: # fixed number of iterations as I was scraping my own page to analyse hastags used, so I knew that 5 would be enough
    body = driver.find_element_by_css_selector('body')
    body.send_keys(Keys.END)
    time.sleep(5)
    counter += 1


body.send_keys(Keys.HOME)
time.sleep(2)

print('Starting now...')
data_objs = []
while driver.execute_script('return window.scrollY /(document.documentElement.scrollHeight - document.documentElement.clientHeight)') != 1:
    items = driver.find_elements_by_css_selector('.v1Nh3.kIKUG._bz0w')
    for item in items:
        data_obj = {}
        data_obj['post_url'] = item.find_element_by_tag_name('a').get_attribute('href')
        data_obj['thumbnail'] = item.find_element_by_tag_name('img').get_attribute('srcset')
        data_obj['description'] = item.find_element_by_tag_name('img').get_attribute('alt')
        if data_obj['description'] == '':
            item.click()
            driver.find_elements_by_css_selector('.wpO6b')[-1].click()
            time.sleep(2)
            data_obj['description'] = item.find_element_by_tag_name('img').get_attribute('alt')

        data_objs.append(data_obj)
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
print('Finished.')

df = pd.DataFrame(data_objs)
df = df[df['description']!='']
df.drop_duplicates('post_url', inplace=True)


def find_handles(string):
    output = re.findall(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9-_]+)', string)
    output = ['@'+x for x in output]
    output = list(set(output))
    shuffle(output)
    return output


df['handles_tagged'] = df['description'].apply(lambda x: find_handles(x) if x else x)


def find_hashtags(string):
    output = re.findall(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))#([A-Za-z]+[A-Za-z0-9-_]+)', string)
    output = ['#'+x for x in output]
    output = list(set(output))
    shuffle(output)
    return output


df['hashtags'] = df['description'].apply(lambda x: find_hashtags(x) if x else x)

df.to_csv('insta.csv', index=False)
