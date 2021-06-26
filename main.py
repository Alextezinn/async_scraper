import time
import datetime
import sys
import asyncio
import json

from loguru import logger

from async_scraper.utils.configuration_logger import config
from async_scraper.scraper import get_count_pages, scraper, data_list


logger.configure(**config)


if __name__ == "__main__":
    start_time = time.time()

    try:
        count_pages = get_count_pages()
    except Exception as err:
        logger.error(err)
        sys.exit(-1)

    try:
        asyncio.run(scraper(count_pages))
    except Exception as err:
        logger.error(err)
        sys.exit(-1)

    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    try:
        with open(f"data_{cur_time}.json", "a") as file:
            json.dump(data_list, file, indent=4, ensure_ascii=False)
    except Exception as err:
        logger.error(err)
        sys.exit(-1)

    logger.info(time.time() - start_time)