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

def train_classifiers( name_of_classifier, filepath_csv ):
	#file with  tokenized, stemmed, reviews without stop words, and clas0,1,2,3
	df = pd.read_csv(filepath_csv)
	reviews = df['text']
	vectorizer = CountVectorizer(max_features=1000)
	X = vectorizer.fit_transform(reviews).toarray()
	#print(len(X[0]))
	X_train = []
	X_test = []
	y = []
	y_train = []
	y_test = []
	#training and testing sets
	for i in range(SCALE_RESOLUTION):
		y.append(df['class{}'.format(i)])
		X_train_pom, X_test_pom, y_train_pom, y_test_pom = train_test_split(X, y[i])
		X_train.append(X_train_pom)
		X_test.append(X_test_pom)
		y_train.append(y_train_pom)
		y_test.append(y_test_pom)

	classifier = []
	#building classifiers and testing 
	for i in range(SCALE_RESOLUTION):
		if name_of_classifier == "bayes":
			classifier.append(BernoulliNB())
		elif name_of_classifier == "svm":
			classifier.append(svm.SVC(gamma='scale'))
		elif name_of_classifier == "tree":
			classifier.append(tree.DecisionTreeClassifier())
		else : 
			print("Name of classifier is incorrect!")
			exit()
		classifier[i].fit(X_train[i], y_train[i])

	return classifier, vectorizer

def prepare_review_text( review, vectorizer ):
	stop_words = set(stopwords.words('english'))
	tokenizer = RegexpTokenizer(r'\w+')
	ps = PorterStemmer()
	wordsFiltered = ""
	words = tokenizer.tokenize(review)
	for w in words:
		if w not in stop_words:
			wordsFiltered = wordsFiltered + " " + ps.stem(w)
	list_pom = [wordsFiltered]
	X = vectorizer.transform(list_pom).toarray()
	return X