import datetime
import os,socket, ast, json


def connect_to_server():
    f = open('scripts/connect.private', 'r')    # Open the file containing the ip and port
    socket_connect = ast.literal_eval(f.read().replace('\n', ''))    # Read the file and convert it to a dictionary
    f.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket_connect[0], int(socket_connect[1])))
    return s


def create_driver_file():
    # Get data from server and Create the file containing the drivers and constructors
    s = connect_to_server()
    s.send(b'return_current_driver_and_constructors')
    data = ast.literal_eval(s.recv(10028).decode())
    f = open('data/current_drivers_and_constructors.json', 'w+')
    f.write(str(data))
    f.close()


def return_current_drivers_and_constructors():
    if not os.path.exists('data/current_drivers_and_constructors.json'):
        if not os.path.exists('data'):  # Create the data folder if it doesn't exist
            os.makedirs('data')
        create_driver_file()
    if os.path.getmtime('data/current_drivers_and_constructors.json')/60/60/24 < 1:  # if the file is older than 1 day
        create_driver_file()

    f = open('data/current_drivers_and_constructors.json', 'r')
    data = f.read()    # get data from file
    if data == '[]' or data == None:
        f.close()
        create_driver_file()
        f = open('data/current_drivers_and_constructors.json', 'r')
    f.close()
    return ast.literal_eval(data)

def create_points_file():
    # Get data from server and create the file containing the point data
    f = open('data/points.json', 'w+')
    s = connect_to_server()
    s.send(b'return_point_data')
    point_data = s.recv(100080).decode()
    f.write(f'["{datetime.date.today()}",{point_data}]')
    f.close()

def return_points(driver):
    if not os.path.exists('data/points.json'):
        if not os.path.exists(('data')):
            os.makedirs('data')
        create_points_file()
    f = open('data/points.json')
    data = ast.literal_eval(f.read())
    if data[0] != str(datetime.date.today()) or data[1] == '[]':    # if the file is older than 1 day or empty
        f.close()
        create_points_file()
    f.close()
    try:
        return data[1][1][driver[0]]  # try driver in driver list
    except KeyError:
        try:
            return data[1][0][driver[1]]  # try constructor in constructor list
        except KeyError:
            print(driver, 'Driver/ Constructor not in point data')


def send_team_data(username, password, driver_data, constructor_data):
    s = connect_to_server()
    s.send(f'save_team-~-{username}-~-{password}-~-{constructor_data}-~-{driver_data}'.encode())
    result = s.recv(1024).decode()
    return result

def convert_name_to_id(name):
    '''use the current_drivers_and_constructors.json file to convert the name[1] to the id[0]'''
    data = return_current_drivers_and_constructors()
    for driver in ast.literal_eval(data[0]):
        if driver[1] == name:
            return driver[0]
    for constructor in ast.literal_eval(data[1]):
        if constructor[1] == name:
            return constructor[0]


def convert_points(points):
    return str(250 + int(points)*20)
