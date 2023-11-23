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
    print((f"Connected by {addr}"))
    while True:
        data = conn.recv(1024)
        if not data:
            break

        request = data.decode()
        logging.info(f"Received request for {request}")

        if request not in valid_request_list:
            print(f"Invalid request {request}")
            logging.error(f"Invalid request {request}")
            conn.sendall("Invalid request".encode())
        

        if request == 'Download':
            try:
                with open(client_model_name, 'rb') as file:
                    while True:
                        bytes_read = file.read(1024)
                        if not bytes_read:
                            break
                        conn.sendall(bytes_read)
                        print("Uploading...")

                conn.sendall("Finish".encode())
                logging.info(f"Sent {client_model_name} to {addr}")
            except FileNotFoundError:
                conn.sendall("File not found".encode())
                logging.error(f"{request} not found")
            except Exception as e:
                conn.sendall("Unknown error".encode())
                logging.error(f"Unknown error: {e}")
        else:
            conn.sendall("Invalid request".encode())
            logging.warning(f"Invalid request {request} from {addr}")
    conn.close()

# 서버 설정
HOST = '127.0.0.1'
PORT = 12345

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
#     server_socket.bind((HOST, PORT))
#     server_socket.listen()

#     logging.info(f"Server started at {HOST}:{PORT}")
#     print((f"Server started at {HOST}:{PORT}"))

#     while True:
#         conn, addr = server_socket.accept()
#         client_thread = threading.Thread(target=handle_client, args=(conn, addr))
#         client_thread.start()

shutdown_flag = False


def listen_for_shutdown():
    global shutdown_flag
    while True:
        command = input("Enter 's' to stop the server\n")
        if command.lower() == 's':
            shutdown_flag = True
            print("Shutting down server...")
            break

def start_server():
    global shutdown_flag
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        logging.info(f"Server started at {HOST}:{PORT}")
        print(f"Server started at {HOST}:{PORT}")

        # Start the shutdown listener thread
        shutdown_thread = threading.Thread(target=listen_for_shutdown)
        shutdown_thread.start()

        while not shutdown_flag:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

        print("Shutting down server...")
        server_socket.close()
        exit()


start_server()