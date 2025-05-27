import logging
from app.utils.scraper import AMCScraper
import json
import sys

def test_scraper():
    try:
        logger = logging.getLogger(__name__)
        logger.info("Starting AMC Scraper test...")
        
        scraper = AMCScraper()
        logger.info("Initialized scraper")
        
        logger.info("Attempting to fetch news content...")
        news_items = scraper.get_news_content()
        
        if news_items:
            logger.info(f"Successfully fetched {len(news_items)} news items")
            logger.info("\nSample items:")
            for i, item in enumerate(news_items[:3], 1):
                logger.info(f"\n{i}. Category: {item['category']}")
                logger.info(f"   Title: {item['title']}")
                logger.info(f"   Date: {item['date']}")
                logger.info(f"   URL: {item['url']}")
                logger.info(f"   Content length: {len(item['content'])} characters")
                logger.info(f"   First 200 chars of content: {item['content'][:200]}...")
        else:
            logger.warning("No news items found!")
            
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    test_scraper() 