from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon, QPixmap
import sys
import ast
import functions as f
from scripts.login import LoginUser

class HTP_Dialogue_Box(QtWidgets.QDialog):
    """Display the how to play dialog box"""
    def __init__(self):
        super(HTP_Dialogue_Box, self).__init__()
        uic.loadUi('gui_files/how_to_play.ui', self)
        self.setWindowTitle('How to Play')  # set title
        self.show()
        self.ok_button = self.findChild(QtWidgets.QPushButton, 'ok_button')
        self.ok_button.clicked.connect(self.close)  # close dialogue box when ok is clicked

class Point_Calculation_Dialogue_Box(QtWidgets.QDialog):
    """Display the point calculation dialogue box"""
    def __init__(self):
        super(Point_Calculation_Dialogue_Box, self).__init__()
        uic.loadUi('gui_files/point_calculation.ui', self)
        self.setWindowTitle('Point Calculation')  # set title
        label = self.findChild(QtWidgets.QLabel, 'point_calculation_pixelmap')
        pixmap = QPixmap('gui_files/points_value_calculation.png')
        label.setPixmap(pixmap)
        self.show()
        self.ok_button = self.findChild(QtWidgets.QPushButton, 'ok_button')
        self.ok_button.clicked.connect(self.close)  # close dialogue box when ok is clicked

class Edit_Team(QtWidgets.QMainWindow):
    def __init__(self):
        super(Edit_Team, self).__init__()
        uic.loadUi('gui_files/edit_team.ui', self)
        self.setWindowTitle('Edit Team')  # set title
        self.set_combo_box_data()
        #self.driver_comboboxes = []
        #for i in range(1,5+1):
            #self.driver_comboboxes.append(self.findChild(QtWidgets.QComboBox, f'driver_combobox_{i}'))
        self.constructor_combobox = self.findChild(QtWidgets.QComboBox, 'constructor_combobox')
        self.submit_button = self.findChild(QtWidgets.QPushButton, 'submit_button')
        self.show()

    def set_combo_box_data(self):
        """Set the data for the combo box"""
        s = f.connect_to_server()
        s.send(b'return_current_driver_and_constructors')
        data = ast.literal_eval(s.recv(1024).decode())    # get data from server in [driver1,driver2---team1,team2]
        drivers = data[0]
        constructors = data[1]
        #for self.driver_combo_box in self.driver_comboboxes: # loop through the driver combo boxes
        for i in range(1, 5 + 1):
            self.driver_combo_box = self.findChild(QtWidgets.QComboBox, f'driver_drop{i}')
            for driver in drivers:
                self.driver_combo_box.addItems(f'{driver} - {f.return_driver_points(driver)}')
                # add each driver and their points to the combo box
        for constructor in constructors:
            self.constructor_combobox.addItems(f'{constructor}')


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
        self.edit_team_button.clicked.connect(self.edit_team_func)
        self.how_to_play_button.clicked.connect(self.how_to_play)
        #self.recent_driver_changes_button.clicked.connect(self.recent_driver_changes)
        self.how_val_calc_button.clicked.connect(self.how_val_calc)

    def how_to_play(self):
        self.htp_dialogue_box = HTP_Dialogue_Box()
        self.htp_dialogue_box.show()  # show dialogue box

    def how_val_calc(self):
        self.point_calculation_dialogue_box = Point_Calculation_Dialogue_Box()
        self.point_calculation_dialogue_box.show()  # show dialogue box

    def refresh_team_data(self):
        s = f.connect_to_server()
        s.send(f'return_team-~-{self.username}-~-{self.password}'.encode())
        result = s.recv(1024).decode()
        print(result)

    def edit_team_func(self):
        self.edit_team_ui = Edit_Team()
        self.edit_team_ui.show()

    def sign_out(self):
        self.close()
        self.destroy()
        sys.exit()




def main(login_user: LoginUser):
    app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
    window = Main_Menu_Ui(login_user.get_username(), login_user.get_password())  # Create an instance of our class
    app.exec_()  # Start the application


