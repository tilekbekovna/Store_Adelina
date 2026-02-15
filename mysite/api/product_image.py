from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import ProductImage
from mysite.database.schema import ProductImageInputSchema,ProductOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

product_image_router = APIRouter(prefix='/product_image', tags=['product_image_nur Crud'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@product_image_router.post('/', response_model=ProductOutSchema)
def create_product_image(product_image: ProductImageInputSchema, db: Session = Depends(get_db)):
    product_image_db = ProductImage(**product_image.dict())
    db.add(product_image_db)
    db.commit()
    db.refresh(product_image_db)
    return product_image_db


@product_image_router.get('/', response_model=List[ProductOutSchema])
def list_product_image(db: Session = Depends(get_db)):
    return db.query(ProductImage).all()


@product_image_router.get('/{productimage_id}')
def get_product_image(product_image_id: int, db: Session = Depends(get_db)):
    product_image_db = db.query(ProductImage).filter(ProductImage.id == product_image_id).first()
    if not product_image_db:
        raise HTTPException(detail='мындай маалымат жок', status_code=400)
    return product_image_db


@product_image_router.put('/{productimage_id}', response_model=dict)
async def update_productimage(productimage_id: int, productimage: ProductImageInputSchema, db: Session = Depends(get_db)):
    productimage_db = db.query(ProductImage).filter(ProductImage.id == productimage_id).first()
    if not productimage_db:
        raise HTTPException(detail='Мындай product image жок', status_code=400)
    for productimage_key, productimage_value in productimage.dict().items():
        setattr(productimage_db, productimage_key, productimage_value)
    db.commit()
    db.refresh(productimage_db)
    return {'message': 'productimage озгорулду'}

@product_image_router.delete('/{productimage_id}', response_model=dict)
async def delete_productimage(productimage_id: int, db: Session = Depends(get_db)):
    productimage_db = db.query(ProductImage).filter(ProductImage.id == productimage_id).first()
    if not productimage_db:
        raise HTTPException(detail='Мындай product image жок', status_code=400)
    db.delete(productimage_db)
    db.commit()
    return {'message': 'productimage удалить болду'}

