# Message Format

## Overview of Application
The client, VPN, and server all take command line arguments, and the client message is constructed through a series of inputs prompted by questions about an ice cream order. The client sends an order message to the VPN server, which the VPN then forwards to the echo-server, and waits for a response. The echo-server sends the response to the VPN server and the VPN server forwards this response back to the client. 

## Client -> VPN Server Message Format
The client constructs and sends a message to the VPN server that contains both order details and routing information, in the following format: <SERVER_IP>, <SERVER_PORT>, <DELIVERY_OPTION>, <ORDER>. The server IP and port number indicates to the VPN where the order should be forwarded, and the delivery option indicates whether the order is for pickup or delivery, which will be processed by the server to construct the response. The order is a comma separated list representing the specific ice cream order, and is also processed by the server to construct the response.

## VPN Server -> Client Message Format

The VPN server sends a response back to the client once it recieves a response from the server which is formatted as a string response, containing the order fulfillment message.

## Example Output

### Client Output
Welcome to Tomoko's Really Pretty Cool (RPC) Ice Cream Stand!

Customer identified! - Connecting you to cashier 127.0.0.1 and port... 55554
Would you like your order for pickup or delivery? (PICKUP/DELIVER)
PICKUP
Would you like a scoop, milkshake, or chipwich?
scoop
Specify the cup size: small, medium, large: 
small
Specify a flavor: strawberry, chocolate, vanilla: 
vanilla
Choose a syrup: no syrup, chocolate syrup, or cherry syrup: 
no syrup
client starting - connecting to cashier at IP 127.0.0.1 and port 55554
connection established, sending message 'PICKUP,scoop,small,vanilla,no syrup'
Ice cream order sent, thank you for your patience!

Order up! Response received from the kitchen to the cashier to you. Your order is ready: 'Here is your small vanilla scoop with no syrup for PICKUP!'
Your order was fulfilled. Time for a Lactaid?

### VPN Server Output
VPN starting - opening up cashier station at 127.0.0.1 with our cool tip jar and communication with the kitchen 55554
Waiting for customers... 

Successfully connected to customer: We are open to orders!

Destination IP and Port identified from header: '127.0.0.1','65432'

Received client order: '127.0.0.1, 65432, PICKUP,scoop,small,vanilla,no, syrup' message length: [54 bytes]

Received client order: 'PICKUP,scoop,small,vanilla,no, syrup' Current bytes: [54 bytes]

Fulfilling order...

### Server Output
Server starting - opening up shop at 127.0.0.1 with our cool entryway door with model number 65432        
Connected established with ('127.0.0.1', 53161). Successfully opened shop: Kitchen is open to orders!

Received client order: 'PICKUP,scoop,small,vanilla,no, syrup' Current bytes: [36 bytes]

Order recieved: PICKUP,scoop,small,vanilla,no, syrup
Saying 'Here is your small vanilla scoop with no syrup for PICKUP!' to the to customer!

Really Pretty Cool kitchen has completed the order, Ice cream has been given to the cashier. Closing kitchen...

## A description of how the network layers are interacting when the Server, VPN, and Client are run
The client generates the order message and adds the destination IP address and port, and this encoded message traverses the Application layer, Transport Layer, Network  layer, and Link Layer to the VPN server through a TCP  connection that the client's transport layer established. The encoded message from the client is decoded by the VPN server to identify the destination IP and Port, and the encoded message will traverse the layer stack again to travel over a TCP connection between the VPN server and the server. The response process is the same is above, but in the opposite order.

## Acknowledgements
I did not collaborate with anyone on this assignment, but used online sources to review python syntax and specifically stack overflow to debug.