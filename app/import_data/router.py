import codecs
import csv
from typing import Literal

from fastapi import APIRouter, UploadFile, status
from fastapi_versioning import version

from app.exceptions import CannotProcessCSVException, DatabaseErrorException

from .utils import TABLE_MODEL_MAP, convert_csv_to_postgres_format

router = APIRouter(
    prefix='/import',
    tags=['import']
)


@router.post(
    '/{table_name}',
    status_code=status.HTTP_201_CREATED
)
@version(1)
async def import_data_to_table(
    file: UploadFile,
    table_name: Literal[
        'categories', 'subcategories', 'goods', 'purchases', 'users'
    ]
):
    """Загружает тестовые данные в базу данных."""
    ModelDAO = TABLE_MODEL_MAP[table_name]
    csvreader = csv.DictReader(
        codecs.iterdecode(file.file, 'utf-8'), delimiter=';'
    )
    data = convert_csv_to_postgres_format(csvreader)
    file.file.close()
    if not data:
        raise CannotProcessCSVException
    added_data = await ModelDAO.add_objects(data)
    if not added_data:
        raise DatabaseErrorException(
            detail=('Не удалось добавить тестовые данные в базу данных.'
                    'Проверьте корректность данных.')
        )
    return 'Данные успешно загружены.'
