from datetime import datetime
from typing import Iterable

from app.categories.dao import CategoryDAO
from app.goods.dao import GoodsDAO
from app.logger import logger
from app.purchases.dao import PurchaseDAO
from app.subcategories.dao import SubcategoryDAO
from app.users.dao import UserDAO

TABLE_MODEL_MAP = {
    'categories': CategoryDAO,
    'subcategories': SubcategoryDAO,
    'goods': GoodsDAO,
    'purchases': PurchaseDAO,
    'users': UserDAO
}


def convert_csv_to_postgres_format(csv_iterable: Iterable):
    """Конвертирует csv в формат PosgreSQL."""
    try:
        data = []
        for row in csv_iterable:
            for key, value in row.items():
                if value.isdigit():
                    row[key] = int(value)
                elif 'when' in key:
                    row[key] = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                elif 'registrated' in key:
                    row[key] = datetime.strptime(value, '%Y-%m-%d')
            data.append(row)
        return data
    except Exception as error:
        logger.error(f'An error has occurred: {error}', exc_info=True)
        return None
