import socket
import logging

# 로깅 설정
logging.basicConfig(filename='client.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 서버 설정
HOST = '127.0.0.1'
PORT = 12345

client_model_name = 'client_model.pt'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))

    while True:
        choice = input("1: Download client-side ResNet\n2: Make prediction\n3: Exit\nEnter your choice: ")

        if choice == '1':
            request = 'Download'

            client_socket.sendall(request.encode())
            bytes_read = client_socket.recv(1024)

            if bytes_read == "File not found".encode():
                print(f"{request} failed: file not found on server.")
                logging.error(f"{request} failed: file not found on server.")
            elif bytes_read == "Invalid request".encode():
                print("Invalid request.")
                logging.warning("Invalid request sent")
            else:
                with open(client_model_name, 'wb') as file:
                    while not bytes_read == 'Finish'.encode():
                        file.write(bytes_read)
                        bytes_read = client_socket.recv(1024)
                        
                    
                print(f"{client_model_name} downloaded successfully.")
                logging.info(f"{client_model_name} downloaded successfully")


        elif choice == '2':
            request = 'Predict'
        elif choice == '3':
            print("Exiting.")
            logging.info("Client exited")
            break
        else:
            print("Invalid command.")
            logging.warning("Invalid command entered")
            continue


        