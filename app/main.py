from fastapi import FastAPI, Depends, HTTPException
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from . import crud, schemas, services, database, models

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users", response_model=schemas.UserRead)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/purchases", response_model=schemas.PurchaseRead)
def create_purchase_endpoint(purchase: schemas.PurchaseCreate, db: Session = Depends(get_db)):
    return crud.create_purchase(db, purchase)

@app.get("/recommendations/{user_id}", response_model=schemas.RecommendationRead)
def get_recommendations_endpoint(user_id: str, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return services.generate_recommendations(db, user_id)

@app.get("/debug/purchases/count")
def count_purchases(db: Session = Depends(get_db)):
    return {"count": db.query(models.Purchase).count()}
