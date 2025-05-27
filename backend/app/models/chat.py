from pymongo import MongoClient
import os
from datetime import datetime

def get_db():
    """Get MongoDB connection with fallback to default local connection"""
    try:
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/amc_chatbot')
        client = MongoClient(mongodb_uri)
        return client.amc_chatbot
    except Exception as e:
        print(f"MongoDB connection error: {str(e)}")
        return None

def save_chat_history(question, answer, language):
    """Save chat interaction to MongoDB"""
    db = get_db()
    if not db:
        print("Warning: MongoDB not available, skipping chat history save")
        return False
    
    chat_record = {
        'question': question,
        'answer': answer,
        'language': language,
        'timestamp': datetime.utcnow()
    }
    
    try:
        db.chat_history.insert_one(chat_record)
        return True
    except Exception as e:
        print(f"Error saving chat history: {str(e)}")
        return False

def get_chat_history(limit=10):
    """Retrieve recent chat history"""
    db = get_db()
    if not db:
        print("Warning: MongoDB not available, returning empty history")
        return []
    
    try:
        history = list(db.chat_history.find(
            {},
            {'_id': 0}
        ).sort('timestamp', -1).limit(limit))
        return history
    except Exception as e:
        print(f"Error retrieving chat history: {str(e)}")
        return [] 