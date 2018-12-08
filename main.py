import string
import sys
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *

board_data = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]

def parse_wall():
    for item in signals:
        if item.getName() == "romOutput[6]":
            temp = item.getTransitionArray()
            j=0
            for i in range(0, 6):
                if ((i+2) * 10 >= temp[j].getDuration()):
                    print("asdf" + str(j))
                    j += 1
                board_data[i][5] = temp[j].getLevel()
                print(board_data[i][5])
                print("dkdkdkdk - "+str(temp[j].getDuration()))
        elif item.getName() == "romOutput[5]":
            temp = item.getTransitionArray()
            j=0
            for i in range(0, 6):
                if ((i+2) * 10 >= temp[j].getDuration()):
                    print("asdf" + str(j))
                    j += 1
                board_data[i][4] = temp[j].getLevel()
                print(board_data[i][4])
                print("dkdkdkdk - "+str(temp[j].getDuration()))
        elif item.getName() == "romOutput[4]":
            temp = item.getTransitionArray()
            j=0
            for i in range(0, 6):
                if ((i+2) * 10 >= temp[j].getDuration()):
                    print("asdf" + str(j))
                    j += 1
                board_data[i][3] = temp[j].getLevel()
                print(board_data[i][3])
                print("dkdkdkdk - "+str(temp[j].getDuration()))
        elif item.getName() == "romOutput[3]":
            temp = item.getTransitionArray()
            j=0
            for i in range(0, 6):
                if ((i+2) * 10 >= temp[j].getDuration()):
                    print("asdf" + str(j))
                    j += 1
                board_data[i][2] = temp[j].getLevel()
                print(board_data[i][2])
                print("dkdkdkdk - "+str(temp[j].getDuration()))
        elif item.getName() == "romOutput[2]":
            temp = item.getTransitionArray()
            j=0
            for i in range(0, 6):
                if ((i+2) * 10 >= temp[j].getDuration()):
                    print("asdf" + str(j))
                    j += 1
                board_data[i][1] = temp[j].getLevel()
                print(board_data[i][1])
                print("dkdkdkdk - "+str(temp[j].getDuration()))
        elif item.getName() == "romOutput[1]":
            temp = item.getTransitionArray()
            j=0
            for i in range(0, 6):
                if ((i+2) * 10 >= temp[j].getDuration()):
                    print("asdf" + str(j))
                    j += 1
                board_data[i][0] = temp[j].getLevel()
                print(board_data[i][0])
                print("dkdkdkdk - "+str(temp[j].getDuration()))

def boardDataRefresh():
    print("print")

def testPrint():
    for item in signals:
        print(item.getName())
        for i in range(0, item.getTransitionCount()):
            print(str(int(item.getTransition(i).getLevel())) + " - " + str(item.getTransition(i).getDuration()))

lines = []
select_line = []
# upside = []
# downside = []
# leftside = []
# rightside = []
temp_string = []
input = []
signals = []
signal_cursor = 0

class Transition:
    level = 0
    duration = 0
    def __init__(self, level, duration):
        self.duration = duration
        self.level = level
    def getLevel(self):
        return self.level
    def getDuration(self):
        return self.duration

class Signal:
    name = ""
    direction = ""
    value_changes = []
    def __init__(self, name, direction):
        self.value_changes = []
        self.name = name
        self.direction = direction
    def getName(self):
        return self.name
    def setName(self, name):
        self.name = name

    def addTransition(self, tr):
        self.value_changes.append(tr)
    def getTransitionCount(self):
        return len(self.value_changes)
    def getTransition(self, index):
        return self.value_changes[index]
    def getPrevTransition(self, index):
        if index == 0:
            return 0
        else:
            return self.value_changes[index - 1]
    def getTransitionArray(self):
        return self.value_changes

def getIndexOfSignal_ByName(name):
    i=-1
    for item in signals:
        i+=1
        if item.getName() == name:
            return i

f = open("hw9_20181207154108.sim.txt", 'r')
signals.append(Signal("default", "asdf"))

while True:
    line = f.readline()
    if not line:
        break
    else:
        lines.append(line)

should_scan_content_of_bracket = False
found_signal = False
found_transition = False
transition_destination_index = 0
temp2 = 0.0

for each_line in lines:
    searchString = "SIGNAL"
    if each_line.find(searchString + "(\"") != -1: # -1 is returned when substring is not found.
        input_index = each_line.find(searchString)
        found_signal = True
        signals[signal_cursor].setName(each_line[input_index + len(searchString) + 2: len(each_line) - 3])
        continue

    searchString = "TRANSITION_LIST"
    if each_line.find(searchString + "(\"") != -1: # -1 is returned when substring is not found.
        input_index = each_line.find(searchString)
        found_transition = True
        transition_destination_index = getIndexOfSignal_ByName(each_line[input_index + len(searchString) + 2: len(each_line) - 3])
        temp2 = 0.0
        continue

    if each_line.find("{") != -1:
        if found_signal or found_transition:
            should_scan_content_of_bracket = True
            if found_signal:
                signals.append(Signal("test", "INPUT"))
        continue
    if each_line.find("}") != -1:
        if found_signal or found_transition:
            should_scan_content_of_bracket = False
            found_signal = False
            found_transition = False
            signal_cursor += 1
        continue


    if should_scan_content_of_bracket and found_transition:
        temp0 = -5
        temp1 = -5
        add_flag = False
        if each_line.find("LEVEL") != -1:
            temp0 = float(each_line[each_line.find("LEVEL")+6])
            add_flag = True
        if each_line.find("FOR") != -1:
            temp1 = float(each_line[each_line.find("FOR")+4: -2])
            temp2 = temp1 + temp2
            add_flag = True

        if add_flag:
            signals[transition_destination_index].addTransition(Transition(temp0, temp2))

        # signals[signal_cursor].addTransition(Transition())
        continue

signals = signals[:-1]




f.close()












class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.setFixedSize(360, 360)
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setRowCount(6)
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()
        self.table.setEnabled(False)
        self.setCentralWidget(self.table)

        for i in range(0, 6):
            self.table.setRowHeight(i, 60)
            self.table.setColumnWidth(i, 60)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.draw)
        self.timer.start()


        parse_wall()

        # for i in range(0, 1001):
        #     print("refreshed")
        #     self.start_timer()


    def draw(self):
        print("draw")
        for row in range(6):
            for column in range(6):
                temp = QTableWidgetItem()
                if board_data[row][column] == 0:
                    temp.setBackground(QColor(255, 255, 255))
                elif board_data[row][column] == 1:
                    temp.setBackground(QColor(97, 97, 97))
                self.table.setItem(row, column, temp)

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  app.exec()