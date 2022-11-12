from sqlalchemy import Integer, Column, BigInteger, String, sql
from utils.db_api.db_gino import BaseModel


class Cart(BaseModel):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    item_id = Column(Integer)
    quantity = Column(Integer)
    price = Column(BigInteger)



    query: sql.Select