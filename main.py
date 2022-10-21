import requests
import time
import zmq
import json
from urllib import parse
import urllib

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


params = urllib.parse.urlencode({
    'api_token': 'tFCbPxXlTl9xISy2MIY34o080M5xlqOftj9iPjdQ',
    'symbols': socket.recv_string(),
    'limit': 3,
    })


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

    return json.dumps({'data':
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
        }, indent=4)


while True:
    #  Wait for next request from client
    api_url = f'https://api.marketaux.com/v1/news/all?{params}'
    res = requests.get(api_url)
    msg = res.json()

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    msg_processed = process_data(msg)
    socket.send_string(json.dumps(msg_processed))


