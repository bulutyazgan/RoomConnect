# RoomConnect
A Pygame networking library FOR AN IDEA, OPEN FOR IMPROVEMENT that simplifies multiplayer game development by converting complex ngrok URLs into simple room numbers, while also providing networking methods to easily integrate multiplayer functionalities into basic projects. No port forwarding required!

## How It Works
RoomConnect is not a project that stands on its own, it is only an interpretation to using the dynamic URL's of ngrok's free tier:

1. **Normal ngrok URL**: `tcp://8.tcp.eu.ngrok.io:12345`
2. **RoomConnect room number**: `812345`

This makes sharing connection details simple and user-friendly. The library also includes built-in features to handle networking easily.

## Additional Features
- Message-based game state sync
- Easy Pygame integration
- Automatic connection handling

## Powered by ngrok
This project utilizes [ngrok](https://ngrok.com/) for networking capabilities. ngrok is a fantastic service that makes local development publicly accessible. Please visit their website to learn more about their services and terms.

- This is an open source educational project
- Requires a free ngrok authtoken
- Please review [ngrok's terms of service](https://ngrok.com/tos) before use

> **Disclaimer:** This project is not intended for commercial use or high-traffic applications. Users must adhere to ngrok's free-tier limitations, including connection caps, bandwidth limits, and session expiration policies. Any misuse of ngrok's services, including attempts to circumvent its terms, is strictly prohibited.

## How It Works
RoomConnect uses a message system similar to Pygame's event system. Instead of checking for events, you check for network messages in your game loop:

```python
# Game loop example
while running:
    # Check network messages
    messages = network.get_messages():
        for msg in messages:
            if msg['type'] == 'move':
                handle_player_move(msg['data'])
    
    # Regular game logic
    game_update()
    draw_screen()
```

## Message System
Messages are passed as dictionaries:
```python
{
    'type': 'move',           # Custom message type
    'data': {'x': 10, 'y': 20}, # Any game data
    'sender': 'Player1'       # Automatically added
}
```

## Setup
1. Install dependencies:
```bash
pip install ngrok
```

2. Initialize RoomConnect:
```python
from RoomConnect import RoomConnect

# Initialize
network = RoomConnect()
network.set_token("your-ngrok-token")

# Host Game
room_number = network.host_game("Player1")
print(f"Share this room number: {room_number}")

# OR Join Game
network.join_game("812345", "Player2")
```

## Message System
Messages in RoomConnect follow a two-part structure:

1. **Message Type**: A string identifier that categorizes the message (e.g., 'move', 'attack', 'state')
2. **Message Data**: A dictionary containing the actual game data

Example message formats:
```python
# Player Movement
{
    'type': 'move',           # Message category
    'data': {                 # Game-specific data
        'position': (100, 200),
        'velocity': (5, 0)
    }
}

# Game State
{
    'type': 'state',
    'data': {
        'score': 100,
        'lives': 3,
        'level': 2
    }
}

# Player Action
{
    'type': 'action',
    'data': {
        'action': 'jump',
        'power': 50
    }
}
```

Common message types:
- `'move'`: Player movement updates
- `'state'`: Game state synchronization
- `'action'`: Player actions/commands
- `'join'`: Player connection events
- `'leave'`: Player disconnection events

```python
# Sending messages
network.send_game_data("move", {
    "position": (100, 200),
    "action": "jump"
})

# Receiving messages
messages = network.get_messages()
for msg in messages:
    if msg["type"] == "move":
        player.move(msg["data"]["position"])
```

## Game Loop Integration
```python
while running:
    # Handle network messages
    if messages := network.get_messages():
        for msg in messages:
            if msg["type"] == "move":
                handle_move(msg["data"])
    
    # Your game logic here
    update()
    draw()
```

## Core Functions
- `network.set_token(token)` - Set ngrok auth token
- `network.host_game(nickname)` - Create game room
- `network.join_game(room_number, nickname)` - Join existing room
- `network.send_game_data(type, data)` - Send game data
- `network.get_messages()` - Get received messages
- `network.close()` - Close connections

## Requirements
- Python 3.6+
- Pygame
- ngrok account (free)
