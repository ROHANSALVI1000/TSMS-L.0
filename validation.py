from pydantic import BaseModel

class API(BaseModel):
    id:int
    name:str
    pas:str

class USER(BaseModel):
    name:str
    pas:str