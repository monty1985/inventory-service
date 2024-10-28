from fastapi import FastAPI, HTTPException
from redis import Redis
from pymongo import MongoClient
from fastapi.responses import JSONResponse
import json

# Initialize FastAPI
app = FastAPI()

# Redis and MongoDB connections
redis_client = Redis(host="redis", port=6379, decode_responses=True)
mongo_client = MongoClient("mongodb://mongodb:27017/")
db = mongo_client.inventoryDB
inventory_collection = db.inventory

def cache_item(item_id, item_data):
    """Cache the item in Redis with a timeout of 30 sec (30 seconds)."""
    # Convert ObjectId to string if present
    if "_id" in item_data:
        item_data["_id"] = str(item_data["_id"])

    redis_client.setex(f"item:{item_id}", 30, json.dumps(item_data))


def get_cached_item(item_id):
    """Retrieve the item from Redis if it exists."""
    cached_item = redis_client.get(f"item:{item_id}")
    if cached_item:
        return json.loads(cached_item)
    return None

@app.post("/items/")
def add_item(item: dict):
    """Add a new item to the inventory and cache it."""
    if inventory_collection.find_one({"item_id": item["item_id"]}):
        raise HTTPException(status_code=400, detail=f"Item with id {item['item_id']} already exists")

    # Insert item into MongoDB
    new_item = inventory_collection.insert_one(item)

    # Cache the item in Redis
    cache_item(item["item_id"], item)

    return {"message": "Item added successfully", "item": item}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    """Fetch an item from Redis cache or MongoDB."""
    # Try to get the item from Redis cache
    cached_item = get_cached_item(item_id)
    if cached_item:
        return {"source": "redis", "item": cached_item}

    # If not found in Redis, fetch from MongoDB
    item = inventory_collection.find_one({"item_id": item_id})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Convert MongoDB ObjectId to string and cache it in Redis
    item["_id"] = str(item["_id"])
    cache_item(item_id, item)

    return {"source": "mongodb", "item": item}
