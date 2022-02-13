#Points given for tasks
assign_points={
  'DriverPoints':{
    'Race':{
      'Results':{
        '1':25,
        '2':18,
        '3':15,
        '4':12,
        '5':10,
        '6':8,
        '7':6,
        '8':4,
        '9':2,
        '10':1,
        'F':-25,  #F,D,W,R,N is DNF
        'D':-25,
        'W':-25,
        'R':-25,
        'N':-25
      },
      'fLap':1,   #Fastest Lap
      'PGFG':1,   #Points per Position gained From grid
      'PLFG':-1,  #Points per Position lost From grid
      'FAT':3,    #Finished above teammate
      'FBT':-3,   #Finished below teammate
    },
    'Qualifying':{
      'Results':{
        '1':3,
        '2':2,
        '3':1,
      },
      'RQ2':5,    #Reached Q2
      'RQ3':5,    #Reached Q3
      'QBT':-3,    #Quallified Below Teammate
      'QAT':3    #Quallified Above Teammate
    }
    },
  'Constructor':{
    'Race':{
      'Results':{
        '1':25+3,
        '2':18+3,
        '3':15+3,
        '4':12+3,
        '5':10+3,
        '6':8+3,
        '7':6+3,
        '8':4+3,
        '9':2+3,
        '10':1+3,
        'F':-25,  #F,D,W,R,N is DNF
        'D':-25,
        'W':-25,
        'R':-25,
        'N':-25
      },
    'fLap':1,     #Fastest Lap
    'PGFG':1,     #Points per Position gained From grid
    'PLFG':-1,    #Points per Position lost From grid
    },
    'Qualifying':{
      'Results':{
        '1':3,
        '2':2,
        '3':1,
      },
      'RQ2':5,   #DriverReached Q2
      'RQ3':5,   #Driver Reached Q3
      'BQ3':3,   #Both drivers reach Q3
      }
    }
  }