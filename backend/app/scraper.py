import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def scrape_amc_data():
    # Example implementation - needs to be adapted to AMC's actual website structure
    base_url = "https://www.ameco.et/"
    news_url = f"{base_url}/news"
    
    try:
        response = requests.get(news_url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        
        # Example scraping logic - needs customization
        news_items = soup.find_all('div', class_='news-item')
        
        for item in news_items[:10]:  # Limit to 10 news items
            title = item.find('h3').text.strip()
            link = item.find('a')['href']
            if not link.startswith('http'):
                link = base_url + link
                
            # Get article details
            article_response = requests.get(link)
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            content = article_soup.find('div', class_='article-content').text.strip()
            date_str = article_soup.find('span', class_='date').text.strip()
            
            articles.append({
                'title': title,
                'url': link,
                'content': content,
                'date': date_str,
                'type': 'news'
            })
        
        return articles
    
    except Exception as e:
        print(f"Scraping error: {e}")
        return []