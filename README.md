# Chat Application

A simple chat application built using Python's socket programming and PyQt5 for the graphical user interface (GUI). This application allows users to register, log in, and chat with each other in real-time.

## Features

- User registration and login
- Real-time messaging between users
- Chat history stored in a SQLite database
- User-friendly GUI built with PyQt5
- Multi-threaded server to handle multiple clients

## Requirements

- Python 3.x
- PyQt5
- SQLite (comes with Python standard library)

## Installation

1. Clone the repository or download the source code.

   ```bash
   git clone <repository-url>
   cd <repository-directory>

## Usage

1. **Start the Server:**
   - Navigate to the directory containing the server code.
   - Run the server script:
     ```bash
     python server.py
2. **Start the Client:**
   - Open another terminal window.
   - Navigate to the directory containing the client code.
   - Run the client script:
     ```bash
     python client.py
3. **Register a New User:**
   Enter a username and password on the login page and click **"Register"** to create a new account.
5. **Log In:**
   Enter your username and password on the login page and click **"Login"**.
6. **Chat with Other Users:**
   After logging in, you will see a list of registered users. Click on a username to start chatting.Type your message in the input field and click "Send" to send 
   the message.

## Database Structure
The application uses SQLite to store user credentials and chat history. The following tables are created:

- **users_chat:** Stores usernames and passwords.
- **chat_history:** Stores messages exchanged between users, including sender, receiver, message content, and timestamp.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
Thanks to the PyQt5 documentation for guidance on building the GUI.
Thanks to the Python community for the resources and libraries that made this project possible
