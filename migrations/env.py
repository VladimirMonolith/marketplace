from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.categories.models import Category
from app.config import settings
from app.database.db import Base
from app.goods.models import Goods
from app.purchases.models import Purchase
from app.subcategories.models import Subcategory
from app.users.models import User

config = context.config

config.set_main_option('sqlalchemy.url', f'{settings.DATABASE_URL}?async_fallback=True')

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata