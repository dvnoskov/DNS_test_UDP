import socket
import binascii
from libs_server_local import DB_DNS_in

host = '127.0.0.1'  # Standard loopback interface address (localhost)
port = 53  # Port to listen on (non-privileged ports are > 1023)



UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPServerSocket.bind((host, port))
print("UDP server up and listening")

while (True):
    data = UDPServerSocket.recvfrom(4096)
    in_message = binascii.hexlify(data[0]).decode("utf-8")
    address = data[1]
    clientIP = "Client IP Address:{}".format(address)
    print("incoming message :",clientIP)
    UDPServerSocket.sendto(binascii.unhexlify(DB_DNS_in(in_message)), address)
    print("answear message :", clientIP)


