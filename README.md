# ChatRoom: Simplified Multiplayer Connections Without Port Forwarding

This is a proof-of-concept chatroom app designed to simplify network connections for developers. By leveraging ngrok's dynamic URLs and stripping them down into room numbers, it eliminates the need for port forwarding, making it easier to establish multiplayer connections over the internet.

## What This Project Does
This project converts ngrok-generated URLs into simplified room numbers, allowing clients to connect using these numbers. It mimics a common approach in multiplayer games, making it easier for developers to implement internet-based connections without the hassle of configuring port forwarding.

Currently, the project functions as a basic chatroom but demonstrates the potential to be integrated into more complex systems, such as multiplayer games built with frameworks like Pygame.

## Why I Created This
I developed this project as an experiment to integrate easy multiplayer connectivity into low-level projects without relying on complex setups. For developers working on Pygame or similar frameworks, this approach simplifies the process of adding multiplayer features.

While this is just a prototype, I am open to expanding it further if it garners interest, potentially making it more compatible with game development frameworks.

## Target Audience
This project is ideal for:
- Developers looking to add internet-based multiplayer features to their low-level projects.
- Game developers using frameworks like Pygame who want to simplify multiplayer implementation.
- Anyone seeking an alternative to port forwarding for establishing network connections.

## Features
- Converts dynamic ngrok URLs into room numbers for easy sharing.
- Eliminates the need for port forwarding.
- Serves as a foundation for integrating multiplayer functionalities into games or other network-based applications.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/siryazgan/ChatRoom_OverTheNetwork
   cd ChatRoom_OverTheNetwork
   ```
2. Create a file named `ngrok_token.txt` in the same directory as `server.py`.
3. Add your ngrok token to the file without any prefix or additional text.
4. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the server and client scripts to start the chatroom.

## Example Usage
Below are some screenshots demonstrating the application in action:

![Example usage](screenshot1.png)
![Example usage](screenshot2.png)

## Possible Errors and Troubleshooting
- **Region-Specific Issues:** The connection assumes that your ngrok URL uses the "eu" prefix. If you are outside the EU or if ngrok generates a URL with a different format, you may need to modify the link handling in the code.
- **Other Issues:** Ensure that your ngrok token is valid and that all dependencies are installed correctly.

## Future Plans
If there is interest, I plan to:
- Expand the project for better integration with game development frameworks like Pygame.
- Add features such as dynamic room creation and more robust error handling.
- Explore additional use cases for the room number functionality.

## Feedback
I am open to feedback and suggestions! Feel free to raise issues or contribute via pull requests on the [GitHub repository](https://github.com/siryazgan/ChatRoom_OverTheNetwork).
