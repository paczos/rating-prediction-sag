from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn import svm
from sklearn import tree
from consts import SCALE_RESOLUTION
from sklearn.metrics import accuracy_score
import sys

filepaths = ['scale_data/scaledata/Dennis+Schwartz/subj.Dennis+Schwartz']#, 'scale_data/scaledata/Scott+Renshaw/subj.Scott+Renshaw', 'scale_data/scaledata/James+Berardinelli/subj.James+Berardinelli']#, 'scale_data/scaledata/Steve+Rhodes/subj.Steve+Rhodes']
filepaths_ratings = ['scale_data/scaledata/Dennis+Schwartz/label.4class.Dennis+Schwartz']#, 'scale_data/scaledata/Scott+Renshaw/label.4class.Scott+Renshaw', 'scale_data/scaledata/James+Berardinelli/label.4class.James+Berardinelli']#, 'scale_data/scaledata/Steve+Rhodes/label.4class.Steve+Rhodes']
#df = pd.read_csv('scale_data/scaledata/Scott+Renshaw/subj.Scott+Renshaw', names=['text'], sep='\t')
#print(df)

# concatenate all reviews
df_list = []
for filepath in filepaths:
    df = pd.read_csv(filepath, names=['text'], sep='\t')
    df_list.append(df)

df_list_class = []
for filepath in filepaths_ratings:
    df_class = pd.read_csv(filepath, names=['class'], sep='\t')
    df_list_class.append(df_class)

df_class = pd.concat(df_list_class, ignore_index=True)
df = pd.concat(df_list, ignore_index=True)
df['class'] = df_class['class']
#print(df)

#delete stop words and signs, tokenization and stemming
stop_words = set(stopwords.words('english'))
tokenizer = RegexpTokenizer(r'\w+')
ps = PorterStemmer()
for index, row in df.iterrows():
    wordsFiltered = ""
    words = tokenizer.tokenize(df.loc[index, 'text'])
    for w in words:
        if w not in stop_words:
            wordsFiltered = wordsFiltered + " " + ps.stem(w)
    df.loc[index, 'text'] = wordsFiltered

#creating bag of words
reviews = df['text']
vectorizer = CountVectorizer(max_features=1000)
X = vectorizer.fit_transform(reviews).toarray()

for i in range(SCALE_RESOLUTION):
    df['class{}'.format(i)] = 0

#add classes for four classifiers
for index, row in df.iterrows():
    df.loc[index, 'class{}'.format(df.loc[index, 'class'])] = 1

X_train = []
X_test = []
y = []
y_train = []
y_test = []
#training and test sets
for i in range(SCALE_RESOLUTION):
    y.append(df['class{}'.format(i)])
    X_train_pom, X_test_pom, y_train_pom, y_test_pom = train_test_split(X, y[i])
    X_train.append(X_train_pom)
    X_test.append(X_test_pom)
    y_train.append(y_train_pom)
    y_test.append(y_test_pom)

# y0 = df['class0']
# y1 = df['class1']
# y2 = df['class2']
# y3 = df['class3']

#training and test sets
# X_train0, X_test0, y_train0, y_test0 = train_test_split(X, y0)
# X_train1, X_test1, y_train1, y_test1 = train_test_split(X, y1)
# X_train2, X_test2, y_train2, y_test2 = train_test_split(X, y2)
# X_train3, X_test3, y_train3, y_test3 = train_test_split(X, y3)


classifier = []
y_pred = []
accuracy = []
#building classifiers and testing 
for i in range(SCALE_RESOLUTION):
    if len(sys.argv) < 2:
        print("Write name of classifier!")
        exit()
    elif sys.argv[1] == "bayes":
        classifier.append(BernoulliNB())
    elif sys.argv[1] == "svm":
        classifier.append(svm.SVC(gamma='scale'))
    elif sys.argv[1] == "tree":
        classifier.append(tree.DecisionTreeClassifier())
    else : 
        print("Name of classifier is incorrect!")
        exit()
    classifier[i].fit(X_train[i], y_train[i])
    y_pred.append(classifier[i].predict(X_test[i]))
    accuracy.append(accuracy_score(y_test[i], y_pred[i]))
    print(accuracy[i])

# classifier = BernoulliNB()
# classifier.fit(X_train3, y_train3)

# # Predict Class
# y_pred = classifier.predict(X_test3)

# # Accuracy 
# from sklearn.metrics import accuracy_score
# accuracy = accuracy_score(y_test3, y_pred)
# print(accuracy)

#print(vectorizer.get_feature_names())
#print(X)


#stemming
# ps = PorterStemmer()
 
# wordsStemmed = []

# for word in wordsFiltered:
#     wordsStemmed.append(ps.stem(word))

# print(wordsStemmed)


 #words = tokenizer.tokenize(reviews)
#print(df.loc[0,'text'])
 
# for w in words:
#     if w not in stop_words:
#         wordsFiltered.append(w)
 
# print(wordsFiltered)

# #stemming
# ps = PorterStemmer()
 
# wordsStemmed = []

# for word in wordsFiltered:
#     wordsStemmed.append(ps.stem(word))

# print(wordsStemmed)