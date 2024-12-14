import socket
import threading

def handle_client(client_socket, client_address, client_id):
    print(f"Connected with Client {client_id} at {client_address}")
    
    while True:
        try:
            message=client_socket.recv(1024).decode()
            if not message:
               print("Connection with Client{client_id} at {client_address} closed")
               break
            print(f"received from client {client_id}: {message}")
            broadcast(message, client_id) 
        except Exception as e:
            print(f"error:{e}")
            break

        client_socket.close()
    def broadcast(message,sender_id):
        sender_identifier = f"client {sender_id}"
        for client_socket, client_id in clients:
            if client_id != sender_id:
                try:
                    client_socket.send(f"{sender_identifier}: {message}")
                except Exception as e:
                    print(f"error broadxasting message: {e} ") 
                    client_socket.close() 
                    remove_clienr=(client_socket)
    
    def remove_client(client_socket):
         for index, (c_socket, c_id) in enumerate (clients):
             if c_socket == client_socket:
                 clients.pop(index)
                 break  
             
    HOST = '127.0.0.1'
    PORT = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(2) # Allow only two clients to connect

    print(f"Server listening on {HOST}: {PORT}")

    clients = []

    next_client_id = 1

    while True:
        client_socket,client_address = server_socket.accept()
        clients.append((client_socket, next_client_id))
        client_thread =threading.Thread(target=handle_client, args=(client_socket))
        client_thread.start()
        next_client_id += 1
                
                