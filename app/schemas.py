from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Product(BaseModel):
    product_id: int
    product_name: str
    product_price: int
    product_stock: int
    product_description: str


class Order(BaseModel):
    product_id: int
    quantity: int

class OrderOut(Order):
    order_id: int
    order_date: datetime
    order_status: str
    total_price: int

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config():
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None