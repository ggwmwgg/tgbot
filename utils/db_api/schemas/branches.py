from sqlalchemy import Integer, Column, BigInteger, String, sql, Float, JSON
from utils.db_api.db_gino import BaseModel


class Branch(BaseModel):
    __tablename__ = 'branches'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(JSON, nullable=True, server_default="{}")
    contacts = Column(String)
    w_from = Column(BigInteger, default=0)
    w_till = Column(BigInteger, default=0)
    is_active = Column(Integer, default=1) # 1 - active, 0 - not active



    query: sql.Select