from PyQt5.QtWidgets import QApplication,QMainWindow,QLabel,QPushButton,QWidget,QVBoxLayout,QStackedWidget,QLineEdit,QTextEdit,QListWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal, QObject
import sys
import sqlite3
import socket
import threading


HEADER=64
PORT=5050
SERVER= socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
FORMAT='utf-8'
DISCONNECT_MESSAGE="DISCONNECT"

class Communicate(QObject):
    message_received = pyqtSignal(str)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CHAT APPLICATION")
        self.setGeometry(0,0,500,500)
        self.initUI()
        self.initDB()
        self.client_socket = None
        self.current_user = None

    def initDB(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users_chat (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                receiver TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def initUI(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.name=QLineEdit(self)
        self.pwd=QLineEdit(self)
        
        self.loginPage = QWidget()
        self.loginLayout=QVBoxLayout()
        self.loginPage.setLayout(self.loginLayout)

        enter_name=QLabel("Enter Username:",self)
        enter_pwd=QLabel("Enter Password",self)
        enter_name.setFont(QFont("Arial",20))
        enter_pwd.setFont(QFont("Arial",20))

        self.name.setPlaceholderText("enter username")
        self.pwd.setPlaceholderText("enter password")
        self.pwd.setEchoMode(QLineEdit.Password)

        login_button=QPushButton("login",self)
        login_button.setFont(QFont("Arial",20))
        login_button.setGeometry(30,100,200,300)
        login_button.clicked.connect(self.chat_interface)
        
        register_button = QPushButton("Register", self)
        register_button.setFont(QFont("Arial", 20))
        register_button.clicked.connect(self.showRegistrationPage)

        self.loginLayout.addWidget(enter_name)
        self.loginLayout.addWidget(self.name)
        self.loginLayout.addWidget(enter_pwd)
        self.loginLayout.addWidget(self.pwd)
        self.loginLayout.addWidget(login_button)
        self.loginLayout.addWidget(register_button)

        #for the panel
        self.loginLayout.setContentsMargins(100, 100, 100, 100)
        self.loginLayout.setSpacing(20)

        self.stacked_widget.addWidget(self.loginPage)

        # Registration Page
        self.regPage = QWidget()
        self.regLayout = QVBoxLayout()
        self.regPage.setLayout(self.regLayout)

        reg_enter_name = QLabel("Enter Username:", self)
        reg_enter_pwd = QLabel("Enter Password:", self)
        reg_enter_name.setFont(QFont("Arial", 20))
        reg_enter_pwd.setFont(QFont("Arial", 20))

        self.reg_name = QLineEdit(self)
        self.reg_pwd = QLineEdit(self)
        self.reg_name.setPlaceholderText("enter username")
        self.reg_pwd.setPlaceholderText("Enter password")
        self.reg_pwd.setEchoMode(QLineEdit.Password)

        register = QPushButton("Register", self)
        register.setFont(QFont("Arial", 20))
        register.clicked.connect(self.registerUser )

        to_login = QPushButton("Back to Login", self)
        to_login.setFont(QFont("Arial", 20))
        to_login.clicked.connect(self.showLoginPage)

        self.regLayout.addWidget(reg_enter_name)
        self.regLayout.addWidget(self.reg_name)
        self.regLayout.addWidget(reg_enter_pwd)
        self.regLayout.addWidget(self.reg_pwd)
        self.regLayout.addWidget(register)
        self.regLayout.addWidget(to_login)

       
        self.stacked_widget.addWidget(self.regPage)

        self.chatPage = QWidget()
        self.chatLayout = QVBoxLayout()
        self.chatPage.setLayout(self.chatLayout)

        # User List Page
        self.userListPage = QWidget()
        self.userListLayout = QVBoxLayout()
        self.userListPage.setLayout(self.userListLayout)

        self.user_list = QListWidget(self)
        self.user_list.itemClicked.connect(self.start_chat_with_user)
        
        self.userListLayout.addWidget(self.user_list)
        self.stacked_widget.addWidget(self.userListPage)

        #chat
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)  
        self.chatLayout.addWidget(self.text_area)

        self.input_field = QLineEdit(self)
        self.chatLayout.addWidget(self.input_field)

        msg=self.input_field.text()
        self.send = QPushButton('Send', self)
        self.send.clicked.connect(self.send_message)

        self.back = QPushButton('Go Back', self)
        self.back.clicked.connect(self.go_back_to_userlist)
        
        self.chatLayout.addWidget(self.send)
        self.chatLayout.addWidget(self.back)
        self.stacked_widget.addWidget(self.chatPage)
        self.socket = None

    def showRegistrationPage(self):
        self.stacked_widget.setCurrentWidget(self.regPage)

    def showLoginPage(self):
        self.stacked_widget.setCurrentWidget(self.loginPage)

    def showUserListPage(self):
        self.load_user_list()
        self.stacked_widget.setCurrentWidget(self.userListPage)

    def load_user_list(self):
        self.user_list.clear()
        self.cursor.execute("SELECT username FROM users_chat")
        users = self.cursor.fetchall()
        for user in users:
            if user[0] != self.current_user:  
                self.user_list.addItem(user[0])

    def registerUser (self):
        username = self.reg_name.text()
        password = self.reg_pwd.text()
        if username and password:
            try:
                self.cursor.execute("INSERT INTO users_chat (username, password) VALUES (?, ?)", (username, password))
                self.conn.commit()
                print("User  registered successfully!")
                self.showLoginPage()  
            except sqlite3.IntegrityError:
                print("Username already exists. Please choose a different username.")
        else:
            print("Please enter both username and password.")
    def go_back_to_userlist(self):
        self.showUserListPage()   
    def chat_interface(self):
        n = self.name.text()
        p = self.pwd.text()
        self.cursor.execute("SELECT * FROM users_chat WHERE username=? AND password=?", (n, p))
        if self.cursor.fetchone():
            self.current_user = n
            self.showUserListPage() 
        else:
            print("Invalid username or password.")
    
    def start_chat_with_user(self, item):
        selected_user = item.text()
        self.text_area.clear()
        self.load_chat_history(selected_user)
        self.client_socket = self.start_client(selected_user)
        threading.Thread(target=self.receive_messages, args=(self.client_socket,)).start()
        self.stacked_widget.setCurrentIndex(3)

    def load_chat_history(self, selected_user):
        self.text_area.clear()
        self.cursor.execute("SELECT sender, message FROM chat_history WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?)", 
                            (self.current_user, selected_user, selected_user, self.current_user))
        messages = self.cursor.fetchall()
        for sender, message in messages:
            self.text_area.append(f"{sender}: {message}")
    
    def receive_messages(self,client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                self.text_area.append(message)
            except:
                print("An error occurred!")
                client_socket.close()
                break

    def send_message(self):
        message = self.input_field.text()
        if message and self.client_socket:
            self.client_socket.send(message.encode('utf-8'))
            self.save_chat_history(self.current_user, message)  
            self.input_field.clear() 

    def save_chat_history(self, sender, message):
        receiver = self.user_list.currentItem().text()
        self.cursor.execute("INSERT INTO chat_history (sender, receiver, message) VALUES (?, ?, ?)", (sender, receiver, message))
        self.conn.commit()
        
    def start_client(self, username):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 5050))
        client_socket.send(username.encode('utf-8'))
        return client_socket
    
    

def main():
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()
