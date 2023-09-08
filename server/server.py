import socket
import threading
import logging

# 로깅 설정
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 클라이언트 처리 함수
def handle_client(conn, addr):
    logging.info(f"Connected by {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break

        request = data.decode()
        logging.info(f"Received request for {request}")
        
        valid_request = request == 'a.txt' or request == 'b.txt'

        if valid_request:
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

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()