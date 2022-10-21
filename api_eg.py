import requests
import json

API_TOKEN = 'tFCbPxXlTl9xISy2MIY34o080M5xlqOftj9iPjdQ'

symbol = 'AMZN'

api_url = f'https://api.marketaux.com/v1/news/all?symbols={symbol}&filter_entities=true&language=en&api_token={API_TOKEN}'


def process_data(json_data):
    max_sentiment = None
    max_title = None
    max_url = None
    min_sentiment = None
    min_title = None
    min_url = None

    for headline in json_data['data']:
        headline_sentiment = headline['entities'][0]['sentiment_score']
        if max_sentiment is None:
            max_sentiment = headline_sentiment
            max_title = headline['title']
            max_url = headline['url']
        if min_sentiment is None:
            min_sentiment = headline_sentiment
            min_title = headline['title']
            min_url = headline['url']
        if headline_sentiment > max_sentiment:
            max_sentiment = headline_sentiment
            max_title = headline['title']
            max_url = headline['url']
        if headline_sentiment < min_sentiment:
            min_sentiment = headline_sentiment
            min_title = headline['title']
            min_url = headline['url']

    return json.dumps({'data' :
        {'highest': {
            'sentiment': max_sentiment
            , 'title': max_title
            , 'url': max_url
            }
        }, 'lowest': {
            'sentiment': min_sentiment
            , 'title': min_title
            , 'url': min_url
            }
        }, indent = 4)

res = requests.get(api_url)
msg = res.json()

print(process_data(msg))


