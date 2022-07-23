import socket

from config import LOCALHOST, random_port

my_socket = socket.socket()

address_and_port = (LOCALHOST, random_port())
my_socket.bind(address_and_port)
print("Started socket on", address_and_port)

my_socket.listen(10)

conn, addr = my_socket.accept()
print("Got connection", conn, addr)




import socket
import random
import logging

logging.basicConfig(level=logging.DEBUG)

HOST = "127.0.0.1"
PORT = random.randint(10000, 20000)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    print(f"Binding server on {HOST}:{PORT}")
    s.bind((HOST, PORT))
    s.listen()

    conn, addr = s.accept()
    with conn:

        while True:

            data = conn.recv(1024)
            print("Received", data, "from", addr)

            if not data or data == b"close":
                print("Got termination signal", data, "and closed connection")
                conn.close()

            data_request = data.decode("utf-8")
            with open("request.txt", "w") as file:
                file.write(data_request)

            with open("request.txt", "r") as f:
                correct_data = f.read().split("\n")
            method = correct_data[0].split()[0]


            def get_status():
                if len(correct_data[0].split()) > 3:
                    return f'{correct_data[0].split()[4]}{correct_data[0].split()[5]}'
                else:
                    return "200 OK"


            parametr = correct_data[0].split()[1]

            conn.send(
                f"HTTP/1.1 200 OK\n Content-Length: 100\n Connection: close\n Content-Type: text/html\n\n <h1>Request information</h1> \n <p>Method: {method}<br>"
                f"Parametr: {parametr}<br>Status: {get_status()}<br><p>".encode("utf-8"))

            # Log message what we send back
            logging.info(f"Sent '{data}' to {addr}")