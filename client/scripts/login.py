import ast
import sys
import functions as f
from PyQt5 import QtWidgets, uic

class LoginUser:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('gui_files/login.ui', self)  # Load the .ui file
        self.show()  # Show the GUI
        self.logged_in = False  # Set logged_in to False
        self.logged_in_user = None

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
            s = f.connect_to_server()
        except Exception:
            self.login_errorbox.setText('Could not connect to server')
            return

        username = self.login_username.text()   # Get the username from the login_username widget
        password = self.login_password.text()   # Get the password from the login_password widget
        s.send(f'login-~-{username}-~-{password}'.encode())
        result = str(s.recv(1024).decode())  # Get the result from the server
        if result == 'True':
            print('Login successful')
            self.logged_in = True
            self.logged_in_user = LoginUser(username, password)
            self.close()  # If Login successful close the login window
        elif not ast.literal_eval(result)[0]:
            self.login_errorbox.setText('Username or password incorrect')
        else:
            self.login_errorbox.setText('Login failed')  # If Login failed show error message
        s.close()

    def register_button_pressed(self):
        """Check if server is online"""
        try:
            s = f.connect_to_server()
        except Exception:
            self.register_errorbox.setText('Could not connect to server')
            return

        username = self.register_username.text()    # Get the username from the register_username widget
        password = self.register_password.text()    # Get the password from the register_password widget


        if '-~-' in (username or password):
            self.register_errorbox.setText('-~- Cannot be used')
            return
            
        print(f'Register pressed: Username - {username}, Password - {password}')
        s.send(f'register-~-{username}-~-{password}'.encode())
        result = s.recv(1024).decode()  # Get the result from the server
        print(result)
        if str(result) == 'True':  # If the register is True
            print('Register successful')
            self.register_errorbox.setStyleSheet('color: green')  # Set the errorbox colour to green
            self.register_errorbox.setText('Register successful')  # Show the register successful message
        elif not ast.literal_eval(result)[0]:
            self.register_errorbox.setText('Username already exists')  # If the username already exists
        else:
            self.register_errorbox.setText('Register failed')   # If register is False, show error message

    def get_logged_in(self):
        """Get the logged_in value"""
        return self.logged_in

    def get_logged_in_user(self):
        """Get the logged_in_user value"""
        return self.logged_in_user

def login():
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Ui() # Create an instance of our class
    app.exec_() # Start the application
    if window.get_logged_in(): # Return the logged_in value
        return window.get_logged_in_user()
    else:
        print('Login failed')