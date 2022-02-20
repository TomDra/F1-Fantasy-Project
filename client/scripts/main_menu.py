from PyQt5 import QtWidgets, uic
import sys
from client import functions as f

class HTP_Dialogue_Box(QtWidgets.QDialog):
    """Display the how to play dialog box"""
    def __init__(self):
        super(HTP_Dialogue_Box, self).__init__()
        uic.loadUi('gui_files/how_to_play.ui', self)
        self.setWindowTitle('How to Play')  # set title
        self.show()
        self.ok_button = self.findChild(QtWidgets.QPushButton, 'ok_button')
        self.ok_button.clicked.connect(self.close)  # close dialogue box when ok is clicked


class Main_Menu_Ui(QtWidgets.QMainWindow):
    def __init__(self, temp_username, temp_password):
        super(Main_Menu_Ui, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('gui_files/main_menu.ui', self)  # Load the .ui file
        self.show()  # Show the GUI
        self.username = temp_username
        self.password = temp_password
        self.setWindowTitle('Main Menu')

        """Find all buttons"""
        self.edit_team_button = self.findChild(QtWidgets.QPushButton, 'edit_team')
        self.refresh_button = self.findChild(QtWidgets.QPushButton, 'refresh')
        self.how_to_play_button = self.findChild(QtWidgets.QPushButton, 'explain_htp')  # explain how to play
        self.recent_driver_changes_button = self.findChild(QtWidgets.QPushButton, 'recent_driver_changes')
        self.how_val_calc_button = self.findChild(QtWidgets.QPushButton, 'how_vac')    # how values are calculated
        self.exit_button = self.findChild(QtWidgets.QPushButton, 'exit')

        """bind buttons to functions"""
        self.refresh_button.clicked.connect(self.refresh_team_data)
        self.exit_button.clicked.connect(self.sign_out)
        #self.edit_team_button.clicked.connect(self.edit_team)
        self.how_to_play_button.clicked.connect(self.how_to_play)
        #self.recent_driver_changes_button.clicked.connect(self.recent_driver_changes)
        #self.how_val_calc_button.clicked.connect(self.how_val_calc)

    def how_to_play(self):
        self.htp_dialogue_box = HTP_Dialogue_Box()
        self.htp_dialogue_box.show()  # show dialogue box

    def refresh_team_data(self):
        s = f.connect_to_server()
        s.send(f'return_team-~-{self.username}-~-{self.password}'.encode())
        result = s.recv(1024).decode()
        print(result)

    def sign_out(self):
        self.close()
        self.destroy()
        sys.exit()




def main():
    app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
    window = Main_Menu_Ui('test','test')  # Create an instance of our class
    app.exec_()  # Start the application


