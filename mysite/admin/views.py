from symtable import Class

from pydantic_core.core_schema import model_field

from mysite.database.models import UserProfile, Category, Product, Review, SubCategory, ProductImage
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]

class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.category_name]

class ProductAdmin(ModelView, model=Product):
    column_list = [Product.product_name]


class ReviewAdmin(ModelView, model=Review):
    column_list = [Review.id, Review.product_id]


class ProductImageAdmin(ModelView, model=ProductImage):
    column_list = [ProductImage.id, ProductImage.product_id]


class SubCategoryAdmin(ModelView, model=SubCategory):
    column_list = [SubCategory.sub_category_name]
