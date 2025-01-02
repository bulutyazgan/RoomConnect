# RoomConnect Documentation

## Quick Start
```python
from RoomConnect import RoomConnect

network = RoomConnect()
network.set_token("your_ngrok_token")
```

## Core Functions

### Connection
```python
# Host a game
room_number = network.host_game("Player1")

# Join a game
success = network.join_game(room_number, "Player2")
```

### Message Types
```python
# Register message types before sending
network.register_message_type("MOVE")
network.register_message_type("ATTACK")

# Send game data
network.send_game_data("MOVE", {"x": 100, "y": 200})

# Get received messages
messages = network.get_messages()
```

### Cleanup
```python
# Close connections
network.close()
```

## Function Reference

| Function | Description |
|----------|-------------|
| `set_token(token)` | Set ngrok authentication token |
| `host_game(nickname)` | Start hosting, returns room number |
| `join_game(room_number, nickname)` | Join existing room, returns success boolean |
| `register_message_type(msg_type)` | Register valid message type |
| `send_game_data(msg_type, data)` | Send data to other players |
| `get_messages()` | Get and clear message queue |
| `close()` | Clean up connections |

## Example Game Loop
```python
while running:
    # Send player position
    network.send_game_data("MOVE", player_position)
    
    # Process received messages
    messages = network.get_messages()
    for msg in messages:
        if msg['type'] == "MOVE":
            update_other_player(msg['data'])
```