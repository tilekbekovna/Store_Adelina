

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DB_URL = "postgresql://postgres:20090929@localhost/shop_app_pi09"


engine = create_engine(DB_URL)


SessionLocal = sessionmaker(bind=engine)


Base = declarative_base()




