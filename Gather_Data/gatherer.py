# User Data Gatherer
from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["IEEECS-bot"]


class Chat(BaseModel):
    user: str
    chat: str
    timestamp: datetime


async def store_chat(chat: Chat, server:str):
    collection = db[f"{server}"]
    try:
        collection.insert_one(chat.dict())
    except Exception:
        pass
