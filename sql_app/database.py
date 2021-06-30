from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import cloudinary

cloudinary.config(
    cloud_name= "hnduusros",
    api_key= "927131722149478",
    api_secret ="he5lFnOeoeRDBmV9z9QKCTxhLn0"
)

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app2.db"
#SQLALCHEMY_DATABASE_URL = "postgresql://dxuxmkvgbkorbr:9ab1a1ef687526acb51ca5ec8af36e8a0fe6b913380dedc45faa58deace9aa1a@ec2-54-145-224-156.compute-1.amazonaws.com:5432/ddqgm0v6j8voj4"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()