from sqlalchemy import Integer, Column, BigInteger, String, sql

from utils.db_api.db_gino import BaseModel


class Item(BaseModel):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name_ru = Column(String(100))
    name_uz = Column(String(100))
    name_en = Column(String(100))
    d_ru = Column(String(444))
    d_uz = Column(String(444))
    d_en = Column(String(444))
    photo = Column(String(444))
    price = Column(BigInteger)
    available = Column(Integer, default=1)
    amount = Column(Integer, default=999)
    cat_ru = Column(String(100))
    cat_uz = Column(String(100))
    cat_en = Column(String(100))



    query: sql.Select