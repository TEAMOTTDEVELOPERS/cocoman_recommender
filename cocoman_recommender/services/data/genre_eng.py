import re
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from cocoman_recommender.config.config import BASE_DIR

import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')


class GenreEngData:
    def __init__(self):
        self.data = None
        self.load_data()

    def load_data(self):
        lemm = WordNetLemmatizer()

        raw_data = pd.read_csv(BASE_DIR + '/datasets/justwatch_eng.csv')

        description = raw_data['story'].copy()
        stop_words = set(stopwords.words('english'))

        for i, d in enumerate(description):
            d = re.sub('[-=+,#/?:^$.@*\"~&%!()\[\]<>`\']', '', d)
            d = re.sub(r'\d+', '', d)
            d = d.lower()
            words = word_tokenize(d)
            word_tokens = []
            for token in words:
                if token not in stop_words:
                    word_tokens.append(token)
            words = [lemm.lemmatize(w, 'v') for w in word_tokens]
            sentence = ""
            for w in words:
                sentence = sentence + w + " "
            description[i] = sentence

        raw_data['story'] = description

        self.data = raw_data
