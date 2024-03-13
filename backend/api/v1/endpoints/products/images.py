import concurrent.futures
import io
import uuid
from typing import Any, List

from backend.core.logging import logger
from fastapi import APIRouter, Depends, HTTPException, UploadFile, BackgroundTasks
from PIL import Image as PIL_Image

from backend.models import User, MediaType
from backend.schemas import MediaRead
from backend.exceptions import FileUploadError
from backend.utils import deps
from backend.utils.image_handler import process_image

router = APIRouter()


@router.post('', response_model=List[MediaRead])
def generate_motorcycle_images(
        files: List[UploadFile],
        background_tasks: BackgroundTasks,
        current_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    def process_single_image(file):
        image_content = file.file.read()
        img = PIL_Image.open(io.BytesIO(image_content))

        try:
            name: str = f'{str(uuid.uuid4())}.{file.filename.split(".")[-1]}'
            [image_url, thumbnail_url, medium_thumbnail_url] = process_image(img, name)
            img.close()
            file.file.close()
            return MediaRead(type=MediaType.IMAGE,
                             url=image_url,
                             thumbnail_url=thumbnail_url,
                             medium_thumbnail_url=medium_thumbnail_url)
        except FileUploadError as e:
            logger.error("Failed to process image.", e)
            img.close()
            file.file.close()
            raise HTTPException(status_code=500, detail='Failed to process image.')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        image_results = list(executor.map(process_single_image, files))

    return image_results
