import pyodbc
# соединение
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\den-b\Documents\python\kurs_3\kursach_bd\kursovik.accdb;')
curs = conn.cursor()
time_st='16:30'
curs.execute("SELECT seat.Number_row, seat.Number_seat_in_row \
FROM hall INNER JOIN (film INNER JOIN ([session] INNER JOIN (seat INNER JOIN sold_ticket ON seat.ID_seat = sold_ticket.ID_seat) \
    ON session.ID_session = sold_ticket.ID_session) \
        ON film.ID_film = session.ID_film) \
            ON (hall.ID_hall = session.ID_hall) \
                AND (hall.ID_hall = seat.ID_hall) \
                    WHERE ((session.Start_time)=?) AND ((film.Name_film)='Бегущий по лезвию 2049') AND ((session.Date_session)='27.05.2020') AND ((hall.Size_hall)='малый') \
                        GROUP BY seat.Number_row, seat.Number_seat_in_row;", (time_st))
tickets=[]
#for row in curs.fetchall():
#    tickets[0].append(row[0])
#    tickets[1].append(row[1])

row = curs.fetchone()
while row:
    tickets.append(row)
    row = curs.fetchone()

#for row in curs.fetchall():
#    for elem in row:
#        tickets.append(elem)
print(tickets)
curs.close()
#print(tickets)
#hall=[[0 for i in range(5)] for j in range(4)]
def get_hall(row, seats_in_row):
    return([[0 for i in range(seats_in_row)] for j in range(row)])
def taken_places_in_hall(tickets, hall):
    for i in (tickets):
        hall[i[0]-1][i[1]-1]=1

#for i in range(len(hall)):  
#    print(hall[i])
    
type="малый"

def make_matrix(type):
    if type=="малый":
        hall=get_hall(4,5)
        taken_places_in_hall(tickets, hall)
        for i in range((len(hall[0])-1), 0, -1):
            hall[0][i],hall[1][i]=hall[0][i-1],hall[1][i-1]
        hall[0][0],hall[1][0]=None, None
        for i in range(len(hall)):  
            print(hall[i])
make_matrix(type)