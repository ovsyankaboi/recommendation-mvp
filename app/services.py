from collections import Counter
from .crud import list_purchases, create_recommendation

def generate_recommendations(db, user_id: str, top_n: int = 5):
    purchases = list_purchases(db, user_id)
    counts = Counter([p.product_id for p in purchases])
    top = counts.most_common(top_n)
    items = [
        {"product_id": pid, "score": qty, "rank": idx + 1}
        for idx, (pid, qty) in enumerate(top)
    ]
    return create_recommendation(db, user_id, items)
