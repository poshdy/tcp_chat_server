import socket
import threading

user_name = input("What is your user_name: ")

client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
client.connect(("::1", 7000))


def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "user_name":
              client.send(user_name.encode("utf-8"))
            else:
                print(message)
        except:
            print("an error occuerred")
            client.close()
            break


def  send_message():
    while True:
        message = f"{user_name}: {input("")}"
        client.send(message.encode("utf-8"))
        
        
        
receive_thread = threading.Thread(target=receive)

receive_thread.start()

send_thread =  threading.Thread(target=send_message)

send_thread.start()
     
        
