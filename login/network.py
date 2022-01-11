import sqlite3
from argon2 import PasswordHasher
ph = PasswordHasher()
sqliteConnection = sqlite3.connect('logins.db')
cursor = sqliteConnection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS logins (username string,hashpass string);")
cursor.execute(f'INSERT INTO logins VALUES ("test", "{ph.hash("teststring")}");')
#cursor.execute("""INSERT INTO logins VALUES ("tea", "9-q809vjwcewxw");""")

print(cursor.execute("SELECT * from logins").fetchall())
class Account:
  def __init__(self,username):
    self.username = username
    self.password_hash = str(cursor.execute(f'SELECT hashpass From logins WHERE username="{username}"').fetchall()[0]).split("'")[1]
  def check_pass(self, given_pass):
    if ph.verify(self.password_hash, given_pass):
      return True
    else:
      return False

print(Account('test').check_pass("teststring"))
sqliteConnection.commit()
sqliteConnection.close()