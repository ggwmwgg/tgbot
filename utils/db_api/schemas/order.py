from sqlalchemy import Integer, Column, BigInteger, String, sql, JSON, Float

from utils.db_api.db_gino import TimedBaseModel


class Order(TimedBaseModel):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    p_type = Column(String(100))
    #list = Column(String)
    #quantity = Column(String)
    items = Column(JSON, nullable=True, server_default="{}")
    comment = Column(String, default="Null")
    total_price = Column(BigInteger, default=0)
    delivery_price = Column(BigInteger, default=0)
    cashback = Column(BigInteger, default=0)
    type_delivery = Column(Integer, default=0) # 1 = delivery, 2 = pickup
    status = Column(Integer, default=1)
    # status (1 = активный, 2 = подтвержден, 3 = приготовление, 4 = доставка, 5 = доставлен, 6 = отменен)
    is_paid = Column(Integer, default=0)
    lon = Column(Float, default=0)
    lat = Column(Float, default=0)
    branch = Column(String(100))
    #courier_id = Column(Integer, default=0)
    date_paid = Column(String(100), default='Null')


    query: sql.Select