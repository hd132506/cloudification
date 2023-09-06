import socket
import logging

# 로깅 설정
logging.basicConfig(filename='client.log', level=logging.INFO)

# 서버 설정
HOST = '127.0.0.1'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))

    while True:
        choice = input("1: Download a.txt\n2: Download b.txt\n3: Exit\nEnter your choice: ")

        if choice == '1':
            request = 'a.txt'
        elif choice == '2':
            request = 'b.txt'
        elif choice == '3':
            print("Exiting.")
            logging.info("Client exited")
            break
        else:
            print("Invalid command.")
            logging.warning("Invalid command entered")
            continue

        client_socket.sendall(request.encode())
        data = client_socket.recv(1024).decode()

        if data == "File not found":
            print(f"{request} not found on server.")
            logging.error(f"{request} not found on server")
        elif data == "Invalid request":
            print("Invalid request.")
            logging.warning("Invalid request sent")
        else:
            with open(request, 'w') as file:
                file.write(data)
            print(f"{request} downloaded successfully.")
            logging.info(f"{request} downloaded successfully")