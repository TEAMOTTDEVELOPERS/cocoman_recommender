from pydantic import BaseModel


class OttDto(BaseModel):
    id: str
    name: str
    image_path: str
