"""
CSE310 Networking Workshop - Example 2 - Solution

This example will explore a peer to peer architecture using Python 
sockets.  The example also a client/server component (Directory Server).
"""

import socketserver
import socket

# The Directory Server will maintain a dictionary with key equal
# to the username and value equal to the IP address.  When a client
# connects, they provide their username, the dictionary is updated, and
# a string representation of that dictionary is returned to the client
# for use.

directory = dict()

class Directory_Server(socketserver.BaseRequestHandler):

    def handle(self):
        # Obtain the address, port, and message (username) sent by client
        source_ip_address = self.client_address[0]
        source_port = self.client_address[1]
        source_msg = str(self.request[0], "UTF-8") 
        print("[{}:{}] => {}".format(source_ip_address, source_port, source_msg))

        # The client will send us their username and we will record the ip address
        directory[source_msg] = source_ip_address

        # Create a string version of the updated directory dictionary to send back
        result = str(directory)

        sock = self.request[1]
        sock.sendto(bytes(result, "UTF-8"), self.client_address)

        print("[{}:{}] <= {}".format(source_ip_address, source_port, result))
        
# Obtain the IP address for the server
host_name = socket.gethostname()
ip_address = socket.gethostbyname(host_name)
server_address = (ip_address, 5000)
print("Starting Server: [{}:{}]".format(server_address[0], server_address[1]))

# Run the server forever
with socketserver.UDPServer(server_address, Directory_Server) as server:
    server.serve_forever()

