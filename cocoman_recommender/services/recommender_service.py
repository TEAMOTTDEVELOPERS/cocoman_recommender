from typing import List

from cocoman_recommender.schemas.contents import ContentsRepository
from cocoman_recommender.services.data.genre_eng import GenreEngData
from cocoman_recommender.services.data.genre_kor import GenreKorData
from cocoman_recommender.services.dnn_models.genre_recommender import GenreRecommender


class GenreRecommenderService:
    def __init__(self, contents_repository: ContentsRepository):
        self.contents_repository = contents_repository

    def recommend(self, query: List[str], lang='kr'):
        if lang == 'kr':
            genre_data = GenreKorData()
        elif lang == 'eng':
            genre_data = GenreEngData()
        else:
            raise Exception('Not support this language : ' + lang)

        result_query = ''
        for q in query:
            result_query += (q + " ")

        recommender = GenreRecommender(genre_data.data['story'])
        indices = recommender.recommend(result_query[0:-1])

        result_index = []
        for i in indices:
            contents = self.contents_repository.get_by_title(genre_data['title'][i])

            result_index.append(contents.id)

        return result_index
