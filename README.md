# cs361_stock_news_microservice
A zeromq microservice that responds to a stock ticker msg with highest sentiment news and lowest sentiment news.

To run the microservice:
- Request an API Key from the external API provider from https://www.marketaux.com/
- Update the auth.py file with your API key
- Install the required packages (pip install pyzmq==24.0.1, pip install requests)
- Run the main.py file locally.

To request data from this microservice:
- Ensure you are connecting to the correct tcp address and port. 
- Send a valid stock ticker symbol (e.g. AMZN, MSFT, NFLX) as a string.

To receive data from this microservice:
- Data will be received in JSON format (see example below), so use the appropriate package to load the json data.


## Example call to the microservice:

import zmq
import json

context = zmq.Context()

###  Socket to talk to server

print("Connecting to server…")

socket = context.socket(zmq.REQ)

socket.connect("tcp://localhost:5555")

### Request news for this symbol
symbol = "MSFT"

print(f"Sending request: {symbol} …")

socket.send_string(symbol)

###  Get the data.
message = json.loads(socket.recv())

print(f"Received reply [ {message} ]")


### Data is returned from the microservice in the following json format:

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

## UML sequence diagram
![image](https://user-images.githubusercontent.com/12983146/198868935-a22d832e-2c35-4321-b260-15ee389dcb6f.png)

