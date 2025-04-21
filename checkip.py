import argparse
import requests
import socket

# Define the default file name to be tested.
DEFAULT_FILE = "proxies.txt"

def test_proxy(ip_port, file):
    try:
        # Split the IP address and port.
        ip, port = ip_port.split(":")

        # Get the IP address as an IPv4 address object.
        ip_obj = socket.inet_aton(ip)
        if ip_obj is None:
            file.write(f"{ip_port} (Invalid IP address)\n")
            return False

        # Create a socket with the IP address and port.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((ip, int(port)))
        if sock.connected:
            # If connected, create a tunnel and try to connect to a remote server.
            socks = requests.socks.socksock.socksocket(
                sock, requests.socks.socksocket.SOCK_STREAM
            )
            remote_sock = requests.socks.socksocket(
                requests.socks.socket.SOCK_STREAM
            )
            remote_sock.connect(("www.google.com", 80))
            socks.connect((remote_sock.getpeername()[0], remote_sock.getpeername()[1]))
            socks.sendall(remote_sock.recv(1024))
            socks.recv(1024)
            remote_sock.sendall(b"GET / HTTP/1.1\r\nHost: www.google.com\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\n\r\n")
            remote_response = remote_sock.recv()
            if remote_response:
                status_code = int(remote_response[0:3])
                file.write(f"{ip_port} (Status: {status_code})\n")
                if status_code == 200:
                    file.write(f"{ip_port} (Good)\n")
                    return True
                file.write(f"{ip_port} (Failed: {status_code})\n")
                return False
            socks.close()
            remote_sock.close()
        sock.close()
    except Exception as e:
        file.write(f"{ip_port} ({str(e)})\n")
        return False

    return False

def main():
    parser = argparse.ArgumentParser(description="Test proxies")
    parser.add_argument("--file", required=False, default=DEFAULT_FILE, help="Specify the file containing IP addresses and ports.")
    args = parser.parse_args()

    with open(args.file, "r") as ip_lines:
        ip_good_file = open("ip-good.txt", "a")
        ip_failed_file = open("ip-failed.txt", "a")

        for ip_line in ip_lines:
            ip_port = ip_line.strip()
            working = test_proxy(ip_port, ip_failed_file)
            if working:
                ip_good_file.write(f"{ip_port}\n")

    ip_good_file.close()
    ip_failed_file.close()

if __name__ == "__main__":
    main()