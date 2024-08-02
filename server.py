import threading
import socket

host = "::1"
port = 7000


server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

server.bind((host, port))

server.listen()


clients = []
user_names = []


def broadcast(message):
    for client in clients:
        client.send(message)


def manage_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            client_index = clients.index(client)
            clients.remove(client_index)
            client.close()
            user_name = user_names.index(client_index)
            user_names.remove(user_name)
            broadcast(f"{user_name} left.")
            break


def receive_connections():
    while True:
        client, add = server.accept()
        print(f"connected with {str(add)}!")
        client.send("user_name".encode("utf-8"))
        user_name = client.recv(1024).decode("utf-8")

        user_names.append(user_name)
        clients.append(client)

        print(f"user_name of the client is {user_name}")
        broadcast(f"{user_name} Joined!".encode("utf-8"))
        client.send("connected to the server".encode("utf-8"))

        thread = threading.Thread(target=manage_client, args=(client,))

        thread.start()


print("Server is listening..")
receive_connections()
