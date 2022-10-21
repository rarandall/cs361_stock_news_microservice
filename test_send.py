import zmq
import json

context = zmq.Context()

#  Socket to talk to server
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response
for request in range(1):
    symbol = "AMZN"
    print(f"Sending request {request}: {symbol} …")
    socket.send_string(symbol)

    #  Get the reply.
    message = json.loads(socket.recv())
    print(f"Received reply {request} [ {message} ]")