import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AMCScraper:
    def __init__(self):
        self.base_url = "https://ameco.et"  # Base URL without trailing slash
        self.cache_file = 'data/amc_cache.json'
        self.cache_duration = timedelta(hours=1)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _load_cache(self):
        """Load cached content"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                    if datetime.fromisoformat(cache['timestamp']) + self.cache_duration > datetime.now():
                        logger.info("Using cached content")
                        return cache['data']
        except Exception as e:
            logger.error(f"Cache loading error: {str(e)}")
        return None
    
    def _save_cache(self, data):
        """Save content to cache"""
        try:
            os.makedirs('data', exist_ok=True)
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'data': data
                }, f, ensure_ascii=False)
            logger.info("Content cached successfully")
        except Exception as e:
            logger.error(f"Cache saving error: {str(e)}")
    
    def _get_page_content(self, url):
        """Get page content with retries"""
        if not url:
            logger.error("Invalid URL: URL is None or empty")
            return None
            
        if not url.startswith('http'):
            url = f"{self.base_url}/{'news' if 'news' in url else ''}"
            
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempting to fetch URL: {url}")
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response.text
            except Exception as e:
                logger.error(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise
        return None

    def get_news_content(self):
        """Scrape news content from AMC website"""
        cached = self._load_cache()
        if cached:
            return cached
        
        news_items = []
        try:
            logger.info(f"Fetching content from {self.base_url}")
            html_content = self._get_page_content(self.base_url)
            if not html_content:
                raise Exception("Failed to fetch main page")
            
            soup = BeautifulSoup(html_content, 'html.parser')
            logger.info("Successfully parsed main page")
            
            # Try to find news sections
            sections = []
            
            # Method 1: Look for news sections by heading
            for heading in ['አማራ', 'ኢትዮጵያ', 'አፍሪካ', 'ዓለም', 'ዜና']:
                section = soup.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'], string=lambda x: x and heading in x)
                if section:
                    sections.append(section.parent)
            
            # Method 2: Look for article containers
            article_containers = soup.find_all(['article', 'div'], class_=lambda x: x and any(term in str(x).lower() for term in ['post', 'article', 'news']))
            sections.extend(article_containers)
            
            logger.info(f"Found {len(sections)} potential news sections")
            
            # Process each section
            for section in sections:
                try:
                    # Find all links in this section
                    links = section.find_all('a')
                    for link in links:
                        try:
                            url = link.get('href', '')
                            if not url:
                                continue
                                
                            if not url.startswith('http'):
                                url = f"{self.base_url}{url if url.startswith('/') else '/' + url}"
                            
                            # Skip if we already processed this URL
                            if any(item['url'] == url for item in news_items):
                                continue
                            
                            logger.info(f"Processing URL: {url}")
                            
                            # Get article content
                            article_html = self._get_page_content(url)
                            if not article_html:
                                continue
                                
                            article_soup = BeautifulSoup(article_html, 'html.parser')
                            
                            # Get title
                            title = None
                            title_elem = article_soup.find(['h1', 'h2', 'h3'], class_=lambda x: x and any(term in str(x).lower() for term in ['title', 'heading']))
                            if title_elem:
                                title = title_elem.text.strip()
                            else:
                                title = link.text.strip()
                            
                            if not title:
                                continue
                            
                            # Get content
                            content = ''
                            content_elem = article_soup.find(['div', 'article'], class_=lambda x: x and any(term in str(x).lower() for term in ['content', 'body', 'text']))
                            if content_elem:
                                # Remove unwanted elements
                                for unwanted in content_elem.find_all(['script', 'style', 'iframe', 'nav', 'header', 'footer']):
                                    unwanted.decompose()
                                content = content_elem.text.strip()
                            
                            # Get date
                            date = ''
                            date_elem = article_soup.find(['time', 'span'], class_=lambda x: x and any(term in str(x).lower() for term in ['date', 'time', 'meta']))
                            if date_elem:
                                date = date_elem.text.strip()
                            
                            # Get category
                            category = 'News'
                            category_elem = article_soup.find(['span', 'a'], class_=lambda x: x and 'category' in str(x).lower())
                            if category_elem:
                                category = category_elem.text.strip()
                            
                            news_items.append({
                                'title': title,
                                'content': content,
                                'date': date,
                                'url': url,
                                'category': category
                            })
                            logger.info(f"Added article: {title}")
                            
                        except Exception as e:
                            logger.error(f"Error processing link: {str(e)}")
                            continue
                            
                except Exception as e:
                    logger.error(f"Error processing section: {str(e)}")
                    continue
            
            if news_items:
                self._save_cache(news_items)
                logger.info(f"Successfully processed {len(news_items)} articles")
            else:
                logger.warning("No news items found")
            
            return news_items
            
        except Exception as e:
            logger.error(f"Error scraping AMC website: {str(e)}")
            cached = self._load_cache()
            return cached if cached else []

def get_amc_content(query, include_english=False):
    """Get relevant AMC content based on the query"""
    logger = logging.getLogger(__name__)
    
    if not query or not isinstance(query, str):
        logger.error("Invalid query")
        return []
    
    try:
        scraper = AMCScraper()
        news_items = scraper.get_news_content()
        
        if not news_items:
            logger.warning("No news items available")
            return []
        
        # Prepare query terms (both Amharic and English)
        query_terms = query.lower().split()
        
        # Score and filter articles
        scored_items = []
        for item in news_items:
            try:
                if not item or not isinstance(item, dict):
                    continue
                
                title = str(item.get('title', '')).lower()
                content = str(item.get('content', '')).lower()
                url = str(item.get('url', ''))
                
                if not title or not url:
                    continue
                
                # Calculate relevance score
                score = 0
                exact_match = False
                
                # Check for exact matches in title
                if query.lower() in title:
                    score += 10
                    exact_match = True
                
                # Check for partial matches in title
                for term in query_terms:
                    if term in title:
                        score += 5
                    if term in content:
                        score += 2
                
                # Determine language
                is_english = any(c.isascii() for c in title)
                
                # Include article if:
                # 1. It has a non-zero score (relevant to query)
                # 2. It's an exact match
                # 3. It matches the language preference
                if score > 0 or exact_match:
                    if include_english or not is_english:
                        scored_items.append({
                            'item': {
                                'title': item['title'],
                                'url': url,
                                'date': item.get('date', ''),
                                'category': item.get('category', ''),
                                'language': 'en' if is_english else 'am'
                            },
                            'score': score,
                            'exact_match': exact_match
                        })
            except Exception as e:
                logger.error(f"Error processing item: {str(e)}")
                continue
        
        # Sort by exact match first, then by score
        scored_items.sort(key=lambda x: (not x['exact_match'], -x['score']))
        
        # Return top 10 most relevant items
        relevant_items = [item['item'] for item in scored_items[:10]]
        
        logger.info(f"Found {len(relevant_items)} relevant items")
        return relevant_items
        
    except Exception as e:
        logger.error(f"Error in get_amc_content: {str(e)}", exc_info=True)
        return [] 