import pandas as pd
from sklearn import svm
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB

from consts import SCALE_RESOLUTION

df = pd.read_csv('data.csv')

reviews = df['text']
vectorizer = CountVectorizer(max_features=1000, ngram_range=(2, 2))  # ngram_range=(2,2)
X = vectorizer.fit_transform(reviews).toarray()

x_train = []
x_test = []
y = []
y_train = []
y_test = []

# training and testing sets bag of words
for i in range(SCALE_RESOLUTION):
    y.append(df['class{}'.format(i)])
    X_train_pom, X_test_pom, y_train_pom, y_test_pom = train_test_split(X, y[i])
    x_train.append(X_train_pom)
    x_test.append(X_test_pom)
    y_train.append(y_train_pom)
    y_test.append(y_test_pom)

classifier_type = ['bayes', 'svm', 'tree']

for j in range(len(classifier_type)):
    classifier = []
    y_pred = []
    accuracy = []
    fallout = []
    recall = []
    precision = []
    for i in range(SCALE_RESOLUTION):
        if classifier_type[j] == 'bayes':
            classifier.append(BernoulliNB())
        elif classifier_type[j] == 'svm':
            classifier.append(svm.SVC(gamma='scale'))
        elif classifier_type[j] == 'tree':
            classifier.append(tree.DecisionTreeClassifier())
        classifier[i].fit(x_train[i], y_train[i])
        y_pred.append(classifier[i].predict(x_test[i]))
        accuracy.append(accuracy_score(y_test[i], y_pred[i]))
        tn, fp, fn, tp = confusion_matrix(y_test[i], y_pred[i]).ravel()
        recall = tp / (tp + fn)
        fallout = fp / (fp + tn)
        precision = tp / (tp + fp)
        print('Recall classifier ' + classifier_type[j] + ' ' + str(i) + ' :' + str(recall))
        print('Accuracy classifier ' + classifier_type[j] + ' ' + str(i) + ' :' + str(accuracy[i]))
        print('Precision classifier ' + classifier_type[j] + ' ' + str(i) + ' :' + str(precision))
        print('Fallout classifier ' + classifier_type[j] + ' ' + str(i) + ' :' + str(fallout))
