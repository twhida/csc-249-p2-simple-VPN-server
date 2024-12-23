#!/usr/bin/env python3
import socket
import arguments
import argparse

# Run 'python3 echo-server.py --help' to see what these lines do
parser = argparse.ArgumentParser('Starts a server that returns the data sent to it unmodified')
parser.add_argument('--server_IP', help='IP address at which to host the server', **arguments.ip_addr_arg)
parser.add_argument('--server_port', help='Port number at which to host the server', **arguments.server_port_arg)
args = parser.parse_args()

SERVER_IP = args.server_IP  # Address to listen on
SERVER_PORT = args.server_port  # Port to listen on (non-privileged ports are > 1023)
# -------------------------- from project 1 --------------------------
def understand(client_order):
    print(f"Order recieved: {client_order}")
    order = client_order.split(",")
    service_type = order[0].strip()
    order_type = order[1].strip()

    if order_type == "scoop":
        if len(order) < 5:
            return "Your scoop order is missing your preferences! Please try again."
        size = order[2].strip()
        flavor = order[3].strip()
        syrup = order[4].strip()
        syrup2 = order[5].strip()
        return f"Here is your {size} {flavor} {order_type} with {syrup} {syrup2} for {service_type}!"

    elif order_type == "milkshake":
        if len(order) < 5:
            return "Your milkshake order is missing your preferences! Please try again."
        flavor = order[2].strip()
        milk = order[3].strip()
        milk2 = order[4].strip()
        syrup = order[5].strip()
        return f"Here is your {flavor} {order_type} with {milk} {milk2} and {syrup} for {service_type}!"

    elif order_type == "chipwich":
        if len(order) < 4:
            return "Your chipwich order is missing your preferences! Please try again."
        flavor = order[2].strip()
        cookie = order[3].strip()
        cookie2 = order[4].strip()
        return f"Here is your {flavor} chipwich with {cookie} {cookie2} cookies for {service_type}!"
    else:
        return "You did not specify an order type! Please try ordering again."
# -------------------------- from project 1 --------------------------

print("Server starting - opening up shop at", SERVER_IP, "with our cool entryway door with model number", SERVER_PORT)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_IP, SERVER_PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected established with {addr}. Successfully opened shop: Kitchen is open to orders!\n")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            #receive order and decode
            client_order = data.decode('utf-8')
            print(f"Received client order: '{client_order}' Current bytes: [{len(data)} bytes]\n")
            #print(f"Received client message: '{data!r}' [{len(data)} bytes]")

            order_fulfillment = understand(client_order)
            print(f"Saying '{order_fulfillment}' to the to customer!\n")
            conn.sendall(order_fulfillment.encode('utf-8'))

            # print(f"echoing '{data!r}' back to client")
            # conn.sendall(data)

# print("server is done!")
print("Really Pretty Cool kitchen has completed the order, Ice cream has been given to the cashier. Closing kitchen...\n")