import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QWidget, QGraphicsScene
from PyQt5.QtGui import QPainter, QColor, QFont, QGradient
from PyQt5 import Qt
# подключение к БД Access
import pyodbc
conn = pyodbc.connect(
    r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\den-b\Documents\python\kurs_3\kursach_bd_git\cinema_check\kursovik.accdb;')
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.nameUi()

    # Присвоение элементам графического интерфейса имен
    def nameUi(self):
        self.setWindowTitle("Кинотеатр")
        self.label_1.setText("Название фильма")
        self.label_2.setText("Дата сеанса")
        self.label_3.setText("Номер места")
        self.label_4.setText("Номер ряда")
        self.take_seat.setText("Занять место")
        self.label_5.setText("Время сеанса")
        self.take_look_seat.setText("Показать место")
        self.label_6.setText("Зал")

    # Настройки графического интерфейса
    def setupUi(self):
        self.setFixedSize(600, 820)
        # задаём центральный виджет
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        # создаём выпадающие списки
        self.comboBox_films = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_films.setGeometry(QtCore.QRect(10, 10, 311, 31))
        self.comboBox_films.setObjectName("comboBox_films")

        self.comboBox_date = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_date.setGeometry(QtCore.QRect(10, 50, 311, 31))
        self.comboBox_date.setObjectName("comboBox_date")

        self.comboBox_time = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_time.setGeometry(QtCore.QRect(10, 90, 311, 31))
        self.comboBox_time.setObjectName("comboBox_time")

        self.comboBox_hall = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_hall.setGeometry(QtCore.QRect(10, 130, 311, 31))
        self.comboBox_hall.setObjectName("comboBox_hall")

        # создаём подписи
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(330, 10, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(330, 50, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(110, 170, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(330, 170, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(330, 90, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(330, 130, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        # создаём textboxы
        self.chosen_seat = QtWidgets.QLineEdit(self.centralwidget)
        self.chosen_seat.setGeometry(QtCore.QRect(10, 170, 91, 31))
        self.chosen_seat.setObjectName("chosen_seat")

        self.chosen_row = QtWidgets.QLineEdit(self.centralwidget)
        self.chosen_row.setGeometry(QtCore.QRect(230, 170, 91, 31))
        self.chosen_row.setObjectName("chosen_row")

        # создаём кнопки
        self.take_look_seat = QtWidgets.QPushButton(self.centralwidget)
        self.take_look_seat.setGeometry(QtCore.QRect(10, 210, 150, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.take_look_seat.setFont(font)
        self.take_look_seat.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.take_look_seat.setObjectName("take_look_seat")

        self.take_seat = QtWidgets.QPushButton(self.centralwidget)
        self.take_seat.setGeometry(QtCore.QRect(230, 210, 150, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.take_seat.setFont(font)
        self.take_seat.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.take_seat.setObjectName("take_seat")

        # создаём поле для вывода изображения кинозала (графическое поле)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 250, 580, 550))
        self.graphicsView.setObjectName("graphicsView")

        # задаём шрифт для textbox
        self.chosen_seat.setFont(QtGui.QFont(
            "Consolas", 12, QtGui.QFont.Light))
        self.chosen_row.setFont(QtGui.QFont("Consolas", 12, QtGui.QFont.Light))

        # создаём соединение с БД
        self.curs = conn.cursor()

        # запрос на получение фильмов
        result_films = self.do_query(
            "SELECT film.Name_film FROM film;", False, None)
        
        # заполняем выпадающий список фильмов
        self.comboBox_films.addItems(result_films)

        # выбран фильм
        self.comboBox_films.activated.connect(self.chose_film)

        # выбрана дата
        self.comboBox_date.activated.connect(self.chose_date)

        # выбрано время
        self.comboBox_time.activated.connect(self.chose_time)

        # выбран зал
        self.comboBox_hall.activated.connect(self.make_matrix_and_hall)

        # кнопка занять место
        self.take_seat.clicked.connect(self._take_seat)

        # кнопка просмотреть место
        self.take_look_seat.clicked.connect(self.look_seat)

        # нарисован ли зал
        self.graph_check = False

    # функция выполняющая SQL запрос к БД
    def do_query(self, line_query, multi, conditions_query):
        if conditions_query:
            self.curs.execute(line_query, conditions_query)
        elif not conditions_query:
            self.curs.execute(line_query)
        result_query = []
        row = self.curs.fetchone()
        if multi:
            while row:
                result_query.append(row)
                row = self.curs.fetchone()
        elif not multi:
            while row:
                result_query.append(row[0])
                row = self.curs.fetchone()
        return result_query

    # отрисовка зала
    def show_places(self):
        self.graph_check=True
        #создаём новую сцену чтобы сбросить фокус
        self.my_scene = QGraphicsScene() 
        self.graphicsView.setScene(self.my_scene)   
        # задаём размер квадратов
        size=25
        x=self.hall_for_show
        # рисуем рамку зала
        color = Qt.Qt.black
        size_sq = QtCore.QRectF(QtCore.QPointF(-size, -(size+5)*2), QtCore.QSizeF((len(x[1])+2)*size, (len(x)+2)*(size+5)))
        self.my_scene.addRect(size_sq, Qt.QPen(color), Qt.QBrush(Qt.Qt.lightGray))
        # рисуем экран
        color = Qt.Qt.cyan
        size_sq = QtCore.QRectF(QtCore.QPointF(0, -(size+5)*2), QtCore.QSizeF((len(x[1]))*size, size/2))
        self.my_scene.addRect(size_sq, Qt.QPen(Qt.Qt.gray), Qt.QBrush(color))
        # подпись для экрана
        text=self.my_scene.addText("Экран", font=QtGui.QFont("Times", 8, QtGui.QFont.Bold))
        text.setPos( ((len(x[1]))*(size - 2))/2,-(size+5)*3)
        # рисуем места
        for i in range(len(x)):
            text=self.my_scene.addText(("Ряд " + str(i+1)), font=QtGui.QFont("Times", 8, QtGui.QFont.Bold))
            text.setPos((len(x[i])+2)*size,i*(size+5))
            number_seat=0
            for j in range(len(x[i])):
                if x[i][j]=="0":
                    color = Qt.Qt.green
                    number_seat=number_seat+1
                elif x[i][j]=="1":
                    color = Qt.Qt.red
                    number_seat=number_seat+1
                else:
                    continue
                size_sq = QtCore.QRectF(QtCore.QPointF(j*size, i*(size+5)), QtCore.QSizeF(size, size))
                self.my_scene.addRect(size_sq, Qt.QPen(color), Qt.QBrush(color))
                text=self.my_scene.addText(str(number_seat), font=QtGui.QFont("Times", 8, QtGui.QFont.Bold))
                text.setPos(j*size, i*(size+5))

    # событие при выходе
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Выход из приложения', 'Вы уверены, что хотите выйти?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.curs.close()
            conn.close()
            event.accept()
        else:
            event.ignore()

    # выбран фильм
    def chose_film(self):
        # очищаем нарисованный зал, если он был нарисован
        if self.graph_check:
            self.my_scene.clear()
            self.graph_check = False
        # очищаем выпадающие списки и текстбоксы
        self.chosen_row.clear()
        self.chosen_seat.clear()
        self.comboBox_date.clear()
        self.comboBox_time.clear()
        self.comboBox_hall.clear()
        film = self.comboBox_films.currentText()
        query = "SELECT session.Date_session \
            FROM film INNER JOIN [session] \
                ON film.ID_film = session.ID_film \
                WHERE ((film.Name_film)=?) \
                    GROUP BY session.Date_session;"
        # запрос на получение дат
        result_dates = self.do_query(query, False, film)
        # заполняем выпадающий список дат
        self.comboBox_date.addItems(result_dates)

    # выбрана дата
    def chose_date(self):
        # очищаем нарисованный зал, если он был нарисован
        if self.graph_check:
            self.my_scene.clear()
            self.graph_check = False
        self.chosen_row.clear()
        self.chosen_seat.clear()
        self.comboBox_time.clear()
        self.comboBox_hall.clear()
        query = "SELECT session.Start_time \
            FROM film INNER JOIN [session] \
                ON film.ID_film = session.ID_film \
                WHERE (((film.Name_film)=?) \
                    AND ((session.Date_session)=?)) \
                    GROUP BY session.Start_time \
                        ORDER BY session.Start_time;"
        film = self.comboBox_films.currentText()
        date = self.comboBox_date.currentText()
        # запрос на получение времени сеансов
        result_times = self.do_query(query, False, (film, date))
        # заполняем выпадающий список времени сеанса
        self.comboBox_time.addItems(result_times)

    # выбрано время
    def chose_time(self):
        # очищаем нарисованный зал, если он был нарисован
        if self.graph_check:
            self.my_scene.clear()
            self.graph_check = False
        self.chosen_row.clear()
        self.chosen_seat.clear()
        self.comboBox_hall.clear()
        query = "SELECT hall.Size_hall \
            FROM hall INNER JOIN (film INNER JOIN [session] \
                ON film.ID_film = session.ID_film) \
                ON hall.ID_hall = session.ID_hall \
                WHERE (((session.Start_time)=?) \
                    AND ((film.Name_film)=?) \
                        AND ((session.Date_session)=?)) \
                    GROUP BY hall.Size_hall;"
        film = self.comboBox_films.currentText()
        date = self.comboBox_date.currentText()
        time = self.comboBox_time.currentText()
        # запрос на получение времени сеансов
        result_hall = self.do_query(query, False, (time, film, date))
        # заполняем выпадающий список времени сеанса
        self.comboBox_hall.addItems(result_hall)

    # запрос к БД, по нему составление матрицы занятых мест и матрицы мест в зале и вызов функции отрисовки
    def make_matrix_and_hall(self):
        if self.graph_check:
            self.my_scene.clear()
            self.graph_check = False
        self.chosen_row.clear()
        self.chosen_seat.clear()
        query = "SELECT seat.Number_row, seat.Number_seat_in_row \
            FROM hall INNER JOIN (film INNER JOIN ([session] INNER JOIN (seat INNER JOIN sold_ticket ON seat.ID_seat = sold_ticket.ID_seat) \
                ON session.ID_session = sold_ticket.ID_session) \
                    ON film.ID_film = session.ID_film) \
                        ON (hall.ID_hall = session.ID_hall) \
                            AND (hall.ID_hall = seat.ID_hall) \
                                WHERE ((session.Start_time)=?) \
                                    AND ((film.Name_film)=?) \
                                        AND ((session.Date_session)=?) \
                                            AND ((hall.Size_hall)=?) \
                                                GROUP BY seat.Number_row, seat.Number_seat_in_row;"
        film = self.comboBox_films.currentText()
        date = self.comboBox_date.currentText()
        time = self.comboBox_time.currentText()
        type_hall = self.comboBox_hall.currentText()
        # запрос на получение списка занятых мест в зале на сеанс
        tickets = self.do_query(query, True, (time, film, date, type_hall))
        hall = []
        #self.matrix_places = []
        if type_hall == "малый":            
            hall = self.get_matrix(4, 5)
            self.taken_places(tickets, hall)            
            # вход в зал в матрице
            self.make_enter_small_medium(hall)
            hall[0][0], hall[1][0] = 2, 2
        elif type_hall=="средний":
            hall = self.get_matrix(7, 6)
            self.taken_places(tickets, hall)            
            # вход в зал в матрице
            self.make_enter_small_medium(hall)
            hall[0][0], hall[1][0] = 2, 2
            for i in range((len(hall[6])-2), 0, -1):
                hall[6][i] = hall[6][i-1]
            hall[6][0], hall[6][5] = 2, 2
        elif type_hall=="большой":
            hall = self.get_matrix(9, 8)
            self.taken_places(tickets, hall)            
            # вход в зал в матрице
            hall[4][4],hall[4][5],hall[4][6],hall[4][7]=2, 2, 2, 2            
            for i in range((len(hall[8])-2), 0, -1):
                hall[8][i] = hall[8][i-1]
                hall[0][i]=hall[0][i-1]
            hall[8][0], hall[8][7] = 2, 2    
            hall[0][0], hall[0][7] = 2, 2     
        self.hall_for_show=[]
        self.matrix_taken_places=[]
        # создаём матрицу зала, которую будем использовать для рисования:hall_for_show
        # и матрицу занятых мест, которую будем использовать для проверки занимаемого места:matrix_taken_places
        for i in hall:
            line = ' '.join([str(elem) for elem in i])
            self.hall_for_show.append(line)
            line=[]
            for j in i:                
                if j==0 or j==1:
                    line.append(j)
            self.matrix_taken_places.append(line)
        self.show_places()
        
    # получение матрицы зала, заполненной 0 определённого размера
    def get_matrix(self, row, seats_in_row):
        return([[0 for i in range(seats_in_row)] for j in range(row)])

    # заполнение матрицы занятыми местами
    def taken_places(self, tickets, hall):
        for i in (tickets):
            hall[i[0]-1][i[1]-1] = 1

    # сдвиг для входа в малый и средний залы
    def make_enter_small_medium(self, hall):
        for i in range((len(hall[0])-1), 0, -1):
            hall[0][i], hall[1][i] = hall[0][i-1], hall[1][i-1]

    # проверка места: занято ли оно, имееется ли вообще в зале
    def check_seat(self):
        if self.check_input():
            i = int(self.chosen_row.text())
            j = int(self.chosen_seat.text())
            if self.is_valid_input(i, j):
                i = i-1
                j = j-1
                if (self.matrix_taken_places[i][j]) == 1:
                    # место занято
                    QMessageBox(1, "Упс...", "Место уже занято!").exec_()
                    return 0
                else:
                    return 1
            else:
                # если не правильно записан номер ряда или место
                QMessageBox(2, "Ошибка!", "Такого места нет!").exec_()
                return 0

    # просмотр места, но не занятие
    def look_seat(self):        
        if self.check_seat():
            self.my_scene.clear()
            self.show_places()
            i = int(self.chosen_row.text())-1
            j = int(self.chosen_seat.text())-1
            # место свободно
            # закрашиваем место жёлтым цветом
            x = self.hall_for_show
            for m in range(len(x)):
                number_seat = 0
                for n in range(len(x[m])):
                    if x[m][n] == "0" or x[m][n] == "1":
                        number_seat = number_seat+1
                    if (number_seat-1) == j and m == i:
                        size_sq = QtCore.QRectF(QtCore.QPointF(
                            n*25, m*(25+5)), QtCore.QSizeF(25, 25))
                        self.my_scene.addRect(size_sq, Qt.QPen(
                            Qt.Qt.yellow), Qt.QBrush(Qt.Qt.yellow))
                        text = self.my_scene.addText(
                            str(number_seat), font=QtGui.QFont("Times", 8, QtGui.QFont.Bold))
                        text.setPos(n*25, m*(25+5))
                        return
            
    # проверка есть ли такое место
    def is_valid_input(self, row, seat):
        if len(self.matrix_taken_places) >= row > 0:
            if len(self.matrix_taken_places[row-1]) >= seat > 0:
                return True
        return False

    # занятие места
    def _take_seat(self):
        if self.check_seat():
            i = int(self.chosen_row.text())
            j = int(self.chosen_seat.text())
            # место свободно
            # делаем запрос на добавление занятого места в БД
            QMessageBox(1, "Успешное бронирование", f"Вы успешно забронировали место в зале: ряд {i}, место {j}").exec_()
            query="SELECT seat.ID_seat \
                FROM hall INNER JOIN seat ON hall.ID_hall = seat.ID_hall \
                    WHERE (((seat.Number_row)=?) \
                        AND ((seat.Number_seat_in_row)=?) \
                            AND ((hall.Size_hall)=?)) \
                        GROUP BY seat.ID_seat;"
            numb_row=i
            numb_seat=j
            type_hall = self.comboBox_hall.currentText()
            id_seat = self.do_query(query, False, (i, j, type_hall))
            query="SELECT session.ID_session \
                FROM hall INNER JOIN (film INNER JOIN [session] \
                    ON film.ID_film = session.ID_film) \
                        ON hall.ID_hall = session.ID_hall \
                    WHERE (((film.Name_film)=?) \
                        AND ((hall.Size_hall)=?) \
                            AND ((session.Start_time)=?) \
                                AND ((session.Date_session)=?)) \
                        GROUP BY session.ID_session;"
            film = self.comboBox_films.currentText()
            date = self.comboBox_date.currentText()
            time = self.comboBox_time.currentText()
            id_session = self.do_query(query, False, (film, type_hall, time, date))
            self.curs.execute('''INSERT INTO sold_ticket ( [ID_session], [ID_seat] ) \
                VALUES (?, ?);''', (id_session[0], id_seat[0]))
            conn.commit()
            self.make_matrix_and_hall()

    # проверка на ввод всех данных
    def check_input(self):
        if (self.chosen_seat.text() == ""
            or self.chosen_row.text() == ""
            or self.comboBox_films.currentText() == ""
            or self.comboBox_time.currentText() == ""
                or self.comboBox_date.currentText() == ""
                or self.comboBox_hall.currentText() == ""
                or not self.graph_check):
            QMessageBox(
                2, "Ошибка!", "Введите все данные до выбора места").exec_()
            return 0
        # проверка числа ли введены в текстбокс
        elif ((not (self.chosen_seat.text()).isnumeric())
              or (not (self.chosen_row.text()).isnumeric())):
            QMessageBox(2, "Ошибка!", "В поля вводится только ЧИСЛА").exec_()
            return 0
        else:
            return 1

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_w = main_window()
    main_w.show()
    sys.exit(app.exec_())
