from pydantic import BaseModel
from typing import List


class ContentsDto(BaseModel):
    title: str
    year: str
    country: str
    running_time: int
    grade_rate: str
    broadcaster: str
    open_date: str
    broadcast_date: str
    story: str
    ott_set: List[int]
    actors_set: List[int]
    directors_set: List[int]
    genres_set: List[int]
    keywords_set: List[int]
