import requests #import needed modules
import ast
def get_drivers():
  data = requests.get('http://ergast.com/api/f1/drivers.json?limit=1900&offset=30')
  drivers = ast.literal_eval(data.content.decode())['MRData']['DriverTable']['Drivers']
  detail_driver_list = []
  file = open('drivers.txt', 'w+')
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

def get_race_data():
  from datetime import date
  for year in range(1950,date.today().year+1):  #Cycle through all years of f1
    total_races_in_year = ast.literal_eval(requests.get(f'http://ergast.com/api/f1/{year}.json').content.decode())['MRData']['total'] #Get all rounds in the year
    for race in range(1,int(total_races_in_year)+1):  #Cycle through all the rounds in the year
      race_data = ast.literal_eval(requests.get(f'http://ergast.com/api/f1/{year}/{race}/results.json').content.decode())  #Get the race data 
      quali_data = ast.literal_eval(requests.get(f'http://ergast.com/api/f1/{year}/{race}/qualifying.json').content.decode())  #Get the quali data
      assign_driver_points(race_data, quali_data)

def assign_driver_points(rData, qData): #use race data to assign points to the driver
  #print(len(rData['MRData']['RaceTable']['Races'][0]['Results']))
  for driver in rData['MRData']['RaceTable']['Races'][0]['Results']:
    driver_id = driver['Driver']['driverId']
    finish_position = driver['position']
    grid_position = driver['grid']
    constructor = driver['Constructor']['name']
    try: fastest_lap_position = driver['FastestLap']['rank']
    except KeyError: fastest_lap_position = 22
    driver_points = get_race_points(finish_position ,grid_position ,constructor ,teammate_position , fastest_lap_position)

def get_race_points(fPos, gPos, team, teammatePos, fLapPos): #Get all data required and create
  points = 0
  from point_distribution import assign_points
  try: points = points + assign_points['DriverPoints']['Race']['Results'][fPos] #add points for finishing finishing top 10 or minus 25 for not finishing
  except KeyError: points = 0
  points = points + ((int(gPos)-int(fPos)*assign_points['DriverPoints']['Race']['PGFG'])) #add points for position gained from grid
  if fLapPos == 1: points = points + assign_points['DriverPoints']['Race']['fLap']  #add points for achiving fastest lap
  if fPos > teammatePos: points = points + assign_points['DriverPoints']['Race']['FAT'] #add points for finishing above teammate
  elif fPos < teammatePos: points = points + assign_points['DriverPoints']['Race']['DBT'] #add points for finishing below teammate
  
  return points



get_drivers()
get_race_data()
