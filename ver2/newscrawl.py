# Important! : Crawling news from websites
from newsapi import NewsApiClient
#basic libraries
import pandas as pd
import numpy as np
import json 
#importing datetime libarary
import datetime
from datetime import date, timedelta
import os


#extracted from GTD database
hot_keywords = ['incidents','explosives','assailants', 'attack',
'bomber', 'bomb', 'dynamite', 'extremists', 'perpatrator']

source_list = ['abc-news', "abc-news-au", "al-jazeera-english", "ansa",
"associated-press", "australian-financial-review", "axios", "bbc-news",
"bloomberg", "breitbart-news", "buzzfeed", "cbs-news", "cnn", "fox-news",
"google-news", "msnbc", "nbc-news", "newsweek", "reuters", "the-hill",
"the-wall-street-journal", "the-washington-times", "time", "usa-today",
"vice-news"]

# Init
newsapi = NewsApiClient(api_key='fed75f65663e4cb7a02f2ae336bacd5e')

#searching datas within 30 days
end_date = date.today().strftime("%Y-%m-%d")
start_date = date.today() - datetime.timedelta(days=30)
start_date = start_date.strftime("%Y-%m-%d")

desired_dir = "./json_files"

def write_json(new_data, filename="Report.JSON"):
   full_path = os.path.join(desired_dir, filename)
   with open(full_path, 'w') as f:
       json_string=json.dumps(new_data)
       f.write(json_string)

# /v2/everything
for keyword in hot_keywords:
    for source in source_list:
        all_articles = newsapi.get_everything(q=keyword,
                                              sources= source,
                                              from_param = start_date,
                                              to=end_date,
                                              #domains='bbc.co.uk,techcrunch.com',
                                              #language='en',
                                              #page=10,
                                              sort_by='relevancy')
                                              
        print(all_articles)
        print(len(all_articles['articles']))
        name = keyword + " " + source + '.json'
        write_json(all_articles, name)

print("Crawling finished")