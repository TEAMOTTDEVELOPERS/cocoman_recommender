import re
import pandas as pd
from konlpy.tag import Okt

from cocoman_recommender.config.config import BASE_DIR


class GenreKorData:
    def __init__(self):
        self.data = None
        self.load_data()

    def load_data(self):
        okt = Okt()
        raw_data = pd.read_csv(BASE_DIR + '/datasets/justwatch_kr.csv')

        description = raw_data['story'].copy()

        for i, d in enumerate(description):
            d = re.sub('[-=+,#/?:^$.@*\"~&%!()\[\]<>`\']', '', d)
            d = re.sub(r'\d+', '', d)
            words = okt.pos(d, norm=True, stem=True)

            nouns = []
            for word, pos in words:
                if pos == 'Noun' and pos == 'Verb':
                    nouns.append(word)

            sentence = ""
            for n in nouns:
                sentence = sentence + n + " "
            description[i] = sentence

        raw_data['story'] = description
        self.data = raw_data
