import os
import aiohttp
import asyncio
from aiohttp import ClientResponseError, ClientError

from backend.core.logging import logger
from backend.db.init_db import init_db_for_script
from backend.models import Image
from typing import List


async def download_image_with_retry(url: str, filename: str, max_retries: int = 2, timeout: int = 10) -> None:
    retries = 0
    while retries <= max_retries:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=timeout) as response:
                    if response.status == 200:
                        content = await response.read()
                        save_path = os.path.join("images", filename)
                        with open(save_path, "wb") as f:
                            f.write(content)
                        print(f"Downloaded and saved: {filename}")
                    else:
                        print(f"Failed to download: {filename}. Status code: {response.status}")
            return
        except (ClientError, ClientResponseError, asyncio.TimeoutError) as e:
            print(f"Error downloading {filename}. Retrying... ({retries + 1}/{max_retries + 1})\n{e}")
            retries += 1
            await asyncio.sleep(1)

    print(f"Failed to download {filename} after {max_retries + 1} attempts.")


async def download_images(images: List[Image]) -> None:
    tasks = []

    for image in images:
        image_name: str = image.image_url.split("/")[-1]
        thumbnail_name: str = image.thumbnail_url.split("/")[-1]
        medium_thumbnail_name: str = image.medium_thumbnail_url.split("/")[-1]

        if not os.path.exists(f"images/{image_name}"):
            tasks.append(download_image_with_retry(image.image_url, image_name))

        if not os.path.exists(f"images/{thumbnail_name}"):
            tasks.append(download_image_with_retry(image.thumbnail_url, thumbnail_name))

        if not os.path.exists(f"images/{medium_thumbnail_name}"):
            tasks.append(download_image_with_retry(image.medium_thumbnail_url, medium_thumbnail_name))

    await asyncio.gather(*tasks)


async def main() -> None:
    logger.info("Initializing database...")
    await init_db_for_script()

    logger.info("Getting all images from DB...")
    images: List[Image] = await Image.all()

    os.makedirs("images", exist_ok=True)

    logger.info("Downloading images...")
    await download_images(images)


if __name__ == "__main__":
    '''
    A script for downloading all of the product images from the URLs provided in the DB.
    
    A folder called 'images' will be created, if it doesn't already exist. Any file name that we find in the DB, that 
    is not already in this folder, will be downloaded.
    '''
    asyncio.run(main())
