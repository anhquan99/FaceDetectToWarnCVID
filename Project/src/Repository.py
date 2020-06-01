import pyodbc
import datetime

# conn = pyodbc.connect('Driver={SQL Server};'
#                         'Server=DESKTOP-LO3H31I;'
#                         'Database=PREDICT_COVID;'
#                         'Trusted_Connection=yes;'
#                         ,autocommit=True)
# cursor = conn.cursor()
# cursor.fast_executemany = True
# sql = "INSERT INTO PREDICTION (REF, OTHER, PREDICT_PER, AT_TIME)  VALUES (?,?,?,?)"
# params = []
# params.append(("name1","name2",3.0,datetime.datetime.now()))
# params.append(("name1","name2",4.0,datetime.datetime.now() + datetime.timedelta(0,3)))
# params.append(("name1","name2",5.0,datetime.datetime.now() + datetime.timedelta(0,4)))
# cursor.executemany(sql, params)

def addPredictionToDatabase(cursor, analyzedFacesArr):
    sql = "INSERT INTO PREDICTION (REF, OTHER, PREDICT_PER, AT_TIME) VALUES (?,?,?,?)"
    params = []
    for i in analyzedFacesArr:
        params.append((i.ref, i.other, i.percentage, datetime.datetime.now()))
    cursor.executemany(sql, params)