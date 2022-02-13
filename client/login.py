from PyQt5 import QtWidgets, uic
import sys, socket, ast, time

f = open('connect.private', 'r')
socket_connect = ast.literal_eval(f.read().replace('\n', ''))
f.close()

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('login.ui', self) # Load the .ui file
        self.show() # Show the GUI

        """Login Buttons"""
        self.login_button = self.findChild(QtWidgets.QPushButton, 'login_button') # Find the login button
        self.login_button.clicked.connect(self.login_button_pressed) # Remember to pass the definition/method, not the return value!
        self.login_username = self.findChild(QtWidgets.QLineEdit, 'login_username')
        self.login_password = self.findChild(QtWidgets.QLineEdit, 'login_password')
        self.login_errorbox = self.findChild(QtWidgets.QLabel, 'login_errorbox')

        """Register Buttons"""
        self.register_button = self.findChild(QtWidgets.QPushButton, 'register_button')
        self.register_button.clicked.connect(self.register_button_pressed)
        self.register_username = self.findChild(QtWidgets.QLineEdit, 'register_username')
        self.register_password = self.findChild(QtWidgets.QLineEdit, 'register_password')
        self.register_errorbox = self.findChild(QtWidgets.QLabel, 'register_errorbox')


    def login_button_pressed(self):
        s = connect_to_server()
        username = self.login_username.text()
        password = self.login_password.text()
        print(f'Login pressed: Username - {username}, Password - {password}')
        s.send(f'login-~-{username}-~-{password}'.encode())
        result = str(s.recv(1024).decode())
        if result == 'True':
            print('Login successful')
            self.close()
        else:
            print('Login failed')
            self.login_errorbox.setText('Login failed')
        s.close()

    def register_button_pressed(self):
        s = connect_to_server()
        username = self.register_username.text()
        password = self.register_password.text()
        print(f'Register pressed: Username - {username}, Password - {password}')
        s.send(f'register-~-{username}-~-{password}'.encode())
        if str(s.recv(1024)) == 'True':
            print('Register successful')
            self.close()
        else:
            print('Register failed')
            self.register_errorbox.setText('Register failed')

def connect_to_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket_connect[0], int(socket_connect[1])))
    return s



app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
app.exec_() # Start the application
