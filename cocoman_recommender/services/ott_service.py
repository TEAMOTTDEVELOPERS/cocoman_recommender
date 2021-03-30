from typing import List

from cocoman_recommender.models.ott_dto import OttDto
from cocoman_recommender.schemas.ott import OttRepository


class OttService:
    def __init__(self, ott_repository: OttRepository):
        self.ott_repository = ott_repository

    def find_all(self) -> List[OttDto]:
        return self.ott_repository.get_all()
