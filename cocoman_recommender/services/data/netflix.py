import re
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

import nltk
nltk.download('punkt')
nltk.download('wordnet')


class NetflixData:
    def __init__(self):
        self.data = None
        self.load_data()

    def load_data(self):
        lemm = WordNetLemmatizer()

        raw_data = pd.read_csv('../../datasets/netflix_titles.csv')

        description = raw_data['description'].copy()

        for i, d in enumerate(description):
            d = re.sub('[-=+,#/?:^$.@*\"~&%!()\[\]<>`\']', '', d)
            d = re.sub(r'\d+', '', d)
            d = d.lower()
            words = word_tokenize(d)
            words = [lemm.lemmatize(w, 'v') for w in words]
            sentence = ""
            for w in words:
                sentence = sentence + w + " "
            description[i] = sentence

        raw_data['description'] = description

        self.data = raw_data
