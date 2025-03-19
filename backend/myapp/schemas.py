from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel , Field
from pydantic.generics import GenericModel

T = TypeVar('T')


class FileMicrobiomeSchema(BaseModel):
    id: Optional[int] = None
    filename: Optional[str] = None
    report_path: Optional[str] = None
    site: Optional[str] = None
    project: Optional[str] = None
    size: Optional[str] = None

    class Config:
        orm_mode = True

class UserReproMBSchema(BaseModel):
    id: Optional[int] = None
    user: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    active: Optional[str] = None

    class Config:
        orm_mode = True

class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)

class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]

class RequestFileMicrobiome(BaseModel):
    parameter: FileMicrobiomeSchema = Field(...)

class RequestUserReproMBSchema(BaseModel):
    parameter: UserReproMBSchema = Field(...)



