from pydantic import BaseModel, EmailStr
from typing import List
import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserRead(BaseModel):
    id: str
    name: str
    email: EmailStr

class PurchaseCreate(BaseModel):
    user_id: str
    product_id: str
    quantity: int
    total_price: float

class PurchaseRead(PurchaseCreate):
    id: str
    purchase_date: datetime.datetime

class RecommendationItem(BaseModel):
    product_id: str
    score: int
    rank: int

class RecommendationRead(BaseModel):
    id: str
    user_id: str
    items: List[RecommendationItem]
    generated_at: datetime.datetime
