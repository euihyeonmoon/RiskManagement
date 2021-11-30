from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

url_list = []
title_list = []
summary_list = []
date_list = []
# source_list = []


url = 'https://www.google.com/search?q=terror&tbm=nws&tbs=qdr:m'
# keyword_list = ['terror']
# for keyword in keyword_list:
#     # set the url
#     url = 'https://www.google.com/search?q=' + keyword + '&tbm=nws&tbs=qdr:m'
#     url_list.append(url)
#     print(url_list)


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
    time.sleep(10)
    return title_list, summary_list, date_list

# crawl until the last page
for i in range(1,4):
#    google_crawl()
    title_list = google_crawl()[0]
    summary_list = google_crawl()[1]
    date_list = google_crawl()[2]
#title_list = google_crawl()[0]
#summary_list = google_crawl()[1]
#date_list = google_crawl()[2]

driver.close()

data = pd.DataFrame({'title':title_list, 'summary':summary_list, 'date':date_list})
print(data)
data.to_excel('google.xlsx', index=False)
