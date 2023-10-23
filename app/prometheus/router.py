import time
from random import random

from fastapi import APIRouter
from fastapi_versioning import version

router = APIRouter(
    prefix='/prometheus',
    tags=['test prometheus + grafana']
)


@router.get('/get_error')
@version(1)
def get_error():
    """Функция для теста Prometheus + Grafana."""
    if random() > 0.5:
        raise ZeroDivisionError
    else:
        raise KeyError


@router.get('/time_consumer')
@version(1)
def time_consumer():
    """Функция для теста Prometheus + Grafana."""
    time.sleep(random() * 5)
    return 'Тест завершен.'


@router.get('/memory_consumer')
@version(1)
def memory_consumer():
    """Функция для теста Prometheus + Grafana."""
    _ = [i for i in range(30_000_000)]
    return 'Тест завершен.'
