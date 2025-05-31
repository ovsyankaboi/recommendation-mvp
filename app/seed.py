# app/seed.py
import os
import csv
from app.models import User, UserStatus
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import create_purchase

def seed_movielens_ratings(path: str):
    db: Session = SessionLocal()
    count = 0
    user_file = os.path.join(os.path.dirname(path), 'u.user')
    if os.path.exists(user_file):
        created = 0
        print("Seeding ratings from:", path)
        print("File size (bytes):", os.path.getsize(path))

        with open(user_file, encoding='latin-1') as fu:
            for line in fu:
                user_id, *_ = line.strip().split('|')
                db.add(User(
                    id=str(user_id),
                    name=f"ML_User_{user_id}",
                    email=f"{user_id}@movielens",
                    status=UserStatus.active
                ))
                created += 1
        db.commit()
        print(f"Seeded {created} users into Users table.")
    else:
        print(f"User file not found at {user_file}")

    with open(path, encoding='latin-1') as f:
        for line in f:
            parts = line.strip().split('::')
            if len(parts) != 4:
                parts = line.strip().split('\t')
            user_id, item_id, rating, _ = parts
            create_purchase(
                db,
                type('P', (), {
                    'user_id': user_id,
                    'product_id': item_id,
                    'quantity': 1,
                    'total_price': float(rating)
                })
            )
            count += 1

    db.close()
    print(f"Seeded {count} ratings into Purchases table.")

if __name__ == "__main__":
    ratings_path = os.path.join(
        os.path.dirname(__file__),
        'data', 'movielens', 'ratings.dat'
    )
    seed_movielens_ratings(ratings_path)

