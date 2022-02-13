from PyQt5 import QtWidgets, uic
import sys, socket, ast

f = open('connect.private', 'r')    # Open the file containing the ip and port
socket_connect = ast.literal_eval(f.read().replace('\n', ''))    # Read the file and convert it to a dictionary
f.close()

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('gui_files/login.ui', self) # Load the .ui file
        self.show() # Show the GUI

        """Find all Login Widgets"""
        self.login_button = self.findChild(QtWidgets.QPushButton, 'login_button')
        self.login_username = self.findChild(QtWidgets.QLineEdit, 'login_username')
        self.login_password = self.findChild(QtWidgets.QLineEdit, 'login_password')
        self.login_errorbox = self.findChild(QtWidgets.QLabel, 'login_errorbox')
        self.login_errorbox.setStyleSheet('color: red')  # Set the errorbox to red
        self.login_button.clicked.connect(self.login_button_pressed)  # On click, call the login_button_pressed function

        """Find all Register Widgets"""
        self.register_button = self.findChild(QtWidgets.QPushButton, 'register_button')
        self.register_username = self.findChild(QtWidgets.QLineEdit, 'register_username')
        self.register_password = self.findChild(QtWidgets.QLineEdit, 'register_password')
        self.register_errorbox = self.findChild(QtWidgets.QLabel, 'register_errorbox')
        self.register_errorbox.setStyleSheet('color: red')  # Set the errorbox to red
        self.register_button.clicked.connect(self.register_button_pressed)  # On click, call register_button_pressed

    def login_button_pressed(self):
        """Check if server is online"""
        try:
            s = connect_to_server()
        except Exception:
            self.login_errorbox.setText('Could not connect to server')
            return

        username = self.login_username.text()   # Get the username from the login_username widget
        password = self.login_password.text()   # Get the password from the login_password widget
        s.send(f'login-~-{username}-~-{password}'.encode())
        result = str(s.recv(1024).decode())  # Get the result from the server
        if result == 'True':
            print('Login successful')
            self.close()  # If Login successful close the login window
        else:
            print('Login failed')
            self.login_errorbox.setText('Login failed')  # If Login failed show error message
        s.close()

    def register_button_pressed(self):
        """Check if server is online"""
        try:
            s = connect_to_server()
        except Exception:
            self.register_errorbox.setText('Could not connect to server')
            return

        username = self.register_username.text()    # Get the username from the register_username widget
        password = self.register_password.text()    # Get the password from the register_password widget
        print(f'Register pressed: Username - {username}, Password - {password}')
        s.send(f'register-~-{username}-~-{password}'.encode())
        if str(s.recv(1024)) == 'True':  # If the register is True
            print('Register successful')
            self.close()
        else:
            print('Register failed')
            self.register_errorbox.setText('Register failed')   # If register is False, show error message

def connect_to_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket_connect[0], int(socket_connect[1])))
    return s



app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
app.exec_() # Start the application
