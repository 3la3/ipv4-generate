import random
import socket

def generate_ip():
    # Generate a random IPv4 address
    ip = ""
    for i in range(4):
        octet = random.randint(0, 255)
        ip += str(octet) + "."
    ip = ip[:-1]  # Remove the last "."
    return ip

def generate_port():
    # Generate a random port number between 1 and 65535
    port = random.randint(1, 65535)
    return port

while True:
    ip = generate_ip()
    port = generate_port()
    result = f"{ip}:{port}"
    print(result)