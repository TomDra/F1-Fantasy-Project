import requests #import needed modules
import ast
from threading import Thread, Lock
import queue
from datetime import date
global directory
directory = 'points/'
lock = Lock()

def get_drivers():
  data = requests.get('http://ergast.com/api/f1/drivers.json?limit=1900&offset=30')
  drivers = ast.literal_eval(data.content.decode())['MRData']['DriverTable']['Drivers']
  detail_driver_list = []
  file = open(f'{directory}drivers.txt', 'w+')
  for driver in drivers:
    try:
      driver_id = driver['driverId']
      full_name = f"{driver['givenName']} {driver['familyName']}"
      nationality = driver['nationality']
      DoB = driver['dateOfBirth']
      number = driver['permanentNumber']
    except Exception:
      number = 'n/a'
    detail_driver_list.append([driver_id,full_name,nationality,DoB,number])
  file.write(str(detail_driver_list))

def save_to_file(queue):
  file = open(f'{directory}raw_points.csv', 'w+')
  file.write('year,round,race name,team,team points,driver1,driver1 points,driver2,driver2 points\n') #Write titles of data
  while finished != True or queue.empty() != True:
    """Loop until queue is empty and finished == True"""
    file.write(queue.get())
  file.close()

def get_race_data():
  global q,finished
  i=1
  q = queue.Queue()
  finished = False
  """use threading to run each year in parallel"""
  threads=[]
  for year in range(1950,date.today().year+1):
      threads.append(Thread(target=year_loop, args=(year,)))
  for thread in threads:
    thread.start()
  for thread in threads:  #End all threads
    print(f"thread ending {thread}")
    thread.join()
  finished = True
  save_to_file(q) #save the queue to a file


def year_loop(year):
  #for year in range(1950,date.today().year+1):  #Cycle through all years of f1 from 1950 to the current year
  total_races_in_year = ast.literal_eval(requests.get(f'http://ergast.com/api/f1/{year}.json').content.decode())['MRData']['total'] #Get all rounds in the year
  for race in range(1,int(total_races_in_year)+1):  #Cycle through all the rounds in the year
    race_data = ast.literal_eval(requests.get(f'http://ergast.com/api/f1/{year}/{race}/results.json').content.decode())  #Get the race data
    try:
      assign_driver_points(race_data) #,quali_data)
    except IndexError as a:
      print(f"test1 {a} {year}")

def assign_driver_points(rData): #use race data to assign points to the driver
  team_dict = {}
  year = rData['MRData']['RaceTable']['Races'][0]['season'] #Get race year
  round = rData['MRData']['RaceTable']['Races'][0]['round'] #Get race number
  rName = rData['MRData']['RaceTable']['Races'][0]['raceName']  #Get race name
  #print(len(rData['MRData']['RaceTable']['Races'][0]['Results']))
  try:
    for driver in rData['MRData']['RaceTable']['Races'][0]['Results']:
      constructor = driver['Constructor']['name'] #Get drivers team
      driver_id = driver['Driver']['driverId']  #Get drivers name
      finish_position = driver['position']  #Get finish pos
      grid_position = driver['grid']   #Get starting position
      try: fastest_lap_position = driver['FastestLap']['rank']  #Get fastest lap rank
      except KeyError: fastest_lap_position = 22
      if constructor not in team_dict:  #Combines all drivers of the same teams in a dictionary
          team_dict[constructor] = []
      team_dict[constructor].append({'driver':driver_id,'fastPosition':fastest_lap_position,'gPosition':grid_position,'fPosition':finish_position}) #make a dictionary which contains all driver data needed and groups drivers by team
    for team in team_dict:
      driver1 = team_dict[team][0]
      try: driver2 = team_dict[team][1]
      except IndexError: driver2 = {'driver': 'n/a', 'fastPosition': 22, 'gPosition': '22', 'fPosition': '22'}  #If no second driver exists, use filler data
      points = get_points(driver1,driver2)  #get the driver and constructors points
      #print(team,points)
      save_points([driver1['driver'],points['driver1']],[driver2['driver'],points['driver2']],[team,points['constructor']],year,round,rName)
  except KeyError as a:
    print(a)

def save_points(driver1,driver2,team,year,round,rName): #save the points to a csv file
  if int(year) == date.today().year:
    team[1] = int(team[1])*10
    driver1[1] = int(driver1[1])*10
    driver2[1] = int(driver2[1])*10
  lock.acquire()
  q.put(f"{year},{round},{rName},{team[0]},{team[1]},{driver1[0]},{driver1[1]},{driver2[0]},{driver2[1]}\n")  #Add the data to the queue
  lock.release()

