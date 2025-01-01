import socket
import ngrok
import threading

with open("ngrok_token.txt", "r") as f:
    ngrok_token = f.read()
ngrok.set_auth_token(ngrok_token)

HOST = "localhost"
PORT = 27555

host_name = input("Enter a HostName: ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

public_url = ngrok.forward(PORT, "tcp")
number = public_url.url().replace("tcp://", "").replace(".tcp.eu.ngrok.io:", "")
print(f"Hello {host_name}, Server is started")
print(f"Room Number: {number}")

def send_thread(conn):
    while True:
        msg_send = f"({host_name}): " + input()
        conn.send(msg_send.encode('utf-8'))

def recv_thread(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    while True:
        msg_recv = conn.recv(1024).decode('utf-8')
        print(msg_recv)


conn, addr = s.accept()
threading.Thread(target=recv_thread, args=(conn, addr)).start()
threading.Thread(target=send_thread, args=(conn,)).start()
