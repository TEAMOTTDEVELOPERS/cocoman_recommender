from typing import List
from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from dependency_injector.wiring import inject, Provide

from cocoman_recommender.models.ott_dto import OttDto
from cocoman_recommender.services.ott_service import OttService
from cocoman_recommender.containers import Container

router = InferringRouter(prefix='/ott')


@cbv(router)
@inject
class OttController:
    def __init__(self, ott_service: OttService = Depends(Provide[Container.ott_service])):
        self.ott_service = ott_service

    @router.post('/all', response_model=List[OttDto])
    async def get_all(self):
        return self.ott_service.find_all()
