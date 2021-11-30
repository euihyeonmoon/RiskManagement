from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

#link_list = []
title_list = []
summary_list = []
date_list = []

#extracted from GTD database
hot_keywords = ['incidents','explosives','assailants', 'attack',
'bomber', 'bomb', 'dynamite', 'extremists', 'perpatrator']

url_list = []
for key in hot_keywords:
    url = 'https://www.google.com/search?q=india' + " " + key +'&tbm=nws&tbs=qdr:m'
    url_list.append(url)


def chroming(url):
    global options
    global driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    driver.get(url)

# crawl the data from google using selenium with Chrome
def google_crawl():
    time.sleep(2)
    # get the title
    title = driver.find_elements_by_css_selector(".mCBkyc.tNxQIb.ynAwRc.JIFdL.JQe2Ld.nDgy9d")
    for _ in title:
        title_list.append(_.text)
    # get the summary
    summary = driver.find_elements_by_css_selector('.GI74Re.nDgy9d')
    for _ in summary:
        summary_list.append(_.text)
    # get the date
    date = driver.find_elements_by_css_selector('.S1FAPd.OSrXXb.ecEXdc')
    for _ in date:
        date_list.append(_.text)
        
    print('Crawling...')

    # click the next page
    next_button = driver.find_elements_by_css_selector('.SJajHc.NVbCr')
    next_button = next_button[-1]
    next_button.click()
    time.sleep(5)
    return title_list, summary_list, date_list

def Chroming_end():
    driver.close()

for url in url_list:
    chroming(url)
    for _ in range(1, 10):
        title_list, summary_list, date_list = google_crawl()
    Chroming_end()

data = pd.DataFrame({'Title':title_list, 'Summary':summary_list, 'Date':date_list})
print(data)
data.to_excel('googling.xlsx', index=False)

print("Crawling is Done")