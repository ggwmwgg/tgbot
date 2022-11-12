from sqlalchemy import Integer, Column, BigInteger, String, sql, Float

from utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    lang_user = Column(String(100))
    number = Column(String(100))
    username = Column(String(100))
    orders_no = Column(Integer, default=0)
    referral = Column(BigInteger, default=id)
    cashback = Column(BigInteger, default=0)
    is_banned = Column(Integer, default=0)  # 0 - not banned, 1 - banned
    is_admin = Column(Integer, default=0)  # 1 = admin, 2 = operator, 3 = delivery
    last = Column(Integer, default=0)  # 0 = no, 1 = delivery, 2 = pickup
    latitude = Column(Float, default=0)
    longitude = Column(Float, default=0)
    branch = Column(String(100), default='Null')
    last_delivery = Column(Integer, default=0)

    query: sql.Select