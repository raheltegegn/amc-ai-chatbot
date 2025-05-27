from flask import Blueprint, request, jsonify, current_app
import logging
import traceback
from .utils.scraper import get_amc_content
from .utils.institution_info import is_institutional_query, get_query_type, get_amc_info

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main.route('/api/ask', methods=['POST'])
def ask():
    try:
        # Log request details
        logger.debug(f"Request headers: {dict(request.headers)}")
        logger.debug(f"Request data: {request.get_data()}")
        
        data = request.get_json()
        logger.debug(f"Parsed JSON data: {data}")
        
        if not data or not isinstance(data, dict):
            return jsonify({
                'status': 'error',
                'message': 'Invalid request format'
            }), 400

        if 'message' not in data:
            return jsonify({
                'status': 'error',
                'message': 'No message provided'
            }), 400

        user_message = data['message']
        language = data.get('language', 'am')
        
        if not user_message or not isinstance(user_message, str):
            return jsonify({
                'status': 'error',
                'message': 'Invalid message format'
            }), 400

        logger.info(f"Processing question: {user_message}")

        # Check if this is an institutional query
        if is_institutional_query(user_message):
            query_type = get_query_type(user_message)
            info = get_amc_info(query_type, language)
            return jsonify({
                'status': 'success',
                'context': [],
                'source': 'AMC Info',
                'message': info,
                'is_institutional': True,
                'total_results': 0
            })

        # Try to get articles from MongoDB if available
        articles = []
        if current_app.db:
            try:
                # Get both Amharic and English articles
                articles = current_app.db.get_articles(query=user_message, limit=5)
                logger.info(f"Found {len(articles)} articles in database")
            except Exception as e:
                logger.warning(f"Error retrieving articles from MongoDB: {str(e)}")
                logger.debug(traceback.format_exc())

        # If no articles found in DB or DB not available, try scraping
        if not articles:
            logger.info("Attempting to scrape new content...")
            try:
                # Get both Amharic and English articles
                articles = get_amc_content(user_message, include_english=True)
                if not articles:
                    logger.warning("No articles found from scraping")
                else:
                    logger.info(f"Scraped {len(articles)} new articles")
                    logger.debug(f"Scraped articles: {articles}")
                
                # Try to save to MongoDB if available
                if current_app.db and articles:
                    try:
                        current_app.db.save_articles(articles)
                        logger.info("Saved new articles to database")
                    except Exception as e:
                        logger.warning(f"Could not save articles to MongoDB: {str(e)}")
                        logger.debug(traceback.format_exc())
            except Exception as e:
                logger.error(f"Error scraping content: {str(e)}")
                logger.debug(traceback.format_exc())
                # Don't return error here, continue with empty articles list

        # Format response
        context = []
        if articles:
            for article in articles:
                if not isinstance(article, dict):
                    logger.warning(f"Skipping invalid article format: {type(article)}")
                    continue
                
                # Clean and validate the article data
                title = str(article.get('title', '')).strip()
                url = str(article.get('url', '')).strip()
                date = str(article.get('date', '')).strip()
                lang = str(article.get('language', 'am')).strip().lower()
                
                if not title or not url:
                    logger.warning(f"Skipping article with missing title or URL")
                    continue
                
                context.append({
                    'title': title,
                    'url': url,
                    'date': date,
                    'language': lang
                })

        # Sort articles by date (newest first) and group by language
        context.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        # Return a valid response even if no articles found
        response = {
            'status': 'success',
            'context': context if context else [],
            'source': 'AMC News',
            'message': 'No relevant content found' if not context else 'Content retrieved successfully',
            'is_institutional': False,
            'total_results': len(context)
        }

        logger.info("Successfully processed request")
        logger.debug(f"Response: {response}")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        logger.debug(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@main.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        status = {
            'status': 'healthy',
            'mongodb': 'connected' if current_app.db else 'not available',
            'scraper': 'initialized' if current_app.scraper else 'not initialized',
            'version': '1.0.0'
        }
        return jsonify(status)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        logger.debug(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': 'Health check failed'
        }), 500 