import socket

class server():
  def __init__(self):
    host = 'localhost'
    port = 9999
    serversocket = socket.socket(
      socket.AF_INET, socket.SOCK_STREAM) 


class points():
  def __init__(self):
    from points import points_recorder as pr
    pr.get_drivers()
    pr.get_race_data()
    

points()
