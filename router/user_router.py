from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from schemas.schemas import  UserBase, UserDisplay
from db.database import get_db
from db import db_user


router = APIRouter(
    prefix = "/user",
    tags= ["user"]
)


@router.post("", response_model= UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    """
    Tạo thông tin người dùng vào CSDL
    """
    return db_user.create_user(db= db, request= request)