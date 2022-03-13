from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon, QPixmap
import sys
import ast
import time
import threading
import functions as f
from scripts.login import LoginUser

class Recent_Point_Changes(QtWidgets.QDialog):
    """Display the point changes dialog box"""
    def __init__(self):
        super(Recent_Point_Changes, self).__init__()
        uic.loadUi('gui_files/point_changes.ui', self)
        self.setWindowTitle('Recent Driver and Constructor Point Changes')  # set title
        self.show()
        self.ok_button = self.findChild(QtWidgets.QPushButton, 'ok_button')
        self.ok_button.clicked.connect(self.close)  # close dialogue box when ok is clicked

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
    def __init__(self, username, password):
        super(Edit_Team, self).__init__()
        uic.loadUi('gui_files/edit_team.ui', self)
        self.username = username
        self.password = password
        self.finished = False
        self.setWindowTitle('Edit Team')  # set title
        '''find combo boxes and buttons'''
        self.constructor_combobox = self.findChild(QtWidgets.QComboBox, 'constructor_drop')
        self.submit_button = self.findChild(QtWidgets.QPushButton, 'submit_button')

        self.total_team_value_label = self.findChild(QtWidgets.QLabel, 'total_team_value')
        self.remaining_money_label = self.findChild(QtWidgets.QLabel, 'remaining_money')
        self.total_money_label = self.findChild(QtWidgets.QLabel, 'total_money')

        self.set_combo_box_data() # set driver and constructor combobox items
        self.submit_button.clicked.connect(self.submit_button_clicked)
        threading.Thread(target=self.label_edit_loop).start()
        self.show()


    def set_combo_box_data(self):
        """Set the data for the combo box"""
        data = f.return_current_drivers_and_constructors()
        # get data from server in  form [[driver1,driver2],[team1,team2]]
        drivers = data[0]
        constructors = data[1]
        # loop through the driver combo boxes
        for i in range(1, 6):
            self.driver_combo_box = self.findChild(QtWidgets.QComboBox, f'driver_drop{i}')
            for driver in ast.literal_eval(drivers):
                self.driver_combo_box.addItem(f'{driver[1]} - {f.convert_points(f.return_points(driver))}')
                # add each driver and their points to the combo box
        for constructor in ast.literal_eval(constructors):
            self.constructor_combobox.addItem(f'{constructor[1]} - {f.convert_points(f.return_points(constructor))}')

    def submit_button_clicked(self):
        """Submit the data to the server"""
        self.finished = True
        # get the data from the combo boxes
        driver_data = []
        for i in range(1, 6):
            driver_data.append(self.findChild(QtWidgets.QComboBox, f'driver_drop{i}').currentText())
        constructor_data = self.constructor_combobox.currentText()
        # send the data to the server
        result = f.send_team_data(self.username, self.password, driver_data, constructor_data)
        if result == 'True':
            self.close()

    def label_edit_loop(self):
        """Loop to update the labels"""
        if self.total_money_label.text() == 'PLACEHOLDER':
            self.total_money_label.setText('1000000')
        while self.finished == False:
            time.sleep(0.5)
            driver_data = []
            for i in range(1, 6):   # for each combo box
                try:    # if there is data to collect
                    driver_data.append(int(self.findChild(QtWidgets.QComboBox, f'driver_drop{i}').currentText().split(' - ')[1]))
                except IndexError:
                    driver_data.append(0)
            try:    # if there is data to collect
                constructor_data = int(self.constructor_combobox.currentText().split(' - ')[1])
            except IndexError:
                constructor_data = 0
            total = sum(driver_data)+constructor_data
            remaining_money = int(self.total_money_label.text()) - total
            self.total_team_value_label.setText(str(total))  # set label text
            self.remaining_money_label.setText(str(remaining_money))  # set label text

    def closeEvent(self, event):
        self.finished = True

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
        self.recent_driver_changes_button.clicked.connect(self.recent_point_changes)
        self.how_val_calc_button.clicked.connect(self.how_val_calc)

        '''Find all labels called team_price, constructor, next_race and driver1 to driver5'''
        self.driver_labels = []
        self.next_race_label = self.findChild(QtWidgets.QLabel, 'next_race')
        self.team_price_label = self.findChild(QtWidgets.QLabel, 'team_price')
        self.constructor_label = self.findChild(QtWidgets.QLabel, 'constructor')
        for i in range(1,6):
            self.driver_labels.append(self.findChild(QtWidgets.QLabel, f'driver{i}'))
        self.refresh_team_data()




    def recent_point_changes(self):
        self.recent_points_change = Recent_Point_Changes()
        self.recent_points_change.show()

    def how_to_play(self):
        self.htp_dialogue_box = HTP_Dialogue_Box()
        self.htp_dialogue_box.show()  # show dialogue box

    def how_val_calc(self):
        self.point_calculation_dialogue_box = Point_Calculation_Dialogue_Box()
        self.point_calculation_dialogue_box.show()  # show dialogue box

    def refresh_team_data(self):
        s = f.connect_to_server()
        s.send(f'return_team-~-{self.username}-~-{self.password}'.encode())
        result = ast.literal_eval(s.recv(1024).decode()[1:-1])
        self.constructor = result[0].split(' - ')
        self.drivers = ast.literal_eval(result[1])
        for i in range(0, 5):
            driver = self.drivers[i].split(' - ')[0]
            driver_old_value = self.drivers[i].split(' - ')[1]
            driver_id = f.convert_name_to_id(driver)
            driver_value = f.convert_points(f.return_points([driver_id,driver]))
            driver_percent_change = round((int(driver_value) - int(driver_old_value))/int(driver_old_value)*100, 2)
            self.driver_labels[i].setText(f'{driver}\n{driver_old_value}\n{driver_value}\n{driver_percent_change}%')

        constructor_new_value = f.convert_points(f.return_points(["",self.constructor[0]]))
        constructor_percent_change = round((int(constructor_new_value) - int(self.constructor[1]))/int(self.constructor[1])*100, 2)
        self.constructor_label.setText(f'{self.constructor[0]}\n{self.constructor[1]}\n{constructor_new_value}\n{constructor_percent_change}%')

    def edit_team_func(self):
        self.edit_team_ui = Edit_Team(self.username, self.password)
        self.edit_team_ui.show()

    def sign_out(self):
        self.close()
        self.destroy()
        sys.exit()




def main(login_user: LoginUser):
    app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
    window = Main_Menu_Ui(login_user.get_username(), login_user.get_password())  # Create an instance of our class
    app.exec_()  # Start the application


