import MySQLdb
import json

def getPassword():
    with open(".\config.json") as json_data_file:
        data = json.load(json_data_file)
    return data["Database"]["Password"]


db = MySQLdb.connect(\
    host = "localhost", \
    user = "root", \
    passwd = "Xebec3Psy1Octo27?", \
    db = "FIT_Community", \
    charset = 'UTF8')

cursor = db.cursor()


cursor.execute(\
    'INSERT INTO STUDENT(BrojIndexa, Username, ImePrezime, Discrimintaor) \
     VALUES("IB170097", "PancakeAlcehmist", "Enis Mulić", "8165")')
cursor.execute('SELECT * FROM Student')
print(cursor.fetchone()[3])

