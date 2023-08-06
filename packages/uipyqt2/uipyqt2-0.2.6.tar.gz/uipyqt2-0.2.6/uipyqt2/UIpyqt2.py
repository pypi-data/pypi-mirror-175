import PyQt6
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtWidgets import *

import sys # Только для доступа к аргументам командной строки

# Приложению нужен один (и только один) экземпляр QApplication.
# Передаём sys.argv, чтобы разрешить аргументы командной строки для приложения.
# Если не будете использовать аргументы командной строки, QApplication([]) тоже работает

class WinUI():
    def __init__(self,arg = sys.argv):
        super().__init__()
        # self.window = QMainWindow()
    
   
    
app = ""
class NewWin(WinUI):
    
    def __init__(self,arg = sys.argv,show = True):
        global app
        app = QApplication([])   
        super().__init__()
        global window
        self.arg = arg
        
        self.window = QMainWindow()
        window = self.window
        self.layout = QVBoxLayout()
        self.container = QWidget()
        
        self.container.setLayout(self.layout)
        
        self.window.setCentralWidget(self.container)
        if show == True or show == 1:
            self.window.show()
        
    def SetFixedWinSize(self,x,y):
        self.window.setFixedSize(QSize(x, y))
    def SetMaxWinSize(self,x,y):
        self.window.setMaximumSize(QSize(x, y))
    def SetMinWinSize(self,x,y):
        self.window.setMinimumSize(QSize(x, y))
    def mainloop(self):
        app.exec()
    def show(self):
        self.window.show()
    def hide(self):
        self.window.hide()  # Важно: окно по умолчанию скрыто.
    def Title(self,text):
        text = str(text)
        self.window.setWindowTitle(text)
    
button = ""
    
class Button(WinUI):
    global button
    
    def __init__(self,win,text,command=None,x=None,y=None):
        super().__init__()
        self.text = text
        self.win = win
        global button
        button = QPushButton(window,text=text)
        # button.move(99999,99999)
        self.button = button
        
        
        
        
        
       
        
        
        # self.button.released.connect(command)
        if x != None and y:
            button.move(x,y)
        try:
            self.button.clicked.connect(command)
        except Exception as e:
            print(e)
        
    def setPress(self,chek):
        self.button.setChecked(chek)
    # def setCentral(self):
    #     """установить кнопку как основной виджет"""
    #     win.window.setCentralWidget(self.button)
    def enabled(self,check):
        """включить/выключить кнопку"""
        self.button.setEnabled(check)
    def place(self,x,y):
        global button
        button.move(x,y)
        
    def pack(self):
        """быстро отрисовать виджет в столбик"""
        self.win.layout.addWidget(button)
    def setText(self,text):
        self.button.setText(text)

class Label(WinUI):
    def __init__(self,win,text):
        super().__init__()
        self.label = QLabel()
        self.label.setText(text)
    def pack(self):
        """быстро отрисовать виджет в столбик"""
        win.layout.addWidget(self.label)
    def setText(self,text):
        self.label.setText(text)

class DialogBox(WinUI):
    def __init__(self):
        super().__init__()

class InputLine(WinUI):
    """command - функция которая будет вызыватся при каждом изменение текста в виджете"""
    def __init__(self,win,command=None):
        self.win = win 
        self.input = QLineEdit()
        if command != None:
            self.input.textChanged.connect(command)
    def getText(self):
        """функция для получения текста из виджета InputLine"""
        return self.input.text()
    # def getText(self,text):
    #     self.text = text
    #     return self.text
    def pack(self):
        """быстро отрисовать виджет в столбик"""
        self.win.layout.addWidget(self.input)


# def iu():
#     lbl.setText(line.getText())
#     btn.setText(line.getText())
# def iu():
#     btn.place(50, 50)
# win = NewWin(arg=[],show=False)
# win.Title("wtf")
# # # lbl = Label(win, "nema")
# # # lbl.pack()
# line = InputLine(win,command=iu)
# line.pack()

# # btn = QPushButton(win.window)
# # btn.move(1,1)
# btn = Button(win, "nema", command=None,y=70)
# # btn.pack()
# btn.place(100, 100)
# win.show()
# win.mainloop()





    # Запускаем цикл событий.


    # Создаём виджет Qt — окно.
    