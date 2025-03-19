from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from myapp.config import SessionLocal
from sqlalchemy.orm import Session
from myapp.schemas import FileMicrobiomeSchema, Request, Response, RequestFileMicrobiome
import myapp.crud as crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
async def create_file_microbiome_service(request: RequestFileMicrobiome, db: Session = Depends(get_db)):
    crud.create_file_microbiome(db, file_microbiome=request.parameter)
    return Response(status="Ok",
                    code="200",
                    message="File created successfully").dict(exclude_none=True)


@router.get("/")
async def get_file_microbiomes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _file_microbiomes = crud.get_file_microbiome(db, skip, limit)
    return Response(status="Ok", code="200", message="Success fetch all data", result=_file_microbiomes)


@router.patch("/update")
async def update_file_microbiome(request: RequestFileMicrobiome, db: Session = Depends(get_db)):
    _file_microbiome = crud.update_file_microbiome(db, file_microbiome_id=request.parameter.id,
                             title=request.parameter.title, description=request.parameter.description)
    return Response(status="Ok", code="200", message="Success update data", result=_file_microbiome)


@router.delete("/delete")
async def delete_file_microbiome(request: RequestFileMicrobiome,  db: Session = Depends(get_db)):
    crud.remove_file_microbiome(db, file_microbiome_id=request.parameter.id)
    return Response(status="Ok", code="200", message="Success delete data").dict(exclude_none=True)



