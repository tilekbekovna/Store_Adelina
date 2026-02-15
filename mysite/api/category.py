from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Category
from mysite.database.schema import CategoryInputSchema, CategoryOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


category_router = APIRouter(prefix='/category', tags=['Category_nur Crud'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@category_router.post('/', response_model=CategoryOutSchema)
async def create_category(category: CategoryInputSchema, db: Session = Depends(get_db)):
    category_db = Category(**category.dict())
    db.add(category_db)
    db.commit()  
    db.refresh(category_db)
    return category_db


@category_router.get('/', response_model=List[CategoryOutSchema])
async def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@category_router.get('/{category_id}')
async def get_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(detail='мындай категори  жок', status_code=400)
    return category_db


@category_router.put('/{category_id}', response_model=dict)
async def update_category(category_id: int, category: CategoryInputSchema,
                          db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id==category_id).first()
    if not category:
        raise HTTPException(detail='Мындай категори жок', status_code=400)

    for category_key, category_value in category.dict().items():
        setattr(category_db, category_key, category_value)

    db.commit()
    db.refresh(category_db)
    return {'message': 'категоори озгорулду'}


@category_router.delete('{/category.db}', response_model=dict)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise  HTTPException(detail='Мындай категори жок', status_code=400)

    db.delete(category_db)
    db.commit()
    return {'message': 'Категори удалить болду'}













