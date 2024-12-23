#!/usr/bin/env python3

# In the ice cream shop example, the VPN would be an intermediary between the customer
# ordering the order and the kitchen staff creating the order. The people making the order
# do not technically know who is ordering, so the cashier is kind of like the VPN!

import socket
import arguments
import argparse

# Run 'python3 VPN.py --help' to see what these lines do
parser = argparse.ArgumentParser('Send a message to a server at the given address and prints the response')
parser.add_argument('--VPN_IP', help='IP address at which to host the VPN', **arguments.ip_addr_arg)
parser.add_argument('--VPN_port', help='Port number at which to host the VPN', **arguments.vpn_port_arg)
args = parser.parse_args()

VPN_IP = args.VPN_IP  # Address to listen on
VPN_PORT = args.VPN_port  # Port to listen on (non-privileged ports are > 1023)


def parse_message(message):
    try:
        MSG = message.split(",")
        if len(MSG) < 3:
            raise ValueError("insufficient data")
        SERVER_IP = MSG[0].strip()
        SERVER_PORT = int(MSG[1].strip())

        client_message = ",".join(MSG[2:]).strip()
        print(f"Destination IP and Port identified from header: '{SERVER_IP}','{SERVER_PORT}'\n")
        print(f"Received client order: '{message}' message length: [{len(message)} bytes]\n")
        # Parse the application-layer header into the destination SERVER_IP, destination SERVER_PORT,
        # and message to forward to that destination
        return SERVER_IP, SERVER_PORT, client_message
    except ValueError as e:
        print(f"parsing error: {e}")
        return None, None, None
    
def encode_message(message):
    # Add an application-layer header
    # Function should properly format the message by encoding it into a specific
    # byte structure that includes both header and message content
    # edits header = "MSG:{len(message)}".encode('utf-8')
    # edits full_message = f"{header.decode('utf-8')},{message}"
    return message.encode('utf-8')

print("VPN starting - opening up cashier station at", VPN_IP, "with our cool tip jar and communication with the kitchen", VPN_PORT)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((VPN_IP, VPN_PORT))
    server_socket.listen()
    print("Waiting for customers... \n")
    conn, addr = server_socket.accept()

    with conn:
        print("Successfully connected to customer: We are open to orders!\n")
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            #receive order and decode
            SERVER_IP, SERVER_PORT, client_message = parse_message(data)
            print(f"Received client order: '{client_message}' Current bytes: [{len(data)} bytes]\n")

            #forward the message to the server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_conn:
                server_conn.connect((SERVER_IP, SERVER_PORT))
                server_conn.sendall(encode_message(client_message))
                response = server_conn.recv(1024).decode("utf-8")

            #send the server's response back to the client
            conn.sendall(response.encode('utf-8'))
            print("Fulfilling order...")

# try:
#     print("VPN starting - connecting to server at IP", SERVER_IP, "and port", SERVER_PORT)
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((SERVER_IP, SERVER_PORT))
#         print(f"connection established, sending message '{encode_message(MSG)}'")
#         s.sendall(bytes(MSG, 'utf-8'))
#         print("Ice cream order sent, thank you for your patience!\n")
#         ECHO_MSG = s.recv(1024).decode("utf-8")

# ## ------ from project 1 ---------
# except ConnectionRefusedError:
#     print("It looks there's no one to take your order... See if the shop is actually open.")
#     exit(1)
# except Exception as e:
#     print(f"Something is wrong with the shop's system... come back later and try ordering again! The sign on the door says: {e}")
#     exit(1)
# ## ------- from project 1 ----------

#message recieved from the server
#closing upon recieving the message from server
# print("Order up! Response received from the kitchen to the cashier.")

### INSTRUCTIONS ###
