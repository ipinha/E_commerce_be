from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

password = 'sonha2612@'

# Mã hóa mật khẩu để đảm bảo chuỗi URL hợp lệ
encoded_password = quote_plus(password)

DATABASE_URL = f"mysql+pymysql://root:{encoded_password}@localhost/ecommerce"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit = False, autoflush= False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
