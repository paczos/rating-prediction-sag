import sys

import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from sklearn import svm
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB

from consts import SCALE_RESOLUTION

file_paths = [
    'scale_data/scaledata/Dennis+Schwartz/subj.Dennis+Schwartz']
# , 'scale_data/scaledata/Scott+Renshaw/subj.Scott+Renshaw',
# 'scale_data/scaledata/James+Berardinelli/subj.James+Berardinelli']
# , 'scale_data/scaledata/Steve+Rhodes/subj.Steve+Rhodes']
file_paths_ratings = [
    'scale_data/scaledata/Dennis+Schwartz/label.4class.Dennis+Schwartz']
# , 'scale_data/scaledata/Scott+Renshaw/label.4class.Scott+Renshaw',
# 'scale_data/scaledata/James+Berardinelli/label.4class.James+Berardinelli']
# #, 'scale_data/scaledata/Steve+Rhodes/label.4class.Steve+Rhodes']
# df = pd.read_csv('scale_data/scaledata/Scott+Renshaw/subj.Scott+Renshaw', names=['text'], sep='\t')
# print(df)

# concatenate all reviews


df_list = []
for filepath in file_paths:
    df = pd.read_csv(filepath, names=['text'], sep='\t')
    df_list.append(df)

df_list_class = []
for filepath in file_paths_ratings:
    df_class = pd.read_csv(filepath, names=['class'], sep='\t')
    df_list_class.append(df_class)

df_class = pd.concat(df_list_class, ignore_index=True)
df = pd.concat(df_list, ignore_index=True)
df['class'] = df_class['class']
# print(df)

# delete stop words and signs, tokenization and stemming
stop_words = set(stopwords.words('english'))
tokenizer = RegexpTokenizer(r'\w+')
ps = PorterStemmer()
for index, row in df.iterrows():
    wordsFiltered = ""
    words = tokenizer.tokenize(df.loc[index, 'text'])
    for w in words:
        if w not in stop_words:
            wordsFiltered = wordsFiltered + ' ' + ps.stem(w)
    df.loc[index, 'text'] = wordsFiltered

# creating bag of words
reviews = df['text']
vectorizer = CountVectorizer(max_features=1000, ngram_range=(2,2))
X = vectorizer.fit_transform(reviews).toarray()
# df['text'] = X.tolist()
print(vectorizer.get_feature_names())

for i in range(SCALE_RESOLUTION):
    df['class{}'.format(i)] = 0

# add classes for four classifiers
for index, row in df.iterrows():
    df.loc[index, 'class{}'.format(df.loc[index, 'class'])] = 1

# df.to_csv('data.csv')

x_train = []
x_test = []
y = []
y_train = []
y_test = []
# training and testing sets
for i in range(SCALE_RESOLUTION):
    y.append(df['class{}'.format(i)])
    X_train_pom, X_test_pom, y_train_pom, y_test_pom = train_test_split(X, y[i])
    x_train.append(X_train_pom)
    x_test.append(X_test_pom)
    y_train.append(y_train_pom)
    y_test.append(y_test_pom)

classifier = []
y_pred = []
accuracy = []

# building classifiers and testing
for i in range(SCALE_RESOLUTION):
    if len(sys.argv) < 2:
        print('Write name of classifier!')
        exit()
    elif sys.argv[1] == 'bayes':
        classifier.append(BernoulliNB())
    elif sys.argv[1] == 'svm':
        classifier.append(svm.SVC(gamma='scale'))
    elif sys.argv[1] == 'tree':
        classifier.append(tree.DecisionTreeClassifier())
    else:
        print('Name of classifier is incorrect!')
        exit()
    classifier[i].fit(x_train[i], y_train[i])
    y_pred.append(classifier[i].predict(x_test[i]))
    accuracy.append(accuracy_score(y_test[i], y_pred[i]))
    print(accuracy[i])
