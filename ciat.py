import warnings
warnings.filterwarnings("ignore")

from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
import time


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--window-size=800x800')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('log-level=3')
# options.add_argument('--proxy-server=45.76.226.206:3128')

driver = webdriver.Chrome('C:\\Users\\bhask\\Downloads\\chromedriver', chrome_options=options)

url = 'https://ciat.org.uk/find-a-practice.html?q=&search_by=location'
driver.get(url)


element = driver.find_element_by_class_name("load-more")
actions = ActionChains(driver)
actions.move_to_element(element).perform()
element.click()
time.sleep(5)

items = driver.find_elements_by_css_selector('.row.member-item')
data_objs = []
for item in items:
    data_obj = {}
    header = item.find_element_by_class_name('location-title').text
    data_obj['company'] = header.split('/')[0]
    data_obj['person'] = header.split('/')[-1].replace('MCIAT', '').strip()

    location_detail = item.find_element_by_css_selector('.col-xs-12.col-sm-6.location-details').text.split('\n')
    for i in range(int(len(location_detail)/2)):
        data_obj[location_detail[i*2]] = location_detail[(i*2)+1]

    data_objs.append(data_obj)

df = pd.DataFrame(data_objs)
df.to_csv('ciat.csv', index=False)