def get_points(driver1_data,driver2_data): #Get all data required to calculate points for both drivers
  drivers_data = [[int(driver1_data['fPosition']),int(driver1_data['gPosition']),int(driver1_data['fastPosition']),int(driver2_data['fPosition'])],
  [int(driver2_data['fPosition']),int(driver2_data['gPosition']),int(driver2_data['fastPosition']),int(driver1_data['fPosition'])]] #Creates a list so that all the data can be inputed into the loop
  driver_points = []
  team_points = 0
  from points import point_distribution as pd
  for i in range(0,2):  #loop twice to get both drivers points
    fPos = drivers_data[i][0] #Extract all data from the list
    gPos = drivers_data[i][1]
    fLapPos = drivers_data[i][2]
    teammatePos = drivers_data[i][3]
    points=0
    """Race Points"""
    try: 
      points = points + pd.assign_points['DriverPoints']['Race']['Results'][str(fPos)] #add points to driver for finishing finishing top 10 or minus 25 for not finishing
      team_points = team_points + pd.assign_points['Constructor']['Race']['Results'][str(fPos)] #Add points to team
    except KeyError: 
      points = 0
    points = points + ((int(gPos) - int(fPos))* pd.assign_points['DriverPoints']['Race']['PGFG']) #add points to driver for position gained from grid
    team_points = team_points + ((int(gPos) - int(fPos)) * pd.assign_points['Constructor']['Race']['PGFG'])
    if fLapPos == 1: 
      points = points + pd.assign_points['DriverPoints']['Race']['fLap']  #Add points to driver for achiving fastest lap
      team_points = team_points + pd.assign_points['Constructor']['Race']['fLap']  #Add points to team for fastest lap  
    if fPos > teammatePos: 
      points = points + pd.assign_points['DriverPoints']['Race']['FAT'] #add points for finishing above teammate
    elif fPos < teammatePos: 
      points = points + pd.assign_points['DriverPoints']['Race']['FBT'] #add points for finishing below teammate
    try:team_points = team_points + pd.assign_points['Constructor']['Race']['Results'][str(fPos)]  #Add points to team for result in race
    except KeyError: 
      pass
    """Quallifying Points"""
    try: 
      points = points + pd.assign_points['DriverPoints']['Qualifying']['Results'][gPos]  #Add driver points for qually pos
      team_points = team_points + pd.assign_points['Constructor']['Qualifying']['Results'][gPos] #Add team points for qually pos
    except KeyError: 
      pass
    if gPos <= 15:
      points = points + pd.assign_points['DriverPoints']['Qualifying']['RQ2']  #Add points for qually positions above 15
      team_points = team_points + pd.assign_points['Constructor']['Qualifying']['RQ2'] #Add team points for qually positions above 15
    if gPos <= 10:
      points = points + pd.assign_points['DriverPoints']['Qualifying']['RQ3']  #Add points for qually positions above 10
      team_points = team_points + pd.assign_points['Constructor']['Qualifying']['RQ3'] #Add team points for qually positions above 10
    driver_points.append(points)
  return {'constructor':team_points,'driver1':driver_points[0],'driver2':driver_points[1]}

def split_driver_points():
  data = open(f'{directory}raw_points.csv','r').readlines()[1:]
  teams = {}
  drivers = {}
  for line in data:
    """Convert the file data back into useful variables"""
    line = line.split(',')
    team = line[3]
    team_points = line[4]
    driver1 = line[5]
    driver1_points = line[6]
    driver2 = line[7]
    driver2_points = line[8]
    """take all points for each driver and append them to a list in a dictionary for that driver"""
    variable_set = [[driver1,driver1_points,drivers],[driver2,driver2_points,drivers],[team,team_points,teams]]
    for driver in variable_set:
      if driver[0] in driver[2]:
        driver[2][driver[0]].append(int(driver[1]))
      else:
        driver[2][driver[0]] = [int(driver[1])]
    """Add the points in the list together and replace the list with a total"""
  for team in teams:
    teams[team]=sum(teams[team])
  for driver in drivers:
    drivers[driver]=sum(drivers[driver])
  """Sort each dictionary so its easier to read"""
  drivers_sorted=dict(sorted(drivers.items(),key= lambda x:x[1]))
  teams_sorted=dict(sorted(teams.items(),key= lambda x:x[1]))
  """save the points to a json file"""
  save_final_points(drivers_sorted,'driver_points.json')
  save_final_points(teams_sorted,'team_points.json')
  print(teams_sorted)
  print(drivers_sorted)

def save_final_points(points,file):
  file = open(directory+file,'w+')
  file.write(str(points).replace("'",'"'))
  file.close

if __name__ == '__main__':
  import time
  get_drivers()
  start = time.time()
  get_race_data()
  print(f"Runtime of the program is {time.time() - start}")
  split_driver_points()


#https://ergast.com/api/f1/constructorstandings/1.json?limit=9999&offset=30
#https://ergast.com/api/f1/driverstandings/1.json?limit=9999&offset=30