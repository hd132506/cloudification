import socket
import threading
import logging
import torch

# 로깅 설정
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

valid_request_list = ['Download', 'Predict']

client_model_name = 'client_model.pt'
server_model_name = 'server_model.pt'

# 클라이언트 처리 함수
def handle_client(conn, addr):
    logging.info(f"Connected by {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break

        request = data.decode()
        logging.info(f"Received request for {request}")

        assert request in valid_request_list, f"Invalid request {request}"

        if request == 'Download':
            try:
                with open(request, 'r') as file:
                    content = file.read()
                conn.sendall(content.encode())
                logging.info(f"Sent {request} to {addr}")
            except FileNotFoundError:
                conn.sendall("File not found".encode())
                logging.error(f"{request} not found")
        else:
            conn.sendall("Invalid request".encode())
            logging.warning(f"Invalid request {request} from {addr}")
    conn.close()

# 서버 설정
HOST = '127.0.0.1'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    logging.info(f"Server started at {HOST}:{PORT}")
    print((f"Server started at {HOST}:{PORT}"))

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()