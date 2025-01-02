# RoomConnect Documentation

## Overview
RoomConnect is a networking library for easy multiplayer integration in Pygame projects. It handles connections through ngrok, eliminating the need for port forwarding or complex network setup.

## Setup
1. Install required packages:
```bash
pip install pyngrok
```

2. First use will prompt for ngrok auth token
   - Get token from [ngrok dashboard](https://dashboard.ngrok.com/auth)
   - Token is saved locally for future use

## Basic Usage

### Initialization
```python
from RoomConnect import RoomConnect

network = RoomConnect()
```

### Hosting a Game
```python
# Start hosting
room_number = network.host_game("HostNickname")
print(f"Room Code: {room_number}")  # Share this with other players
```

### Joining a Game
```python
# Join using room number
success = network.join_game("012345", "PlayerNickname")
if not success:
    print("Failed to connect")
```

## Message System

### Registering Message Types
```python
# Register message types before sending/receiving
network.register_message_type("POSITION")
network.register_message_type("SCORE")
network.register_message_type("ACTION")
```

### Sending Data
```python
# Send position update
network.send_game_data("POSITION", {"x": 100, "y": 200})

# Send score update
network.send_game_data("SCORE", 500)

# Send player action
network.send_game_data("ACTION", "JUMP")
```

### Receiving Data
```python
# In game loop
messages = network.get_messages()
for msg in messages:
    if msg['type'] == "POSITION":
        player_pos = msg['data']
        update_player_position(msg['sender'], player_pos)
    elif msg['type'] == "SCORE":
        update_score(msg['sender'], msg['data'])
```

## Complete Example

### Multiplayer Snake Game
```python
import pygame
from RoomConnect import RoomConnect

# Initialize
pygame.init()
network = RoomConnect()
network.register_message_type("MOVE")
network.register_message_type("FOOD")

# Host or Join
is_host = input("Host game? (y/n): ") == "y"
if is_host:
    room = network.host_game("Host")
    print(f"Room Code: {room}")
else:
    room = input("Enter room code: ")
    network.join_game(room, "Player2")

# Game Loop
running = True
while running:
    # Handle game events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                network.send_game_data("MOVE", "RIGHT")
    
    # Process network messages
    messages = network.get_messages()
    for msg in messages:
        if msg['type'] == "MOVE":
            update_player_movement(msg['sender'], msg['data'])
        elif msg['type'] == "FOOD":
            update_food_position(msg['data'])
```

### Properties
- `connected` (bool): Connection status
- `is_host` (bool): Host status
- `is_client` (bool): Client status
- `nickname` (str): Player nickname

### Methods
- `host_game(nickname)`: Start hosting
- `join_game(room_number, nickname)`: Join game
- `register_message_type(msg_type)`: Register message type
- `send_game_data(msg_type, data)`: Send game data
- `get_messages()`: Get received messages
- `close()`: Clean up connections