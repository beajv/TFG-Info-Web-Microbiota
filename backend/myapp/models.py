from sqlalchemy import  Column, Integer, String
from myapp.config import Base

class FileMicrobiome(Base):
    __tablename__ ="files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    report_path = Column(String)
    site = Column(String)
    project = Column(String)
    size = Column(String)
    
    
class UserReproMB(Base):
    __tablename__ ="users"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String)
    password = Column(String)
    email = Column(String)
    active = Column(String)
    admin = Column(String)
