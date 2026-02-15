from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import UserProfile
from mysite.database.schema import UserProfileInputSchema, UserProfileOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


user_router = APIRouter(prefix='/users', tags=['User_nur Crud'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.post('/', response_model=UserProfileOutSchema)
def create_user(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = UserProfile(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@user_router.get('/', response_model=List[UserProfileOutSchema])
async def list_user(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()

@user_router.get('/{user_id', response_model=UserProfileOutSchema)
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user_db:
        raise HTTPException(detail='мындай маалымат жок', status_code=400)
    return user_db


@user_router.put("/{userprofile_id}", response_model=UserProfileOutSchema)
async def update_userprofile(userprofile_id: int, userprofile: UserProfileInputSchema,
                             db: Session = Depends(get_db)):
    userprofile_db = db.query(UserProfile).filter(UserProfile.id == userprofile_id).first()

    if not userprofile_db:
        raise HTTPException(detail="Мындай userprofile жок", status_code=400,)

    for userprofile_key, userprofile_value in userprofile.dict().items():
        setattr(userprofile_db, userprofile_key, userprofile_value)

    db.commit()
    db.refresh(userprofile_db)
    return {'message': 'userprofile озгорулду'}


@user_router.delete("/{userprofile_id}", response_model=dict)
async def delete_userprofile(
    userprofile_id: int, db: Session = Depends(get_db)):
    userprofile_db = db.query(UserProfile).filter(UserProfile.id == userprofile_id).first()
    if not userprofile_db:
        raise HTTPException(detail="Мындай userprofile жок", status_code=400)


    db.delete(userprofile_db)
    db.commit()
    return {"message": "UserProfile удалтетилди"}



