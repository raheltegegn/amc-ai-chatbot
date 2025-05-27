from pymongo import MongoClient
from datetime import datetime, timedelta
import os
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

# MongoDB setup
client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'))
db = client.amc_chatbot
cache_collection = db.response_cache

def cache_response(question, response, language):
    cache_collection.insert_one({
        'question': question,
        'response': response,
        'language': language,
        'timestamp': datetime.now()
    })

def get_cached_response(question, language):
    # Check for cached responses in the last 24 hours
    one_day_ago = datetime.now() - timedelta(days=1)
    
    cached = cache_collection.find_one({
        'question': question,
        'language': language,
        'timestamp': {'$gte': one_day_ago}
    })
    
    if cached:
        return {
            'question': cached['question'],
            'answer': cached['response'],
            'language': cached['language'],
            'source': 'cache'
        }
    return None

class Database:
    def __init__(self, connection_string: str = "mongodb://localhost:27017/"):
        try:
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            # Test the connection
            self.client.server_info()
            self.db = self.client.amc_chatbot
            self.articles = self.db.articles
            # Create text index for better search
            self.articles.create_index([
                ("title", "text"),
                ("content", "text")
            ])
            # Create unique index on URL
            self.articles.create_index([("url", 1)], unique=True)
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

    def save_articles(self, articles: List[Dict[str, Any]]) -> None:
        """Save or update articles in MongoDB"""
        try:
            for article in articles:
                article['last_updated'] = datetime.now()
                self.articles.update_one(
                    {'url': article['url']},
                    {'$set': article},
                    upsert=True
                )
            logger.info(f"Successfully saved/updated {len(articles)} articles")
        except Exception as e:
            logger.error(f"Error saving articles to MongoDB: {str(e)}")
            raise

    def get_articles(self, query: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve articles from MongoDB with optional text search"""
        try:
            if query:
                # Use text search if available, fallback to regex
                try:
                    cursor = self.articles.find(
                        {"$text": {"$search": query}},
                        {"score": {"$meta": "textScore"}}
                    ).sort([("score", {"$meta": "textScore"})]).limit(limit)
                    results = list(cursor)
                    if not results:
                        # Fallback to regex search
                        cursor = self.articles.find(
                            {
                                '$or': [
                                    {'title': {'$regex': query, '$options': 'i'}},
                                    {'content': {'$regex': query, '$options': 'i'}}
                                ]
                            }
                        ).sort('last_updated', -1).limit(limit)
                        results = list(cursor)
                    return results
                except Exception as e:
                    logger.error(f"Error using text search: {str(e)}")
                    raise
            else:
                cursor = self.articles.find().sort('last_updated', -1).limit(limit)
                return list(cursor)
        except Exception as e:
            logger.error(f"Error retrieving articles from MongoDB: {str(e)}")
            raise

    def get_article_by_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific article by URL"""
        try:
            return self.articles.find_one({'url': url})
        except Exception as e:
            logger.error(f"Error retrieving article by URL: {str(e)}")
            raise