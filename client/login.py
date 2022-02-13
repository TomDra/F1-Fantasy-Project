from PyQt5 import QtWidgets, uic
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('form.ui', self) # Load the .ui file
        self.show() # Show the GUI
        self.login_button = self.findChild(QtWidgets.QPushButton, 'login_button') # Find the login button
        self.login_button.clicked.connect(self.login_button_pressed) # Remember to pass the definition/method, not the return value!
        self.login_username = self.findChild(QtWidgets.QLineEdit, 'login_username')
        self.login_password = self.findChild(QtWidgets.QLineEdit, 'login_password')
def login_button_pressed(self):
    username = self.login_username.text()
    password = self.login_password.text()
    s.send((f'login-~-{username}-~-{password}').encode())
    if s.recive(1024) == True:
        self.close()
        
    


app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
app.exec_() # Start the application
