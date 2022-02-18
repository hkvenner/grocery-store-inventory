from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Brand(Base):
    __tablename__ = 'brands'

    brand_id = Column(Integer, primary_key=True)
    brand_name = Column(String)

    def __repr__(self):
        return f'<Brand(name={self.brand_name})'


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer)
    date_updated = Column(DateTime)
    brand_id = Column(Integer, ForeignKey("brands.brand_id"))

    def __repr__(self):
        return f'<Product(name={self.product_name}, quantity={self.product_quantity}, price={self.product_price}, date_updated ={self.date_updated}, brand_id ={self.brand_id})'

