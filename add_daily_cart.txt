import json
import random
from datetime import datetime, timedelta

brands = ["Brand A", "Brand B", "Brand C", "Brand D", "Brand E"]
categories = ["Electronics", "Clothing", "Books", "Home", "Sports"]
payment_methods = ["Credit Card", "Debit Card", "PayPal", "UPI"]
payment_statuses = ["Paid", "Unpaid"]

def generate_order(order_num):
    price = round(random.uniform(1000, 50000), 2)
    quantity = random.randint(1, 5)
    discount_percentage = round(random.uniform(5, 25), 2)
    discounted_total = round(price * quantity * (1 - discount_percentage / 100), 2)
    shipping = round(random.uniform(50, 500), 2)
    tax = round(discounted_total * 0.12, 2)
    total = round(discounted_total + shipping + tax, 2)

    is_returned = random.choice([True, False])
    return_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d") if is_returned else None
    cart_refund_amount = discounted_total if is_returned else 0
    cart_refund_shipping = is_returned and random.choice([True, False])

    return {
        "order_id": f"ORD{order_num:04d}",
        "order_date": (datetime.now() - timedelta(days=random.randint(0, 60))).strftime("%Y-%m-%d"),
        "user_id": random.randint(1, 100),
        "payment_method": random.choice(payment_methods),
        "payment_status": random.choice(payment_statuses),
        "is_returned": is_returned,
        "cart_refund_amount": cart_refund_amount,
        "cart_refund_shipping": cart_refund_shipping,
        "return_date": return_date,
        "product_id": random.randint(1000, 9999),
        "product_title": f"Product {random.randint(1, 100)}",
        "brand": random.choice(brands),
        "category": random.choice(categories),
        "discount_percentage": discount_percentage,
        "discounted_total": discounted_total,
        "price": price,
        "quantity": quantity,
        "shipping": shipping,
        "tax": tax,
        "total": total
    }

def add_daily_order():
    try:
        with open('carts.json', 'r+') as f:
            data = json.load(f)
            new_order = generate_order(len(data['orders']) + 1)
            data['orders'].append(new_order)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
            print(f"✅ Added order #{new_order['order_id']}")
    except FileNotFoundError:
        with open('sales.json', 'w') as f:
            data = {"orders": [generate_order(1)]}
            json.dump(data, f, indent=2)
            print("✅ sales.json created with order #ORD0001")

if __name__ == '__main__':
    add_daily_order()

