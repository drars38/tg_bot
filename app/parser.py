import httpx
import asyncio
from bs4 import BeautifulSoup
import logging
from random import randint

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)


async def pars(url: str = 'https://vostok.transneft.ru/media-center/'):
    await asyncio.sleep(randint(1, 5))  # Имитируем случайную задержку

    async with httpx.AsyncClient() as session:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50'
        }

        logging.debug(f'Запрос к {url} с заголовками {headers}')
        response = await session.get(url=url, headers=headers)

        logging.debug(f'Получен ответ с кодом состояния: {response.status_code}')

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml').find('ul', class_='list-news')
            elements = soup.find_all('a', href=True)
            dict_links_text = {}

            for el in elements:
                el_link = el['href']
                el_text = el.text.strip()  # Убираем лишние пробелы
                dict_links_text[el_text] = el_link

            logging.debug(f'Спарсенные данные: {dict_links_text}')

            return dict_links_text
        else:
            logging.error(f'Не удалось получить данные с сайта. Код состояния: {response.status_code}')
            return {}



