from app.extensions import mongo
from bson import ObjectId

class MongoCart:
    @staticmethod
    def add_item(user_id, product_data):
        cart_item = {
            "user_id": user_id,
            "product_id": product_data["id"],
            "name": product_data["name"],
            "price": product_data["price"],
            "quantity": product_data.get("quantity", 1)
        }
        return mongo.db.cart_items.insert_one(cart_item)

    @staticmethod
    def get_user_cart(user_id):
        return list(mongo.db.cart_items.find({"user_id": user_id}))

    @staticmethod
    def update_quantity(item_id, quantity):
        return mongo.db.cart_items.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": {"quantity": quantity}}
        )

    @staticmethod
    def remove_item(item_id):
        return mongo.db.cart_items.delete_one({"_id": ObjectId(item_id)}) 