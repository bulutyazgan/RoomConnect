# RoomConnect: Easy Multiplayer Integration for Pygame

RoomConnect is a networking library designed to simplify multiplayer game development in Pygame. It handles network connections through ngrok, converting complex URLs into simple room numbers, making it easy to connect players without port forwarding.

## Core Features
- Simple room number system for connections
- Message-based game state synchronization
- Easy integration with Pygame game loops
- Automatic connection handling
- JSON-based data transmission

## How It Works
RoomConnect uses a message system similar to Pygame's event system. Instead of checking for events, you check for network messages in your game loop:

<<<<<<< HEAD
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
=======
## Features
- Converts dynamic ngrok URLs into room numbers for easy sharing.
- Eliminates the need for port forwarding.
- Serves as a foundation for integrating multiplayer functionalities into games or other network-based applications.

## Setup
1. Clone the repository:
   git clone https://github.com/siryazgan/RoomConnect
   cd RoomConnect
   ```
2. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server and client scripts to start the chatroom. (The server will ask for your ngrok auth-token the first time you run it, and save it to a file named `.ngrok_token.txt`)

## Example Usage
Below are some screenshots demonstrating the algorithm's basics in action:

![Example usage](screenshots/screenshot1.png)
![Example usage](screenshots/screenshot2.png)

## Possible Errors and Troubleshooting
- **Region-Specific Issues:** The connection assumes that your ngrok URL uses the "eu" prefix. If you are outside the EU or if ngrok generates a URL with a different format, you may need to modify the link handling in the code.
- **Other Issues:** Ensure that your ngrok token is valid and that all dependencies are installed correctly.

## Feedback
I am open to feedback and suggestions! Feel free to raise issues or contribute.

# RoomConnect 🎮

Make your Pygame games multiplayer! Like playing with friends over the internet.

## How to Start 🚀

1. Install the thing you need:
```bash
pip install ngrok
>>>>>>> 1b36e018fab4397b4ec1a7d00a1b3b1723626386
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
pip install pyngrok pygame
```

2. Initialize RoomConnect:
```python
from RoomConnect import RoomConnect

network = RoomConnect()
network.set_token("your_ngrok_token")
```

## Hosting & Joining Games
```python
# Host
room_number = network.host_game("Player1")
network.register_message_type("move")

# Join
network.join_game(room_number, "Player2")
network.register_message_type("move")
```

## Sending & Receiving Data
```python
# Send game data
network.send_game_data("move", {
    'position': (100, 200),
    'action': 'jump'
})

# Receive data in game loop
messages = network.get_messages()
for msg in messages:
    if msg['type'] == 'move':
        update_player(msg['data'])
```

## Example Projects
See the examples folder for complete implementations:
- Tic-tac-toe multiplayer
- Snake multiplayer (coming soon)
- Pong multiplayer (coming soon)

## Technical Details
- Uses ngrok for connection handling
- JSON serialization for data transfer
- Threaded message handling
- Automatic connection management

## Error Handling
- Connection status monitoring
- Automatic disconnection detection
- Message validation
- Type checking for registered messages

## Future Plans
- More example games
- Built-in game state synchronization
- Latency compensation
- Room management system

## Contributing
Contributions welcome! See CONTRIBUTING.md for guidelines.
