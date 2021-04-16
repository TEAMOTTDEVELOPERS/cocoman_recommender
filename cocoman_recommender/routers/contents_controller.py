from fastapi import Depends, UploadFile, File
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from dependency_injector.wiring import inject, Provide

from cocoman_recommender.models.contents_dto import ContentsDto
from cocoman_recommender.services.contents_service import ContentsService
from cocoman_recommender.containers import Container

router = InferringRouter()


@cbv(router)
class ContentsController:
    @inject
    def __init__(self, contents_service: ContentsService = Depends(Provide[Container.contents_service])):
        self.contents_service = contents_service

    @router.post('/all')
    async def get_all(self):
        return self.contents_service.find_all()

    @router.post('/{id}')
    async def get_by_id(self, id: int):
        return self.contents_service.find_by_id(id)

    @router.post('/create')
    async def create(self, contents_dto: ContentsDto, poster_file: UploadFile = File(...)):
        return self.contents_service.create(poster_file, contents_dto)

    @router.post('/delete')
    async def delete(self, id: int):
        return self.contents_service.delete_by_id(id)

    @router.post('/update/{id}')
    async def update(self, id: int, contents_dto: ContentsDto, poster_file: UploadFile = File(...)):
        return self.contents_service.update(id, poster_file, contents_dto)
