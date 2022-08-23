
import os
import socket
import time

SERVER_ADDRESS = (HOST, PORT) = '', 8888

def handle_client(client_connection):
    request_data = client_connection.recv(1024)
    print(request_data.decode('utf-8'))

    http_response = b"""\
HTTP/1.1 200 OK

Hello from server 
"""

    client_connection.sendall(http_response)
    time.sleep(10)

def serve_forever():

    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(1)

    print(f'serving HTTP on port {PORT}...')

    while True:
        client_connection, client_address = listen_socket.accept()
        pid = os.fork()
        if pid == 0:
            listen_socket.close()
            handle_client(client_connection)
            client_connection.close()
            os._exit(1)
        else:
            client_connection.close()