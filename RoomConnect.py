import socket
import threading
import pygame
import ngrok
import os
import json
import time

class RoomConnect:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_host = False
        self.is_client = False
        self.nickname = None
        self.connected = False
        self.port = 27555
        self.room_number = None
        self._setup_ngrok()
        self.message_types = set()
        self.message_queue = []
        self.clients = []  # Only used by host
        
    def _setup_ngrok(self):
        if os.path.exists(".ngrok_token.txt"):
            with open(".ngrok_token.txt", "r") as f:
                ngrok_token = f.read().strip()
            ngrok.set_auth_token(ngrok_token)
        else:
            ngrok_token = input("Please enter your ngrok auth-token (you will only have to do this once): ")
            with open(".ngrok_token.txt", "w") as f:
                f.write(ngrok_token)

    def host_game(self, nickname):
        self.is_host = True
        self.nickname = nickname
        self.socket.bind(('localhost', self.port))
        self.socket.listen()
        
        # Generate room number using ngrok
        tunnel = ngrok.forward(self.port, "tcp")
        public_url = tunnel.url()
        self.room_number = public_url.replace("tcp://", "").replace(".tcp.eu.ngrok.io:", "")
        print(f"Room Number: {self.room_number}")
        
        threading.Thread(target=self._accept_connections, daemon=True).start()
        return self.room_number

    def join_game(self, room_number, nickname):
        self.is_client = True
        self.nickname = nickname
        self.room_number = room_number
        
        # Parse room number
        host = room_number[0] + ".tcp.eu.ngrok.io"
        port = int(room_number[1:])
        
        try:
            self.socket.connect((host, port))
            self.connected = True
            threading.Thread(target=self._receive_data, daemon=True).start()
            return True
        except:
            return False

    def _accept_connections(self):
        while True:
            try:
                client, addr = self.socket.accept()
                threading.Thread(target=self._handle_client, 
                               args=(client, addr), 
                               daemon=True).start()
            except:
                break

    def _handle_client(self, client, addr):
        self.clients.append(client)
        while True:
            try:
                data = client.recv(1024).decode('utf-8')
                if not data:
                    break
                message = json.loads(data)
                if message['type'] in self.message_types:
                    self._broadcast(data, sender=client)
                    self.message_queue.append(message)
            except:
                break
        self.clients.remove(client)
        client.close()

    def _receive_data(self):
        while self.connected:
            try:
                data = self.socket.recv(1024).decode('utf-8')
                if not data:
                    break
                message = json.loads(data)
                if message['type'] in self.message_types:
                    self.message_queue.append(message)
            except:
                break
        self.connected = False

    def _process_data(self, data):
        # Create pygame event from received data
        event_data = {'type': 'NETWORK_DATA', 'data': data}
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, event_data))

    def send_data(self, data):
        if self.connected:
            try:
                message = f"({self.nickname}): {data}"
                if self.is_host:
                    # Broadcast to all clients
                    pass
                else:
                    # Send to host
                    self.socket.send(message.encode('utf-8'))
                return True
            except:
                return False
        return False

    def send_game_data(self, msg_type, data):
        """Send game data of registered type"""
        if msg_type not in self.message_types:
            return False
            
        message = {
            'type': msg_type,
            'data': data,
            'sender': self.nickname,
            'timestamp': time.time()
        }
        
        try:
            if self.is_host:
                self._broadcast(json.dumps(message))
            else:
                self.socket.send(json.dumps(message).encode('utf-8'))
            return True
        except:
            return False

    def get_messages(self):
        """Return and clear message queue"""
        messages = self.message_queue.copy()
        self.message_queue.clear()
        return messages

    def _broadcast(self, data, sender=None):
        """Send data to all clients except sender"""
        if self.is_host:
            for client in self.clients:
                if client != sender:
                    try:
                        client.send(data.encode('utf-8'))
                    except:
                        self.clients.remove(client)

    def register_message_type(self, msg_type):
        """Register a valid message type"""
        self.message_types.add(msg_type)

    def update(self):
        # Call this in game loop
        pass

    def close(self):
        self.socket.close()
        if self.is_host:
            ngrok.disconnect()