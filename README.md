# cs361_stock_news_microservice
A zeromq microservice that responds to a stock ticker msg with highest sentiment news and lowest sentiment news.

To run the microservice:
- Run the main.py file locally.

To request data from this microservice:
- Ensure you are connecting to the correct tcp address and port. 
- Send a valid stock ticker symbol (e.g. AMZN, MSFT, NFLX) as a string.


Example call to the microservice:

import zmq
import json

context = zmq.Context()

#  Socket to talk to server
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response

symbol = "MSFT"
print(f"Sending request: {symbol} …")
socket.send_string(symbol)

#  Get the reply.
message = json.loads(socket.recv())
print(f"Received reply [ {message} ]")


Data is returned from the microservice in the following json format:

{
    "data": {
        "highest": {
            "sentiment": 0.112267,
            "title": "My Current Favorite Stocks To Buy",
            "url": "https://seekingalpha.com/article/4550807-my-current-favorite-stocks-to-buy"
        }
    },
    "lowest": {
        "sentiment": -0.0423,
        "title": "Why Q3s GDP Print Doesn't Mean Recession Avoidance",
        "url": "https://www.forbes.com/sites/greatspeculations/2022/10/29/why-q3s-gdp-print-doesnt-mean-recession-avoidance/"
    }
}

![image](https://user-images.githubusercontent.com/12983146/198868706-8a858ee4-aff8-4687-8fa9-2fb5b8d93170.png)

