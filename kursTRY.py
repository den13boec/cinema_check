import sys
import codecs # русские буквы в txt файле
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QWidget, QGraphicsScene
from PyQt5.QtGui import QPainter, QColor, QFont, QGradient
from PyQt5 import Qt

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
    
    # Присвоение элементам графического интерфейса имен
    def nameUi(self, MainWindow):
        MainWindow.setWindowTitle("Кинотеатр")
        self.label_1.setText("Название фильма")
        self.label_2.setText("Дата сеанса")
        self.label_3.setText("Номер места")
        self.label_4.setText("Номер ряда")
        self.take_seat.setText("Занять место")
        self.label_5.setText("Время сеанса и зал")
        self.take_look_seat.setText("Показать место")
        
    # Настройки графического интерфейса       
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(600, 820)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox_films = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_films.setGeometry(QtCore.QRect(10, 10, 311, 31))
        self.comboBox_films.setObjectName("comboBox_films")
        self.comboBox_date = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_date.setGeometry(QtCore.QRect(10, 50, 311, 31))
        self.comboBox_date.setObjectName("comboBox_date")
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
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 250, 580, 550))
        self.graphicsView.setObjectName("graphicsView")
        self.chosen_seat = QtWidgets.QLineEdit(self.centralwidget)
        self.chosen_seat.setGeometry(QtCore.QRect(10, 170, 91, 31))
        self.chosen_seat.setObjectName("chosen_seat")
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
        self.chosen_row = QtWidgets.QLineEdit(self.centralwidget)
        self.chosen_row.setGeometry(QtCore.QRect(230, 170, 91, 31))
        self.chosen_row.setObjectName("chosen_row")
        self.take_seat = QtWidgets.QPushButton(self.centralwidget)
        self.take_seat.setGeometry(QtCore.QRect(230, 210, 150, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.take_seat.setFont(font)
        self.take_seat.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.take_seat.setObjectName("take_seat")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(330, 90, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.comboBox_time = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_time.setGeometry(QtCore.QRect(10, 90, 311, 31))
        self.comboBox_time.setObjectName("comboBox_time")      
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 512, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.take_look_seat = QtWidgets.QPushButton(self.centralwidget)
        self.take_look_seat.setGeometry(QtCore.QRect(10, 210, 150, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.take_look_seat.setFont(font)
        self.take_look_seat.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.take_look_seat.setObjectName("take_look_seat")
        
        # задаём шрифт для textbox
        self.chosen_seat.setFont(QtGui.QFont("Consolas", 12, QtGui.QFont.Light))
        self.chosen_row.setFont(QtGui.QFont("Consolas", 12, QtGui.QFont.Light))
        
        self.nameUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)        

        # заполняем выпадающий список фильмов
        self.comboBox_films.addItems(os.listdir("Фильмы"))
        # выбран фильм
        self.comboBox_films.activated.connect(self.chose_film)
        # выбрана дата
        self.comboBox_date.activated.connect(self.chose_date)

        # кнопка занять место
        self.take_seat.clicked.connect(self.check_seat)
        
        # кнопка просмотреть место
        self.take_look_seat.clicked.connect(self.check_look_seat)
                
        # выбрано время и зал-показать зал
        self.comboBox_time.activated.connect(self.show_places)
        
        # нарисован ли зал
        self.graph_check=False
        
    # РИСОВАНИЕ 
    def show_places(self):
        self.graph_check=True
        #создаём новую сцену чтобы сбросить фокус
        self.my_scene = QGraphicsScene() 
        self.graphicsView.setScene(self.my_scene)   
        # задаём размер квадратов        
        size=20
        # читаем файл мест      
        x=self.read_file()
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
         
    # выбран фильм
    def chose_film(self):
        if self.graph_check==True:
            self.my_scene.clear()
            self.graph_check=False
        self.chosen_row.clear()
        self.chosen_seat.clear()
        self.comboBox_date.clear()
        self.comboBox_time.clear()
        # заполняем выпадающий список дат
        self.comboBox_date.addItems(os.listdir("Фильмы\\"+self.comboBox_films.currentText()))
                
    # выбрана дата
    def chose_date(self):
        if self.graph_check==True:
            self.my_scene.clear()
            self.graph_check=False
        self.chosen_row.clear()
        self.chosen_seat.clear()
        self.comboBox_time.clear()
        # получаем названия файлов
        file_names=os.listdir("Фильмы\\"+self.comboBox_films.currentText() +"\\" + self.comboBox_date.currentText())
        # убираем расширение txt
        file_names = [os.path.splitext(each)[0] for each in file_names]
        self.comboBox_time.addItems(file_names)
 
    # просмотр места, но не занятие
    def check_look_seat(self):        
        if self.check_input():
            self.load_matrix()
            self.show_places()
            i = int(self.chosen_row.text())
            j = int(self.chosen_seat.text()) 
            if self.is_valid_input(i, j):
                i=i-1
                j=j-1
                if (self.matrix[i][j]) == "1":
                    # место занято
                    QMessageBox(1, "Упс...", "Место уже занято!").exec_()
                else:
                    # место свободно
                    # закрашиваем место жёлтым цветом     
                    x=self.read_file()
                    for m in range(len(x)):
                        number_seat=0
                        for n in range(len(x[m])):
                            if x[m][n]=="0" or x[m][n]=="1":
                                number_seat=number_seat+1
                            if (number_seat-1)==j and m==i:
                                size_sq = QtCore.QRectF(QtCore.QPointF(n*20, m*(20+5)), QtCore.QSizeF(20, 20))
                                self.my_scene.addRect(size_sq, Qt.QPen(Qt.Qt.yellow), Qt.QBrush(Qt.Qt.yellow))
                                text=self.my_scene.addText(str(number_seat), font=QtGui.QFont("Times", 8, QtGui.QFont.Bold))
                                text.setPos(n*20, m*(20+5))
                                return                            
            else:
                # если не правильно записан номер ряда или место            
                QMessageBox(1, "Ошибка!", "Такого места нет!").exec_()
                return    

    # чтение файла
    def read_file(self):
        path = "Фильмы\\" + self.comboBox_films.currentText() +"\\" + \
            self.comboBox_date.currentText() + "\\" + self.comboBox_time.currentText()+".txt"
        file = codecs.open(path, encoding='utf-8', mode='r')
        x = file.read().splitlines()
        file.close()
        return x

    # перевод матрицы
    def matrix_to_text(self, text_modify):
        i = 0
        for id, line in enumerate(text_modify):
            j = 0
            line_arr = line.split(",")
            for index, symbol in enumerate(line_arr):
                if symbol != "_":
                    line_arr[index] = self.matrix[i][j]
                    j += 1
            text_modify[id] = ",".join(line_arr)
            i = i + 1
        return "\n".join(text_modify)

    # сохранение изменённой матрицы
    def save_matrix(self):
        path = "Фильмы\\" + self.comboBox_films.currentText() +"\\" + \
                        self.comboBox_date.currentText() + "\\" + self.comboBox_time.currentText()+".txt"
        text = self.read_file()        
        file = codecs.open(path, encoding='utf-8', mode='w')
        file.write(self.matrix_to_text(text))
        file.close()

    # проверка есть ли такое место
    def is_valid_input(self, row, seat):        
        if len(self.matrix) >= row > 0:
            if len(self.matrix[row-1]) >= seat > 0:
                return True
        return False

    # занятие места
    def check_seat(self):                
        if self.check_input():
            self.load_matrix()
            i = int(self.chosen_row.text())
            j = int(self.chosen_seat.text()) 
            if self.is_valid_input(i, j):
                i=i-1
                j=j-1
                if (self.matrix[i][j]) == "1":
                    # место занято
                    QMessageBox(1, "Упс...", "Место уже занято!").exec_()
                else:
                    # место свободно
                    # пишем сначала в матрицу -- потом грамотно сохраняем в файл
                    # не нарушая структуры
                    self.matrix[i][j] = "1"
                    self.save_matrix()
                    self.show_places()
            else:
                # если не правильно записан номер ряда или место            
                QMessageBox(1, "Ошибка!", "Такого места нет!").exec_()
                return
            
    # загрузка матрицы
    def load_matrix(self):
        path = "Фильмы\\" + self.comboBox_films.currentText() +"\\" + \
            self.comboBox_date.currentText() + "\\" + self.comboBox_time.currentText()+".txt"
        file = codecs.open(path, encoding='utf-8', mode='r')
        self.matrix = []
        for line in file.read().splitlines():
            self.matrix.append([symbol for symbol in line.split(",") if symbol != "_"])
        file.close()
   
    # проверка на ввод всех данных
    def check_input(self):
        if (self.chosen_seat.text() == ""
            or self.chosen_row.text() == ""
            or self.comboBox_films.currentText()==""
            or self.comboBox_time.currentText()==""
            or self.comboBox_date.currentText()==""):
            QMessageBox(2, "Ошибка!", "Введите все данные до выбора места").exec_()
            return 0
        # проверка числа ли введены в текстбокс
        elif ((self.chosen_seat.text()).isnumeric()==False
             or (self.chosen_row.text()).isnumeric()==False):                
            QMessageBox(2, "Ошибка!", "В поля вводится только ЧИСЛА").exec_()
            return 0
        else:                
            return 1
                            
            
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())