from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

url_list = []
title_list = []
summary_list = []
date_list = []
# source_list = []


url = 'https://edition.cnn.com/search?size=30&q=terror&sort=newest'
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
def cnn_crawl():
    time.sleep(2)
    # get the title
    title = driver.find_elements_by_css_selector(".cnn-search__result-headline")
    for _ in title:
        title_list.append(_.text)
    # get the summary
    summary = driver.find_elements_by_css_selector('.cnn-search__result-body')
    for _ in summary:
        summary_list.append(_.text)
    # get the date
    date = driver.find_elements_by_css_selector('.cnn-search__result-publish-date')
    for _ in date:
        date_list.append(_.text)
        
    print('Crawling...')

    # click the next page
    next_button = driver.find_elements_by_css_selector('.pagination-arrow.pagination-arrow-right.cnnSearchPageLink.text-active')
    next_button = next_button[-1]
    next_button.click()
    time.sleep(10)
    return title_list, summary_list, date_list

# crawl until the last page
for i in range(1,2):
#    cnn_crawl()
    title_list = cnn_crawl()[0]
    summary_list = cnn_crawl()[1]
    date_list = cnn_crawl()[2]

driver.close()

data = pd.DataFrame({'Title':title_list, 'Summary':summary_list, 'Date':date_list})
print(data)
data.to_excel('cnn.xlsx', index=False)

print("Crawling is Done")
