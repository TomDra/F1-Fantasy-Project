import datetime
import os,socket, ast, json


def connect_to_server():
    f = open('scripts/connect.private', 'r')    # Open the file containing the ip and port
    socket_connect = ast.literal_eval(f.read().replace('\n', ''))    # Read the file and convert it to a dictionary
    f.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket_connect[0], int(socket_connect[1])))
    return s

def create_points_file():
    f = open('data/points.json', 'w+')
    s = connect_to_server()
    s.send(b'return_point_data')   # todo: create this command on server side
    point_data = s.recv(2048).decode()
    f.write(f'["{datetime.date.today()}",{point_data}]')
    f.close()

def return_driver_points(driver):
    if not os.path.exists('data/points.json'):
        if not os.path.exists(('data')):
            os.makedirs('data')
        create_points_file()
    else:
        f = open('data/points.json')
        data = ast.literal_eval(f.read())   #fixme
        if data[0] != str(datetime.date.today()) or data[1] == '[]':
            f.close()
            create_points_file()
        else:
            f.close()
            return data[1][driver]
