import sqlite3
import time
import ast, requests
from argon2 import PasswordHasher
import socket
import threading, json
from main import save_team, return_team

ph = PasswordHasher()
sqliteConnection = sqlite3.connect('login/logins.db', check_same_thread=False)
cursor = sqliteConnection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS logins (userID ,username string,hashpass string, UNIQUE(userID), PRIMARY KEY (userID));")
#cursor.execute(f'INSERT INTO logins VALUES (1,"test", "{ph.hash("teststring")}");')
print(cursor.execute("SELECT * FROM logins").fetchall())

class Account:
  def __init__(self,username):
    self.username = username
    try:
      if str(cursor.execute(f'SELECT username FROM logins WHERE username="{self.username}"').fetchall()[0]).split("'")[1] != None:  # if username exists
        self.account = True
        self.password_hash = str(cursor.execute(f'SELECT hashpass FROM logins WHERE username="{username}"').fetchall()[0]).split("'")[1]
    except IndexError:
      self.account = False

  def valid_account(self):
    return self.account

  def check_pass(self, given_pass):
    try:
      if ph.verify(self.password_hash, given_pass):
        return True
    except Exception:
      return [False,'Invalid Password']

  def create_record(self, password):
    id = 0
    while True:
      try:
        cursor.execute(f'INSERT INTO logins (userID, username, hashpass) VALUES({id},"{self.username}","{password}")')
        print('Account Created')
        break
      except Exception:
        id = id + 1


def login(account_username, password):  
  user = Account(account_username)
  if user.valid_account():
    result = user.check_pass(password)
  else:
    result = [False,'Invalid Username']
  return result

def register(username, password):
  user = Account(username)
  if user.valid_account() != True:
    user.create_record(ph.hash(password))
    return True
  else:
    return [False, 'Username Occupied']


def handle_client_login(client_socket):
  """create a new thread for each client and determine if the client is a new user or returning user so they can login or register"""
  request = client_socket.recv(1024).decode()
  request = request.split('-~-')
  print(request)
  if request[0] == 'register':
    """request in form [register, username, password]"""
    result = register(request[1], request[2])
    sqliteConnection.commit()   # commit changes to database
    client_socket.send(str(result).encode())
  elif request[0] == 'login':
    """request in form [login, username, password]"""
    result = login(request[1], request[2])
    print(result)
    client_socket.send((str(result)).encode())
    if result:  # if login is successful
      return True
  elif request[0] == 'save_team':
    """request in form [save_team, username, password, team_data, driver_data, spare_cash]"""
    if login(request[1], request[2]):  # if login is successful
      userID = cursor.execute(f'SELECT userID FROM logins WHERE username = "{request[1]}"').fetchall()[0][0]
      result = save_team(userID, request[3], request[4], request[5]) # save team
    client_socket.send(str(result).encode())
  elif request[0] == 'return_team':
    """request in form [return_team, username, password]"""
    if (login_result := login(request[1], request[2])):  # if login is successful
      userID = cursor.execute(f'SELECT userID FROM logins WHERE username = "{request[1]}"').fetchall()[0][0]
      result = return_team(userID) # return team
    else:
      result = login_result
    client_socket.send(str(result).encode())
  elif request[0] == 'return_point_data':
    # get point data from files and send to client
    team_points = open('points/team_points.json')
    driver_points = open('points/driver_points.json')
    team_points = json.load(team_points)
    driver_points = json.load(driver_points)
    client_socket.send(json.dumps([team_points, driver_points]).encode())
  elif request[0] == 'return_current_driver_and_constructors':
    # get current driver and constructor data from files and send to client
    current_drivers = open('points/current_drivers.txt', 'r')
    current_constructors = open('points/current_constructors.txt', 'r')
    current_drivers = current_drivers.read()
    current_constructors = current_constructors.read()
    client_socket.send(str([current_drivers, current_constructors]).encode())
  elif request[0] == 'get_next_race':
    try:
      data = ast.literal_eval(requests.get('https://ergast.com/api/f1/current/next.json').content.decode())
      data = data['MRData']['RaceTable']['Races'][0]  # get useful data
      race_name = data['raceName']
      date = data['date']
      time = data['time']
    except:
      race_name, date, time = 'N/A'

    client_socket.send(str([race_name, date, time]).encode())
  else:
    client_socket.send(b'Invalid Request')
  return False


def main():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('localhost', 9999))
  s.listen(5)
  """create a thread for each client"""
  while True:
    client_socket, address = s.accept()
    print(f'Connection from {address} has been established')
    client = threading.Thread(target=handle_client, args=(client_socket,))
    client.start()
    print(f'Thread for {address} has been created')
    client.join()
    sqliteConnection.commit()




#sqliteConnection.close()