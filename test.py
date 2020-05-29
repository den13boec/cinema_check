import pyodbc
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\den-b\Documents\python\kurs_3\kursach_bd\kursovik.accdb;')
curs = conn.cursor()
curs.execute("SELECT film.Name_film FROM film;")
result_query=[]
row = curs.fetchone() 
while row:
    result_query.append(row[0])
    row = curs.fetchone()
print(result_query)