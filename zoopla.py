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

url = 'https://www.zoopla.co.uk/for-sale/property/aldersbrook/?page_size=100'
print('Starting to fetch...')
driver.get(url)
driver.find_element_by_css_selector('.ui-button-primary.ui-cookie-accept-all-medium-large').click()
driver.find_element_by_class_name('listing-results-utils-tooltip').find_element_by_class_name('btn').click()

items = driver.find_elements_by_class_name('listing-results-wrapper')
print('Staring to scrape.')
data_objs = []
for item in items:
    data_obj = {}
    data_obj['price'] = item.find_element_by_css_selector('.listing-results-price.text-price').text
    print(data_obj['price'])

    data_obj['beds'] = item.find_element_by_css_selector('.num-icon.num-beds').text
    data_obj['baths'] = item.find_element_by_css_selector('.num-icon.num-baths').text
    data_obj['reception'] = item.find_element_by_css_selector('.num-icon.num-reception').text

    data_obj['header'] = item.find_element_by_class_name('listing-results-attr').text.replace('Just added', '')
    data_obj['address'] = item.find_element_by_class_name('listing-results-address').text

    data_obj['description'] = item.find_element_by_tag_name('p').text

    nearby_places = item.find_element_by_css_selector('.nearby_stations_schools.clearfix')
    places = []
    for place in nearby_places.find_elements_by_tag_name('li'):
        places.append(place.text)

    footer = item.find_element_by_css_selector('.listing-results-footer.clearfix')
    left_footer = footer.find_element_by_class_name('listing-results-left')
    data_obj['listed_by'] = left_footer.find_element_by_tag_name('span').text
    data_obj['listed_on'] = left_footer.find_element_by_tag_name('small').text.replace('Listed on ', '').replace(' by', '')

    data_obj['phone'] = item.find_element_by_class_name('agent_phone').text.replace(' **', '')

    data_objs.append(data_obj)

df = pd.DataFrame(data_objs)
df.to_csv('zoopla.csv', index=False)
