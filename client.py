import socket
import threading

number = input("Enter Room Number: ")
HOST = number[0] + ".tcp.eu.ngrok.io"
PORT = int(number[1:])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nick = input("Select your Nickname: ")
s.connect((HOST, PORT))

def send_thread(nick):
    print(f"[CONNECTION SUCCESFUL] Hello {nick}, you can start chatting")
    while True:
        msg_send = f"({nick}): " + input()
        s.send(msg_send.encode('utf-8'))

def recv_thread():
    while True:
        msg_recv = s.recv(1024).decode('utf-8')
        print(msg_recv)

threading.Thread(target=recv_thread).start()
threading.Thread(target=send_thread, args=(nick,)).start()
