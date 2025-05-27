import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/amc_chatbot')
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
    SCRAPE_INTERVAL = int(os.getenv('SCRAPE_INTERVAL', 3600))  # 1 hour
    MAX_CACHE_AGE = int(os.getenv('MAX_CACHE_AGE', 86400))  # 24 hours