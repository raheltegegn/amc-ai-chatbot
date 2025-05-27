from app import app
from flask import request, jsonify
from .ai_engine import generate_response
from .scraper import scrape_amc_data
from .database import cache_response, get_cached_response

@app.route('/api/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')
    language = data.get('language', 'am')
    
    # Check cache first
    cached = get_cached_response(question, language)
    if cached:
        return jsonify(cached)
    
    # Your existing implementation continues here...
    # ...
    # Scrape fresh data if not in cache
    scraped_data = scrape_amc_data()
    
    # Generate AI response
    response = generate_response(question, scraped_data, language)
    
    # Cache the response
    cache_response(question, response, language)
    
    return jsonify({
        'question': question,
        'answer': response,
        'language': language,
        'source': 'AMC'
    })

@app.route('/api/search', methods=['POST'])
def search_content():
    data = request.get_json()
    query = data.get('query')
    language = data.get('language', 'am')
    
    scraped_data = scrape_amc_data()
    results = []
    
    # Simple search implementation (can be enhanced)
    for item in scraped_data:
        if query.lower() in item['title'].lower() or query.lower() in item['content'].lower():
            results.append({
                'title': item['title'],
                'summary': item['content'][:150] + '...',
                'url': item['url']
            })
    
    return jsonify({
        'query': query,
        'results': results[:5],  # Limit to 5 results
        'language': language
    })