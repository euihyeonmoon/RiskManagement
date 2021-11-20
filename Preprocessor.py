import numpy as np
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
stop = stopwords.words('english')

data = pd.read_excel('cnn.xlsx')

df = pd.DataFrame(data)
# Time preprocessing : n hours ago -> 1 day ago
# for i in range(len(df['Month'])):
#     if df['Month'][i] == 0:
#         df['Month'][i] += 1

# for i in range(len(df['Day'])):
#     if df['Day'][i] == 0:
#         df['Day'][i] += 1
# df['Time'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
# df.drop(['Year', 'Month', 'Day'], axis = 1 , inplace = True)
# df['Time'] = [x.to_pydatetime().date() for x in df['Time']]

# df= df[['Time', 'Summary', 'Country']]

df.dropna(how='any', axis=0, inplace=True)
df.reset_index(inplace = True)
df.drop(['index'], axis = 1 , inplace = True)

# Natural Language Processing
df['Summary'] = df.apply(lambda row: nltk.word_tokenize(row['Summary']), axis=1)
df['Summary'] = df['Summary'].apply(lambda x: [word for word in x if word not in (stop)])
df['Summary'] = df['Summary'].apply(lambda x: [WordNetLemmatizer().lemmatize(word, pos='v') for word in x])
df['Summary'] = df['Summary'].apply(lambda a : a[2:]) #delete?

tokenized_doc = df['Summary'].apply(lambda x: [word for word in x if len(word) > 3])

detokenized_doc = []
for i in range(len(df)):
    t = ' '.join(tokenized_doc[i])
    detokenized_doc.append(t)

df['Summary'] = detokenized_doc

vectorizer = TfidfVectorizer(stop_words='english', max_features= 1000) # reserving top 1,000 words
X = vectorizer.fit_transform(df['Summary'])

lda_model=LatentDirichletAllocation(n_components=50,learning_method='online',random_state=777,max_iter=1)
lda_top=lda_model.fit_transform(X)

terms = vectorizer.get_feature_names()

def get_topics(components, feature_names, n=1):
    for idx, topic in enumerate(components):
        print("Topic %d:" % (idx+1), [(feature_names[i], topic[i].round(2)) for i in topic.argsort()[:-n - 1:-1]])

get_topics(lda_model.components_,terms)

hot_keywords = []
for topic in lda_model.components_:
    for _ in ([(terms[i]) for i in topic.argsort()[:-1 - 1:-1]]):
        hot_keywords.append(_)

print("the length of the list from the dataframe with 'hot_keywords' is " + str(len(hot_keywords)))

# Filter the texts with hot keywords
for i, sentence in enumerate(df['Summary']):
    if any(x in sentence for x in hot_keywords):
        pass
    else:
        df.drop(df.index[i])
        
# dropping duplicated data
df.drop_duplicates(inplace = True)
df.reset_index(inplace = True)
df.drop(['index'], axis = 1, inplace = True)

df.to_excel('cnn_fixed.xlsx', index=False)

print("Preprocessing is Done")