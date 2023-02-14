from typing import List

from fastapi import Depends, FastAPI, HTTPException,status,Response
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

# create Database Table
models.Base.metadata.create_all(bind=engine)


app = FastAPI()


#Create Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print("request data is ",user)
    print("db is",db)
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.delete("/items/{user_id}/",response_model=schemas.User)
def delete_user(user_id:int,db:Session=Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == user_id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User not Exist')
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.patch("items/{user_id}/",response_model=schemas.User)
def updateUser(user_id:int,user:schemas.UserCreate ,db:Session=Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == user_id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {user_id} found')
    update_data = user.dict(exclude_unset=True)
    user_query.filter(models.User.id == user_id).update(update_data,
                                                       synchronize_session=False)
    db.commit()
    db.refresh(user)
    return {"status": "success", "note": user}

    

@app.get("/")
def root():
    return {"message":"Welcome to fastAPI and SQLAlchemy"}