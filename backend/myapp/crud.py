from sqlalchemy.orm import Session
from myapp.models import FileMicrobiome, UserReproMB
from myapp.schemas import FileMicrobiomeSchema, UserReproMBSchema


def get_file_microbiome(db: Session, skip: int = 0, limit: int = 100):
    return db.query(FileMicrobiome).offset(skip).limit(limit).all()


def get_file_microbiome_by_id(db: Session, file_microbiome_id: int):
    return db.query(FileMicrobiome).filter(FileMicrobiome.id == file_microbiome_id).first()


def create_file_microbiome(db: Session, file_microbiome: FileMicrobiomeSchema):
    _file_microbiome = FileMicrobiome(filename=file_microbiome.filename, report_path=file_microbiome.report_path)
    db.add(_file_microbiome)
    db.commit()
    db.refresh(_file_microbiome)
    return _file_microbiome

def create_file_microbiome_by_name(db: Session, filename):
    _file_microbiome = FileMicrobiome(filename=filename, report_path="")
    db.add(_file_microbiome)
    db.commit()
    db.refresh(_file_microbiome)
    return _file_microbiome

def remove_file_microbiome(db: Session, file_microbiome_id: int):
    _file_microbiome = get_file_microbiome_by_id(db=db, file_microbiome_id=file_microbiome_id)
    db.delete(_file_microbiome)
    db.commit()


def update_file_microbiome(db: Session, file_microbiome_id: int, filename: str, report_path: str):
    _file_microbiome = get_file_microbiome_by_id(db=db, file_microbiome_id=file_microbiome_id)

    _file_microbiome.filename = filename
    _file_microbiome.report_path = report_path

    db.commit()
    db.refresh(_file_microbiome)
    return _file_microbiome

def create_user_repromb(db: Session, user_repromb: UserReproMBSchema):
    _user_repromb = UserReproMB(user=user_repromb.user, password=user_repromb.password)
    db.add(_user_repromb)
    db.commit()
    db.refresh(_user_repromb)
    return _user_repromb

def get_user_repromb_by_user(db: Session, user_repromb: str):
    return db.query(UserReproMB).filter(UserReproMB.user == user_repromb).first()
