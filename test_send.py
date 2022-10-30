import zmq
import json

context = zmq.Context()

#  Socket to talk to server
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Request news for this symbol
symbol = "MSFT"
print(f"Sending request: {symbol} …")
socket.send_string(symbol)

#  Get the data.
message = json.loads(socket.recv())
print(f"Received reply [ {message} ]")