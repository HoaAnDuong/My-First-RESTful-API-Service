import sqlalchemy
from sqlalchemy import *
import os
dir = os.getcwd()
dir += "\ "
engine = sqlalchemy.create_engine(f"sqlite:///{dir}database.db")

