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

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app2.db" + connect_args={'check_same_thread': False}
#SQLALCHEMY_DATABASE_URL = "postgresql://tpijxvtyifqxwg:d5369183ba8301095bf3aa019811776a6e119d6c8da0f0c88256cce1ea4f9393@ec2-3-212-75-25.compute-1.amazonaws.com:5432/d347hqgn8ik60i"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:J8v5.f675@localhost/granjas_test1"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()