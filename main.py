# Author: Raymond Randall
# Date: November 14, 2022
# Description: A microservice that retreives one positive and one negative headline about the received stock ticket symbol.
# API (update auth.py with API key): https://api.marketaux.com/

import requests
import zmq
import json
from urllib import parse
import urllib
import auth

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
print('Now listening on port 5555...')

def process_data(json_data):
    max_sentiment = None
    max_title = None
    max_url = None
    min_sentiment = None
    min_title = None
    min_url = None

    for headline in json_data['data']:
        headline_sentiment = headline['entities'][0]['sentiment_score']
        if not headline_sentiment:
            headline_sentiment=0  # if sentiment score is missing, assign a 0.
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

    return json.dumps({
        'highest': {
                'sentiment': max_sentiment
                , 'title': max_title
                , 'url': max_url
        }, 'lowest': {
            'sentiment': min_sentiment
            , 'title': min_title
            , 'url': min_url
            }
        })


while True:
    #  Wait for next ticker request from client
    params = urllib.parse.urlencode({
        'api_token': auth.API_KEY,
        'symbols': socket.recv_string(),
        'limit': 3,
    })

    # Get the ticker news from the API
    try:
        api_url = f'https://api.marketaux.com/v1/news/all?{params}'
    except Exception as e:
        print(f'There was an error during the request: {e}')
    res = requests.get(api_url)
    msg = res.json()

    # Process the data
    msg_processed = process_data(msg)

    #  Send data back to client
    socket.send_string(json.dumps(msg_processed))


