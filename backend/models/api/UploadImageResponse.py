from pydantic.main import BaseModel


class UploadImageResponse(BaseModel):
    thumbnail: str
    image: str
