#!/usr/bin/env python3

import socket
import arguments
import argparse

# Run 'python3 client.py --help' to see what these lines do
parser = argparse.ArgumentParser('Send a message to a server at the given address and print the response')
parser.add_argument('--server_IP', help='IP address at which the server is hosted', **arguments.ip_addr_arg)
parser.add_argument('--server_port', help='Port number at which the server is hosted', **arguments.server_port_arg)
parser.add_argument('--VPN_IP', help='IP address at which the VPN is hosted', **arguments.ip_addr_arg)
parser.add_argument('--VPN_port', help='Port number at which the VPN is hosted', **arguments.vpn_port_arg)
parser.add_argument('--message', default=['Hello, world'], nargs='+', help='The message to send to the server', metavar='MESSAGE')
args = parser.parse_args()

SERVER_IP = args.server_IP  # The server's IP address
SERVER_PORT = args.server_port  # The port used by the server
VPN_IP = args.VPN_IP  # The server's IP address
VPN_PORT = args.VPN_port  # The port used by the server
order_message = ' '.join(args.message) # The message to send to the server

## --------------------------------- from the project 1 ----------------------------
#introduction, connection confirmation
print("Welcome to Tomoko's Really Pretty Cool (RPC) Ice Cream Stand!\n")
print("Customer identified! - Connecting you to cashier", VPN_IP, "and port...", VPN_PORT)

#initalizing arguments/parameters for operations
#these arguments will be updated with user input
order_type = ""
size = ""
flavor = ""
syrup = ""
milk = ""
cookie = ""

# New prompt for pickup or delivery
service_type = ""
while service_type not in ["PICKUP", "DELIVER"]:
    service_type = input("Would you like your order for pickup or delivery? (PICKUP/DELIVER)\n")
    if service_type not in ["PICKUP", "DELIVER"]:
        print("I didn't quite catch that! Please choose either PICKUP or DELIVER.")

#order type is updated first, and handles misspelling or empty inputs
while order_type not in ["scoop", "milkshake", "chipwich"]:
    order_type = input("Would you like a scoop, milkshake, or chipwich?\n")   
    if order_type not in ["scoop", "milkshake", "chipwich"]:
        print("I didn't quite catch that! Please choose either scoop, milkshake, or chipwich: ")

    #arguments for scoop order type are updated and include size, flavor, and choice of syrup
    #error handling implemented with if statements!
    if order_type == "scoop":
        while size not in ["small", "medium", "large"]:
            size = input("Specify the cup size: small, medium, large: \n")
            if size not in ["small", "medium", "large"]:
                print("I didn't quite catch that! Please choose either small, medium, or large: \n" )
        
        while flavor not in ["strawberry", "chocolate", "vanilla"]:
            flavor = input("Specify a flavor: strawberry, chocolate, vanilla: \n")
            if flavor not in ["strawberry", "chocolate", "vanilla"]:
                print("I didn't quite catch that! Please choose either strawberry, chocolate, vanilla: \n")

        while syrup not in ["no syrup", "chocolate syrup", "cherry syrup"]:
            syrup = input("Choose a syrup: no syrup, chocolate syrup, or cherry syrup: \n")
            if syrup not in ["no syrup", "chocolate syrup", "cherry syrup"]:
                print("I didn't quite catch that! Please choose either no syrup, chocolate syrup, or cherry syrup: \n")

    #arguments for milkshake order type are updated and include flavor, milk type, and choice of syrup
    #error handling implemented with if statements!
    elif order_type == "milkshake":
        while flavor not in ["strawberry", "chocolate", "vanilla"]:
            flavor = input("Specify a flavor: strawberry, chocolate, vanilla: \n")
            if flavor not in ["strawberry", "chocolate", "vanilla"]:
                print("I didn't quite catch that! Please choose either strawberry, chocolate, vanilla: \n")
        
        while milk not in ["dairy milk", "oat milk", "almond milk", "soy milk"]:
            milk = input("Choose your milk or alternative: dairy milk, oat milk, almond milk, or soy milk: \n")
            if milk not in ["dairy milk", "oat milk", "almond milk", "soy milk"]:
                print("I didn't quite catch that! Please choose either dairy milk, oat milk, almond milk, or soy milk: \n")
        
        while syrup not in ["no syrup", "chocolate syrup", "cherry syrup"]:
            syrup = input("Choose a syrup: no syrup, chocolate syrup, or cherry syrup: \n")
            if syrup not in ["no syrup", "chocolate syrup", "cherry syrup"]:
                print("I didn't quite catch that! Please choose either no syrup, chocolate syrup, or cherry syrup: \n")

    #arguments for chipwich order type are updated and include flavor and choice of cookie
    #error handling implemented with if statements!
    elif order_type == "chipwich":
        while flavor not in ["strawberry", "chocolate", "vanilla"]:
            flavor = input("Specify a flavor: strawberry, chocolate, vanilla: \n")
            if flavor not in ["strawberry", "chocolate", "vanilla"]:
                print("I didn't quite catch that! Please choose either strawberry, chocolate, vanilla: \n")
        
        while cookie not in ["chocolate chip", "oatmeal raisin", "ginger bread"]:
            cookie = input("Choose the cookies for your ice cream sandwich: chocolate chip, oatmeal raisin, ginger bread: \n")
            if cookie not in ["chocolate chip", "oatmeal raisin", "ginger bread"]:
                print("I didn't quite catch that! Please choose either chocolate chip, oatmeal raisin, or ginger bread: \n")

#order_message created based on order type
if order_type == "scoop":
    order_message = f"{service_type},{order_type},{size},{flavor},{syrup}"
elif order_type == "milkshake":
    order_message = f"{service_type},{order_type},{flavor},{milk},{syrup}"
elif order_type == "chipwich":
    order_message = f"{service_type},{order_type},{flavor},{cookie}"

## -------------------------------- from project 1 -------------------------------------
def encode_message(message):
    # message is not empty
    if not message:
        raise ValueError("Message unclear!")
    # Split the user input into verb and order
    message_parts = message.split(' ',1)
    if len(message_parts) < 2:
        raise ValueError("Message must contain both delivery option and order.")
    
    delivery_option, order = message_parts

    # Add an application-layer header to the message that the VPN can use to forward it
    header = f"{delivery_option}".encode('utf-8')
    
    # format the full message with the server IP and port
    full_message = f"{SERVER_IP}, {SERVER_PORT}, {header.decode('utf-8')}, {order}"
    return full_message.encode('utf-8')

try:
    print("client starting - connecting to cashier at IP", VPN_IP, "and port", VPN_PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((VPN_IP, VPN_PORT))
        print(f"connection established, sending message '{order_message}'")
        
        # Send the order message to VPN
        s.sendall(encode_message(order_message))
        print("Ice cream order sent, thank you for your patience!\n")

        # Wait for the response from the VPN
        # This is where the client needs to stay open until it receives the response from VPN
        response = s.recv(1024).decode('utf-8')
        print(f"Order up! Response received from the kitchen to the cashier to you. Your order is ready: '{response}'")
        print("Your order was fulfilled. Time for a Lactaid?\n")

## ------ from project 1 ---------
except ConnectionRefusedError:
    print("It looks there's no one to take your order... See if the shop is actually open.")
    exit(1)
except Exception as e:
    print(f"Something is wrong with the shop's system... come back later and try ordering again! The sign on the door says: {e}")
    exit(1)
## ------- from project 1 ----------

#message recieved from the server
#closing upon recieving the message from server