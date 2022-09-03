from pydantic import BaseModel


class Video(BaseModel):
    video: str
    thumbnail: str
