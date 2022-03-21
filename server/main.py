"""Create a database for the team data for each user"""
import sqlite3
import socket
import threading
import chat.chat_server as chat


sqliteConnection = sqlite3.connect('teamData.db', check_same_thread=False)
dataCursor = sqliteConnection.cursor()
dataCursor.execute("""
CREATE TABLE IF NOT EXISTS 
teamData (userID int NOT NULL,team string,drivers,cash, UNIQUE(userID), PRIMARY KEY (userID));
""")  #Creates table in the format [userID,team,drivers]


def create_driver_points():
  from points import points_recorder as pr
  pr.get_drivers()
  pr.get_race_data()
  pr.split_driver_points()


from login import network as net


def main():
  """Create server connection"""
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('localhost', 9999))
  s.listen(5)
  print('Server started')
  """Create a thread for each client"""
  while True:
    client_socket, address = s.accept()
    print(f'Connection from {address} has been established')
    client = threading.Thread(target=handle_client, args=(client_socket,))  # create a thread for each client
    client.start()
    print(f'Thread for {address} has been created')
    client.join()
    print(f'Thread for {address} has been joined')
    sqliteConnection.commit() # save changes to the database


def handle_client(client_socket):
  user = net.handle_client_login(client_socket)
  sqliteConnection.commit()


def save_team(userID, constructor, drivers, spare_cash):
  """Save the team data to the database"""
  """IF DATA EXISTS, UPDATE IT"""
  dataCursor.execute(f'INSERT OR REPLACE INTO teamData (userID, team, drivers, cash) VALUES ({userID}, "{constructor}", "{drivers}", {spare_cash})')
  sqliteConnection.commit()
  return True


def return_team(userID):
  """Return the team data from the database"""
  """IF DATA EXISTS, RETURN IT"""
  data = dataCursor.execute(f'SELECT team, drivers, cash FROM teamData WHERE userID = {userID}').fetchall()
  print(data)
  return data

def chat_server():
  """Create server connection"""
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('localhost', 9988))
  s.listen(5)
  print('Chat Server started')
  """Create a thread for each client"""
  while True:
    client_socket, address = s.accept()
    client = threading.Thread(target=chat.handle_client, args=(client_socket,))  # create a thread for each client
    client.start()
    client.join()
    print(f'Chat Connection from {address} has been established, started, and joined')

if __name__ == '__main__':
  try:
    create_driver_points()
  except SyntaxError:
    print('API Offline')
  '''Start chat server'''
  threading.Thread(target=chat_server).start()
  '''Start main server'''
  main()
  sqliteConnection.commit()  # save changes to the database






