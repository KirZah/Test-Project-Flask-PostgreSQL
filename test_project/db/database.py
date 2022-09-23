from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://kirill:NJxBTLieFM0b@192.168.2.4:5432/farm_manager"

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL,
    pool_size=5,  # number of connections
    max_overflow=10,  # how many exceeding connections
    pool_recycle=-1,  # reconnection period
    pool_timeout=30,
    # connect_args={"check_same_thread": False}  # for sqlite
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Экземпляр SessionLocal() отвечает за все обращения к базе данных
# и представляет «промежуточную зону» для всех объектов,
# загруженных в объект сессии базы данных.
Base = declarative_base()
