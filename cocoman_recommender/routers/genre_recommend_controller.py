from typing import List

from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from dependency_injector.wiring import inject, Provide

from cocoman_recommender.containers import Container

from cocoman_recommender.services.recommender_service import GenreRecommenderService

router = APIRouter()


@cbv(router)
class GenreRecommendController:
    @inject
    def __init__(self,
                 genre_recommender_service: GenreRecommenderService = Depends(Provide[Container.genre_recommender])):
        self.genre_recommender_service = genre_recommender_service

    @router.post('/genre/{lang}')
    async def genre_recommend(self, lang: str, query: List[str]):
        contents_ids = self.genre_recommender_service.recommend(query, lang)
        return JSONResponse(content=contents_ids)
