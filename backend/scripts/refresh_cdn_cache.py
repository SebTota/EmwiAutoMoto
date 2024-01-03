import asyncio
import aiohttp
from aiohttp import ClientResponseError, ClientError

from backend.core.logging import logger
from backend.db.init_db import init_db_for_script
from backend.models import Image


async def make_http_request_with_retry(url: str, max_retries: int = 2) -> str:
    retries = 0
    while retries <= max_retries:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    await response.read()
                    return response.headers.get('cf-cache-status', 'MISS')
        except (ClientError, ClientResponseError) as e:
            print(e, flush=True)
            logger.error(f"Error making request to {url}. Retrying... ({retries + 1}/{max_retries + 1})\n{e}")
            retries += 1
            await asyncio.sleep(1)

    raise RuntimeError(f"Failed to make HTTP request to {url} after {max_retries + 1} attempts.")


async def refresh_cdn_cache(image: Image, concurrent_runs: asyncio.Semaphore):
    try:
        # Make asynchronous HTTP requests for image URLs concurrently
        async with concurrent_runs:
            cf_cache_status_image_url = await make_http_request_with_retry(image.image_url)
        async with concurrent_runs:
            cf_cache_status_thumbnail_url = await make_http_request_with_retry(image.thumbnail_url)
        async with concurrent_runs:
            cf_cache_status_medium_thumbnail_url = await make_http_request_with_retry(image.medium_thumbnail_url)

        if cf_cache_status_image_url == 'HIT':
            logger.info(f"Cache HIT for {image.image_url}")
        else:
            logger.info(f"Cache MISS for {image.image_url}")

        if cf_cache_status_thumbnail_url == 'HIT':
            logger.info(f"Cache HIT for {image.thumbnail_url}")
        else:
            logger.info(f"Cache MISS for {image.thumbnail_url}")

        if cf_cache_status_medium_thumbnail_url == 'HIT':
            logger.info(f"Cache HIT for {image.medium_thumbnail_url}")
        else:
            logger.info(f"Cache MISS for {image.medium_thumbnail_url}")

    except Exception as e:
        logger.error(f"Error refreshing CDN cache for {image.image_url}:\n{e}")
    finally:
        pass


async def get_all_images() -> [Image]:
    return await Image.all()


async def main():
    logger.info("Initializing database...")
    await init_db_for_script()

    logger.info("Fetching all images from database...")
    images: [Image] = await get_all_images()
    logger.info(f"Retrieved {len(images)} image objects from the db. That equates to {len(images) * 3} image requests.")

    concurrent_runs = asyncio.Semaphore(3)

    # Refresh CDN cache for all images concurrently
    logger.info("Refreshing CDN cache for all images...")
    await asyncio.gather(*[refresh_cdn_cache(image, concurrent_runs) for image in images])


if __name__ == '__main__':
    asyncio.run(main())
