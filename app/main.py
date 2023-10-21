import time

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.models import (
    CategoryAdmin,
    GoodsAdmin,
    PurchasesAdmin,
    SubcategoryAdmin,
    UserAdmin
)
from app.categories.router import router as categories_router
from app.config import settings
from app.database.connection import engine
from app.goods.router import router as goods_router
from app.import_data.router import router as import_data_router
from app.logger import logger
from app.purchases.router import router as purchases_router
from app.subcategories.router import router as subcategories_router
from app.users.config import auth_backend
from app.users.manager import fastapi_users
from app.users.schemas import UserCreate, UserRead, UserUpdate

sentry_sdk.init(
    dsn='https://0005ee3146a5c373c2f48ae450e58453@o1384117.'
        'ingest.sentry.io/4506021194366976',
    traces_sample_rate=1.0
)

app = FastAPI(title='marketplace')


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix='/auth',
    tags=['auth'],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='/auth',
    tags=['auth'],
)

app.include_router(
    fastapi_users.get_users_router(
        UserRead, UserUpdate, requires_verification=True
    ),
    prefix='/users',
    tags=['users'],
)

app.include_router(import_data_router)
app.include_router(categories_router)
app.include_router(subcategories_router)
app.include_router(goods_router)
app.include_router(purchases_router)
app.include_router(prometheus_router) 

app = VersionedFastAPI(
    app,
    version_format='{major}',
    prefix_format='/v{major}',
)

admin = Admin(
    app=app, engine=engine, authentication_backend=authentication_backend
)

admin.add_view(UserAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(SubcategoryAdmin)
admin.add_view(GoodsAdmin)
admin.add_view(PurchasesAdmin)


@app.on_event('startup')
def startup():
    logger.info(f'Service {app.title} started.')
    redis = aioredis.from_url(
        f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}'
    )
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


@app.on_event('shutdown')
def shutdown_event():
    logger.info(f'Service {app.title} exited.')


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    """Добавляет заголовок со временем выполнения запроса."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        'Request handlinf time',
        extra={'process_time': round(process_time, 4)}
    )
    return response
