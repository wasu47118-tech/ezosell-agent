# database.py

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Seller(Base):
    __tablename__ = 'sellers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String, unique=True)
    total_sales = Column(Float, default=0)
    total_commission = Column(Float, default=0)
    commission_paid = Column(Float, default=0)
    free_trial_end = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer)
    platform = Column(String)
    product_name = Column(String)
    amount = Column(Float)
    commission = Column(Float)
    order_date = Column(DateTime, default=datetime.now)

engine = create_engine('sqlite:///ezosell.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

print("✅ Database ready!")