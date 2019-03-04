# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 11:20:55 2019

@author: satish.kumar
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 10:29:04 2019

Sentiment analysis of all drug review

@author: satish.kumar
"""

import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re


df = pd.read_excel('drugsReview_All.xlsx')
df.head()

df.drop(['Unnamed: 0', 'drugName','condition', 'date', 'usefulCount'], axis=1,inplace=True)

ps = PorterStemmer()
def text_cleaner( review_text ):
    
    raw_words = review_text.split()
    stops = set(stopwords.words("english")) 
    meaningful_words = [ps.stem(w.lower()) for w in raw_words if not w in stops]
    
    """ Using Stemmer to get root words """
    
    return " ".join( meaningful_words )

df['review'] = df['review'].apply((lambda x: str(re.sub('[^a-zA-Z\s]','',x)).strip()))
df['review'] = df['review'].apply(lambda x : text_cleaner(str(x)))

#text representation
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
features = tfidf.fit_transform(df.review).toarray()
labels = df.rating
features.shape

#diving into test data and traingin data

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
X_train, X_test, y_train, y_test = train_test_split(df['review'], df['rating'], random_state = 0)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf = MultinomialNB().fit(X_train_tfidf, y_train)

#accuracy
print("accuracy", clf.score(X_train_tfidf, y_train))

# current rating mean
#print("mean ",df["rating"].mean())
#ratingList = df['rating'].tolist()

#make pridiction

userReview = "weight loss great hair loss worth"
print(clf.predict(count_vect.transform([userReview])))
#ratingList.append(clf.predict(count_vect.transform([userReview])))

# new mean
#print("new mean", np.mean(ratingList))