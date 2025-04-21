from sqlalchemy.orm import Session
from . import models

def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_purchase(db: Session, purchase):
    db_pur = models.Purchase(
        user_id=purchase.user_id,
        product_id=purchase.product_id,
        quantity=purchase.quantity,
        total_price=purchase.total_price
    )
    db.add(db_pur)
    db.commit()
    db.refresh(db_pur)
    return db_pur

def list_purchases(db: Session, user_id: str):
    return db.query(models.Purchase).filter(models.Purchase.user_id == user_id).all()

def create_recommendation(db: Session, user_id: str, items: list):
    rec = models.Recommendation(user_id=user_id, items=items)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec
