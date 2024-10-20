from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm.session import Session
from fastapi.responses import FileResponse
from schemas.schemas import VehicleDisplay, VehicleBase
from db.database import get_db
from db import db_vehicles
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix="/vehicle",
    tags=["vehicle"]
)

# Tạo thông tin phương tiện của nhân viên vào CSDL
@router.post("", response_model= VehicleDisplay)
def create_vehicle(request: VehicleBase, db: Session = Depends(get_db)):
    """
    Tạo thông tin phương tiện của nhân viên vào CSDL

    """
    
    return db_vehicles.create_vehicle(db= db, request= request)