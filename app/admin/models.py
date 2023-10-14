from sqladmin import ModelView

from app.categories.models import Category
from app.goods.models import Goods
from app.purchases.models import Purchase
from app.subcategories.models import Subcategory
from app.users.models import User


class UserAdmin(ModelView, model=User):
    """Класс для отображения пользователей в админке."""

    column_list = [c.name for c in User.__table__.c]
    column_details_exclude_list = [User.hashed_password]
    column_list += [User.purchases]
    can_delete = True
    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = 'fa-solid fa-user'


class CategoryAdmin(ModelView, model=Category):
    """Класс для отображения категорий в админке."""

    column_list = [c.name for c in Category.__table__.c]
    column_list += [Category.subcategories]
    name = 'Категория'
    name_plural = 'Категории'
    icon = 'fa-solid fa-folder'


class SubcategoryAdmin(ModelView, model=Subcategory):
    """Класс для отображения подкатегорий в админке."""

    column_list = [c.name for c in Subcategory.__table__.c]
    column_list += [Subcategory.category, Subcategory.goods]
    name = 'Подкатегория'
    name_plural = 'Подкатегории'
    icon = 'fa-solid fa-folder-open'


class GoodsAdmin(ModelView, model=Goods):
    """Класс для отображения товаров в админке."""

    column_list = [c.name for c in Goods.__table__.c]
    column_list += [Goods.subcategory, Goods.purchases]
    name = 'Товар'
    name_plural = 'Товары'
    icon = 'fa-solid fa-database'


class PurchasesAdmin(ModelView, model=Purchase):
    """Класс для отображения покупок в админке."""

    column_list = [c.name for c in Purchase.__table__.c]
    column_list += [Purchase.buyer, Purchase.goods]
    name = 'Покупка'
    name_plural = 'Покупки'
    icon = 'fa-solid fa-coins'
