from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from typing import Optional
from bson import ObjectId
import json
from urllib.parse import parse_qs

app = FastAPI()

connectionstring = "mongodb+srv://hkkwak:<passwd>@cluster0.ocmnn3x.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# MongoDB 클라이언트 설정
client = MongoClient(connectionstring)
db = client.test
collection = db.maplekh_mongodb

def str_to_objectid(str_id):
    try:
        return ObjectId(str_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

@app.get("/create/")
async def create_item(index: int, text: str, description: Optional[str] = None):
    items = json.loads(text)
    items["index"] = index
    result = collection.insert_one(items)
    return {"_id": str(result.inserted_id)}

@app.get("/read/{item_id}")
async def read_item(item_id: str):
    object_id = str_to_objectid(item_id)
    item = collection.find_one({"_id": object_id})
    if item:
        item["_id"] = str(item["_id"])
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/update/{item_id}")
async def update_item(item_id: str, index: int, text: str, description: Optional[str] = None):
    object_id = str_to_objectid(item_id)
    items = json.loads(text)
    items["index"] = index
    result = collection.update_one({"_id": object_id}, {"$set": items})
    if result.matched_count:
        return {"msg": "Item updated"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/delete/{item_id}")
async def delete_item(item_id: str):
    object_id = str_to_objectid(item_id)
    result = collection.delete_one({"_id": object_id})
    if result.deleted_count:
        return {"msg": "Item deleted"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
