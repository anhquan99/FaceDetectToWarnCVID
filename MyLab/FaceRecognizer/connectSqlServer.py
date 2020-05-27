import pyodbc
conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=DESKTOP-LO3H31I;'
                        'Database=PHOTO_FORUM;'
                        'Trusted_Connection=yes;'
                        )
cursor = conn.cursor()
cursor.execute('SELECT * FROM  dbo.PHOTO_USER')
for row in cursor:
    print(row)