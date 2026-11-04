from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.orm import declarative_base,sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()
database_url=os.getenv("url")
engine=create_engine(database_url)
sessionlocal=sessionmaker(bind=engine)

base=declarative_base()

class user_info(base):
    __tablename__="user_info"
    id=Column(Integer,primary_key=True)
    name=Column(String)
    pas=Column(String)

base.metadata.create_all(engine)


def get_db():
    session=sessionlocal()
    db=session

    try:
        yield db

    finally:
        db.close()
        