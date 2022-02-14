from PyQt5 import QtWidgets, uic
import sys, socket, ast


class Main_Menu_Ui(QtWidgets.QMainWindow):
    def __init__(self, temp_username, temp_password):
        super(Main_Menu_Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('gui_files/main_menu.ui', self) # Load the .ui file
        self.show() # Show the GUI
        self.username = temp_username
        self.password = temp_password

    def refresh_team_data(self):
        s = connect_to_server()



def main():
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Main_Menu_Ui() # Create an instance of our class
    app.exec_() # Start the application
