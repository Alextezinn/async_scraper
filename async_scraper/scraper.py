import asyncio
import json
from typing import Dict, List

import aiohttp
import requests
from loguru import logger

from async_scraper.utils.configuration_logger import config
from constants import HEADERS, WEBSITE_URL, WEBSITE_PAGE_URL


logger.configure(**config)
data_list = []


async def get_possible_stores(item: Dict, possible_stores: List[str],
                              stores: List[Dict]) -> int:
    total_amount = 0

    for ps in possible_stores:
        if ps in item:
            if item[ps] is None or len(item[ps]) < 1:
                continue
            else:
                for store in item[ps]:

                    try:
                        store_name = store['STORE_NAME']
                        store_price = float(store['PRICE'])
                        store_amount = int(store['AMOUNT'])
                    except KeyError as err:
                        raise err

                    total_amount += store_amount

                    stores.append(
                        {
                            "store_name": store_name,
                            "store_price": store_price,
                            "store_amount": store_amount
                        }
                    )

        return total_amount


async def get_data_from_page(session: aiohttp.ClientSession, page_id: int) -> None:

    url = "".join([WEBSITE_PAGE_URL, str(page_id)])

    async with session.get(url=url, headers=HEADERS) as response:
        data = await response.text()

        try:
            data = json.loads(data)
        except json.decoder.JSONDecodeError as err:
            raise err

        try:
            items = data['items']
        except KeyError as err:
            raise err

        possible_stores = ["discountStores", "fortochkiStores", "commonStores"]
        for item in items:

            try:
                item_name = item['name']
                item_price = item['price']
            except KeyError as err:
                raise err

            item_img = f"{WEBSITE_URL}{item['imgSrc']}"
            item_url = f"{WEBSITE_URL}{item['url']}"

            stores = []
            total_amount = await get_possible_stores(item, possible_stores, stores)

            data_list.append(
                {
                    "name": item_name,
                    "price": item_price,
                    "url": item_url,
                    "img_url": item_img,
                    "stores": stores,
                    "total_amount": total_amount
                }
            )

        logger.info(f"Обработал {page_id} страницу")


def get_count_pages() -> int:
    with requests.Session() as session:
        url = "".join([WEBSITE_PAGE_URL, str(1)])

        try:
            response = session.get(url=url, headers=HEADERS)
        except requests.exceptions.ConnectionError as err:
            raise err
        else:
            pages_count = response.json()['pageCount']
            return pages_count


async def scraper(count_pages: int) -> None:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for page_id in range(1, count_pages + 1):
            task = asyncio.create_task(get_data_from_page(session, page_id))
            tasks.append(task)

        await asyncio.gather(*tasks)