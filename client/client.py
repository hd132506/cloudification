import socket
import logging
import torch
import sys
import os
import io


current_script_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_script_path)
parent_directory = os.path.dirname(os.path.dirname(current_directory))
grand_parent_directory = os.path.dirname(parent_directory)

sys.path.append(grand_parent_directory)

from models.resnet import ResNetClient


# 로깅 설정
logging.basicConfig(filename='log_client.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
            client_socket.sendall(request.encode())
            print('Make sure that you have downloaded the client-side Model first.')
            path = input("Enter the input data path (diffault: ./test.pt): ")
            if path == '':
                path = './test.pt'
            try:
                data = torch.load(path)[0].unsqueeze(1).float()
                test_label = torch.load(path)[1]

            except FileNotFoundError:
                print("File not found.")
                logging.error("File not found")
                continue
            except Exception as e:
                print(f"Unknown error: {e}")
                logging.error(f"Unknown error: {e}")
                continue
            print("File loaded successfully.")
            logging.info("File loaded successfully")

            print("Loading clinet-side model...")
            logging.info("Loading client-side model")
            

            print('Original data: ', data)

            model = ResNetClient()
            model.load_state_dict(torch.load(client_model_name))
            model.eval()
            print("Model loaded successfully.")
            logging.info("Model loaded successfully")

            print(data.shape)
            smashed_data = model(data).cpu().detach()
            print(smashed_data.shape)
            print(smashed_data.dtype)
            buff = io.BytesIO()
            torch.save(smashed_data, buff)
            buff.seek(0)
            
            restored = torch.load(buff)



            data_size = len(buff.getvalue())

            client_socket.sendall(data_size.to_bytes(8, 'big'))
            client_socket.sendall(buff.getvalue())
            # assert False

            # client_socket.sendall(smashed_data.cpu().detach().numpy().tobytes())
            # client_socket.sendall('Finish'.encode())
            print("Model fed successfully. Smashed data sent.")
            logging.info("Model fed successfully. Smashed data sent.")

            print("Waiting for prediction result...")
            logging.info("Waiting for prediction result...")

            data_size = int.from_bytes(client_socket.recv(8), 'big')
            print('size', data_size)

            received_bytes = 0
            received_prediction = bytearray()
            while received_bytes < data_size:
                chunk = client_socket.recv(1024*10)
                if not chunk:
                    raise Exception("Connection lost while receiving data")
                received_prediction.extend(chunk)
                received_bytes += len(chunk)

            buffer = io.BytesIO(received_prediction)
            prediction = torch.load(buffer).argmax(dim=1)

            print("Prediction received successfully.")


            print("Prediction accuracy:", end=' ')
            print((prediction == test_label).sum().item() / len(prediction))
            print()



        elif choice == '3':
            print("Exiting.")
            logging.info("Client exited")
            break
        else:
            print("Invalid command.")
            logging.warning("Invalid command entered")
            continue


        