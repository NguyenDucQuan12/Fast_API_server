from fastapi import APIRouter, Query, Depends, status, UploadFile, File, HTTPException
from sqlalchemy.orm.session import Session
from schemas.schemas import EmployeeDisplay, EmployeeBase, UserAuth
from db.database import get_db
from db import db_employee
from file.save_avatar import save_avatar_upload_from_user
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix="/ocr",
    tags=["ocr"]
)
