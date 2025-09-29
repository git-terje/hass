import os
import pymysql  # <- registrerer PyMySQL som driver
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
