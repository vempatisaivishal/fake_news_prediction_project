import nltk
import joblib
import pickle
from nltk.corpus import stopwords
import pandas as pd
import string as s
class clickbait:
    def __init__(self, title):
        self.result = 0
        self.headline = title
        self.lemmatize = nltk.stem.WordNetLemmatizer()

    def tokenization(self, text):
        lst = text.split()
        return lst

    def lowercasing(self, lst):
        new_lst = []
        for i in lst:
            new_lst.append(i.lower())
        return new_lst

    def remove_stopwords(self, lst):
        stop = stopwords.words('english')
        new_lst = []
        for i in lst:
            if i not in stop:
                new_lst.append(i)
        return new_lst

    def remove_punctuations(self, lst):
        new_lst = []
        for i in lst:
            for j in s.punctuation:
                i = i.replace(j, '')
            new_lst.append(i)
        return new_lst

    def remove_numbers(self, lst):
        nodig_lst = []
        new_lst = []
        for i in lst:
            for j in s.digits:
                i = i.replace(j, '')
            nodig_lst.append(i)
        for i in nodig_lst:
            if i != '':
                new_lst.append(i)
        return new_lst

    def remove_spaces(self, lst):
        new_lst = []
        for i in lst:
            i = i.strip()
            new_lst.append(i)
        return new_lst

    def lemmatzation(self, lst):
        new_lst = []
        for i in lst:
            i = self.lemmatize.lemmatize(i)
            new_lst.append(i)
        return new_lst

    def vectorrize(self, lst):
        dg = ''
        for i in lst:
            dg += i
            dg += ' '
        with open('vectorize.pkl', 'rb') as fin:
            tfidf = pickle.load(fin)
            return tfidf.transform(pd.Series({1: dg}))

    def predict(self, lst):
        with open('clickbaitmodel (1).pkl', 'rb') as ld:
            model = joblib.load(ld)
            return model.predict(lst)

    def run(self):
        self.headline = self.tokenization(self.headline)
        self.headline = self.lowercasing(self.headline)
        self.headline = self.remove_stopwords(self.headline)
        self.headline = self.remove_spaces(self.headline)
        self.headline = self.remove_numbers(self.headline)
        self.headline = self.remove_punctuations(self.headline)
        self.headline = self.lemmatzation(self.headline)
        self.headline = self.vectorrize(self.headline)
        self.result = self.predict(self.headline)
        return self.result