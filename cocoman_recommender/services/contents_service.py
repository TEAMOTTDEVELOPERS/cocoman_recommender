import os.path
import shutil
from typing import List
from fastapi import UploadFile

from cocoman_recommender.config.config import BASE_DIR
from cocoman_recommender.models.contents_dto import ContentsDto
from cocoman_recommender.schemas.contents import ContentsRepository, Contents
from cocoman_recommender.schemas.ott import OttRepository
from cocoman_recommender.schemas.actor import ActorRepository
from cocoman_recommender.schemas.director import DirectorRepository
from cocoman_recommender.schemas.genre import GenreRepository
from cocoman_recommender.schemas.keyword import KeywordRepository


class ContentsService:
    def __init__(self,
                 contents_repository: ContentsRepository,
                 ott_repository: OttRepository,
                 actor_repository: ActorRepository,
                 director_repository: DirectorRepository,
                 genre_repository: GenreRepository,
                 keyword_repository: KeywordRepository):
        self.contents_repository = contents_repository
        self.ott_repository = ott_repository
        self.actor_repository = actor_repository
        self.director_repository = director_repository
        self.genre_repository = genre_repository
        self.keyword_repository = keyword_repository

    def find_all(self) -> List[Contents]:
        return self.contents_repository.get_all()

    def find_by_id(self, id: int) -> Contents:
        return self.contents_repository.get_by_id(id)

    def create(self, poster_file: UploadFile, contents_dto: ContentsDto):
        ott_list = []
        for ott_id in contents_dto.ott_set:
            ott = self.ott_repository.get_by_id(ott_id)
            ott_list.append(ott)

        actor_list = []
        for actor_id in contents_dto.actors_set:
            actor = self.actor_repository.get_by_id(actor_id)
            actor_list.append(actor)

        director_list = []
        for director_id in contents_dto.directors_set:
            director = self.director_repository.get_by_id(director_id)
            director_list.append(director)

        genre_list = []
        for genre_id in contents_dto.genres_set:
            genre = self.genre_repository.get_by_id(genre_id)
            genre_list.append(genre)

        keyword_list = []
        for keyword_id in contents_dto.keywords_set:
            keyword = self.keyword_repository.get_by_id(keyword_id)
            keyword_list.append(keyword)

        if poster_file.filename != '':
            _, extension = os.path.splitext(poster_file.filename)
            file_name = 'contents_' + contents_dto.title
            local_path = os.path.join(BASE_DIR + '/static/img' + file_name)
            with open(local_path, 'wb') as buffer:
                shutil.copyfileobj(poster_file.file, buffer)
            poster_path = os.path.join('/static/img' + file_name)
        else:
            poster_path = ''

        content = Contents(title=contents_dto.title,
                           year=contents_dto.year,
                           country=contents_dto.country,
                           running_time=contents_dto.running_time,
                           grade_rate=contents_dto.grade_rate,
                           broadcaster=contents_dto.broadcaster,
                           open_date=contents_dto.open_date,
                           broadcast_date=contents_dto.broadcast_date,
                           story=contents_dto.story,
                           poster_path=poster_path,
                           ott_id=ott_list,
                           actors_id=actor_list,
                           director_id=director_list,
                           genre_id=genre_list,
                           keyword_id=keyword_list
                           )

        self.contents_repository.create(content)

    def delete_by_id(self, id: int):
        content = self.contents_repository.get_by_id(id)

        if content.poster_path != '':
            local_path = os.path.join(BASE_DIR + content.poster_path)
            os.remove(local_path)

        self.contents_repository.delete_by_id(id)

    def update(self, id: int, poster_file: UploadFile, contents_dto: ContentsDto):
        ott_list = []
        for ott_id in contents_dto.ott_set:
            ott = self.ott_repository.get_by_id(ott_id)
            ott_list.append(ott)

        actor_list = []
        for actor_id in contents_dto.actors_set:
            actor = self.actor_repository.get_by_id(actor_id)
            actor_list.append(actor)

        director_list = []
        for director_id in contents_dto.directors_set:
            director = self.director_repository.get_by_id(director_id)
            director_list.append(director)

        genre_list = []
        for genre_id in contents_dto.genres_set:
            genre = self.genre_repository.get_by_id(genre_id)
            genre_list.append(genre)

        keyword_list = []
        for keyword_id in contents_dto.keywords_set:
            keyword = self.keyword_repository.get_by_id(keyword_id)
            keyword_list.append(keyword)

        content = self.contents_repository.get_by_id(id)

        if content.poster_path != '':
            local_path = os.path.join(BASE_DIR + content.poster_path)
            os.remove(local_path)

        if poster_file.filename != '':
            _, extension = os.path.splitext(poster_file.filename)
            file_name = 'contents_' + contents_dto.title
            local_path = os.path.join(BASE_DIR + '/static/img' + file_name)
            with open(local_path, 'wb') as buffer:
                shutil.copyfileobj(poster_file.file, buffer)
            poster_path = os.path.join('/static/img' + file_name)
        else:
            poster_path = ''

        content = Contents(title=contents_dto.title,
                           year=contents_dto.year,
                           country=contents_dto.country,
                           running_time=contents_dto.running_time,
                           grade_rate=contents_dto.grade_rate,
                           broadcaster=contents_dto.broadcaster,
                           open_date=contents_dto.open_date,
                           broadcast_date=contents_dto.broadcast_date,
                           story=contents_dto.story,
                           poster_path=poster_path,
                           ott_id=ott_list,
                           actors_id=actor_list,
                           director_id=director_list,
                           genre_id=genre_list,
                           keyword_id=keyword_list
                           )

        self.contents_repository.update(id, content)
