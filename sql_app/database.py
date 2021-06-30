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
SQLALCHEMY_DATABASE_URL = "postgresql://eqehnbihbtkmvy:c25ecd8c8e84970dd623a8d3f4be8e04aa16161f17a17ffea7b66b9245e58f12@ec2-54-162-119-125.compute-1.amazonaws.com:5432/daev0nklfg5klj"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()