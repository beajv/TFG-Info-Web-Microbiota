from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from myapp.config import SessionLocal
from sqlalchemy.orm import Session
from myapp.schemas import UserReproMBSchema, Request, Response, RequestUserReproMBSchema
import myapp.crud as crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
async def create_file_microbiome(request: RequestUserReproMBSchema, db: Session = Depends(get_db)):
    crud.create_user_repromb(db, user_repromb=request.parameter)
    return Response(status="Ok",
                    code="201",
                    message="User created successfully").dict(exclude_none=True)


@router.get("/")
async def get_file_microbiomes(user: str, db: Session = Depends(get_db)):
    _user_repromb = crud.get_user_repromb_by_user(db,user)
    return Response(status="Ok", code="200", message="Success fetch all data", result=_user_repromb)


