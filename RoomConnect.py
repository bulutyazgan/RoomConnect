import socket
import threading
import ngrok
import json

class RoomConnect:
    def __init__(self, port=27555, region="eu"):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_host = False
        self.is_client = False
        self.nickname = None
        self.connected = False
        self.port = port
        self.room_number = None
        self.message_types = set()
        self.message_queue = []
        self.clients = []  # Only used by host
        self.regions = {
            "eu": ".eu", 
            "us": ""
            }
        if region in self.regions:
            self.region = region

    def set_token(self, token):
        """Set ngrok authentication token"""
        ngrok.set_auth_token(token)

    def host_game(self, nickname):
        self.is_host = True
        self.nickname = nickname
        self.socket.bind(('localhost', self.port))
        self.socket.listen()
        
        # Generate room number using ngrok
        tunnel = ngrok.forward(self.port, "tcp")
        public_url = tunnel.url()
        self.room_number = public_url.replace("tcp://", "").replace(f".tcp{self.regions[self.region]}.ngrok.io:", "")
        
        threading.Thread(target=self._accept_connections, daemon=True).start()
        return self.room_number

    def join_game(self, room_number, nickname):
        self.is_client = True
        self.nickname = nickname
        self.room_number = room_number
        
        # Parse room number
        host = room_number[0] + f".tcp{self.regions[self.region]}.ngrok.io"
        port = int(room_number[1:])
        
        try:
            self.socket.connect((host, port))
            self.connected = True
            threading.Thread(target=self._receive_data, daemon=True).start()
            return True
        except:
            return False

    def _accept_connections(self):
        self.connected = True
        while self.is_host and self.connected:
            try:
                client, addr = self.socket.accept()
                self.clients.append(client)
                print(f"Client connected: {addr}")
                threading.Thread(target=self._handle_client, args=(client, addr), daemon=True).start()
            except:
                break
        self.connected = False

    def _handle_client(self, client, addr):
        while True:
            try:
                data = client.recv(1024).decode('utf-8')
                if not data:
                    break
                message = json.loads(data)
                if message['type'] in self.message_types:
                    self._broadcast(data, client)
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

    def _broadcast(self, data, sender=None):
        if self.is_host:
            for client in self.clients:
                if client != sender:
                    try:
                        client.send(data.encode('utf-8'))
                    except:
                        self.clients.remove(client)

    def send_game_data(self, msg_type, data):
        """Send game data as JSON"""
        if msg_type in self.message_types:
            message = {
                'type': msg_type,
                'data': data,
                'sender': self.nickname
            }
            try:
                data = json.dumps(message)
                if self.is_host:
                    self._broadcast(data)
                else:
                    self.socket.send(data.encode('utf-8'))
                return True
            except:
                return False
        return False

    def get_messages(self):
        """Get and clear message queue"""
        messages = self.message_queue.copy()
        self.message_queue.clear()
        return messages

    def register_message_type(self, msg_type):
        """Register a valid message type"""
        self.message_types.add(msg_type)

    def close(self):
        """Clean up connections"""
        self.connected = False
        if self.is_host:
            for client in self.clients:
                client.close()
        self.socket.close()
        if self.is_host:
            ngrok.disconnect()