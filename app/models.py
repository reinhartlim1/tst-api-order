from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    order_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    order_status = Column(String, nullable=False, server_default="Waiting for payment")
    customer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id", ondelete="CASCADE"), nullable=False)
    total_price = Column(Integer, nullable=False)
    customer = relationship("User")
    product = relationship("Product")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, server_default="FALSE")

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, nullable=False)
    product_name = Column(String, nullable=False)
    product_price = Column(Integer, nullable=False)
    product_stock = Column(Integer, nullable=False)
    product_description = Column(String, nullable=False)