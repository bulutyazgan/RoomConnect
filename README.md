# ChatRoom_OverTheNetwork: An Alternative to Port Forwarding for Multiplayer Functionalities

ChatRoom_OverTheNetwork is a chatroom app that leverages ngrok's free utilities to create a network-based chatroom without requiring port forwarding.

## Why?
This project began as an experiment to implement multiplayer functionality in my Pygame projects without dealing with port forwarding. By utilizing ngrok, the server generates a room number that is passed to the client to establish a connection, mimicking the common approach in multiplayer games.

This is currently a prototype of the concept. If it gains interest, I plan to expand and refine it further.

## Setup
1. Create a file named `ngrok_token.txt` in the same directory as `server.py`.
2. Add your ngrok token to the file without any prefix or additional text.
3. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt

## Possible Error
The connection assumes that your ngrok URL uses the "eu" prefix. If you are outside the EU or if ngrok generates a URL with a different format for any reason, you may need to modify the link handling in the code.
