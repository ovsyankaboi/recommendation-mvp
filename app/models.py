from sqlalchemy import Column, String, Enum, DateTime, JSON, Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
import enum, datetime
from uuid import uuid4

Base = declarative_base()

class UserStatus(str, enum.Enum):
    active = "active"
    suspended = "suspended"

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.active)
    purchases = relationship("Purchase", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="user")

class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    product_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    total_price = Column(DECIMAL, nullable=False)
    purchase_date = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="purchases")

class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    items = Column(JSON, nullable=False)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="recommendations")
