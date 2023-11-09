import json
import os
from pprint import pprint

import requests


def get_news(country: str):
    response = requests.get(
        f"https://newsapi.org/v2/top-headlines?country={country}&category=technology&apiKey={os.getenv('NEWS_API_KEY')}"
    )
    news = json.loads(response.content)
    filtered_articles = [article for article in news["articles"] if not any(keyword.lower() in article["title"].lower() for keyword in ["amazon", "flipkart"])]
    return filtered_articles[:10]


[pprint(news) for news in get_news('in')]
