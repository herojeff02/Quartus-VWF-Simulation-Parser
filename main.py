import os
import sys
from PyQt5.QtCore import QSize, QTimer, Qt
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import *

color_background = QColor(255, 255, 255)
color_blocked = QColor(2, 102, 0)
color_goal = QColor(4, 194, 2)
color_spawn = QColor(97, 152, 255)
color_obstacle = QColor(236, 30, 15)

cell_empty = 0
cell_blocked = 1
cell_goal = 2
cell_spawn = 3
cell_obstacle = 4
cell_player = 5

interval = 100

board_data = [[1, 1, 1, 1, 1, 1, 1, 1],
              [1, 0, 0, 0, 1, 1, 1, 1],
              [1, 0, 0, 0, 0, 1, 1, 1],
              [1, 0, 0, 0, 0, 0, 1, 1],
              [1, 1, 0, 0, 0, 0, 0, 1],
              [1, 1, 1, 0, 0, 0, 0, 1],
              [1, 1, 1, 1, 0, 0, 2, 1],
              [1, 1, 1, 1, 1, 1, 1, 1]]


def did_die(time):
    for item in signals:
        if item.getName() == "die":
            temp = item.getTransitionArray()
            for period in temp:
                total = period.getDuration()
                if total > time:
                    return period.getLevel()


def did_clear_game(time):
    total = 0.0
    for item in signals:
        if item.getName() == "WIN":
            temp = item.getTransitionArray()
            for period in temp:
                total = period.getDuration()
                if total > time:
                    return period.getLevel()

def parse_spawn():
    col = 0
    row = 0
    for item in signals:
        if item.getName() == "init_col[2]":
            temp = item.getTransitionArray()
            col += temp[0].getLevel()
            break
    for item in signals:
        if item.getName() == "init_col[1]":
            temp = item.getTransitionArray()
            col += temp[0].getLevel()*2
            break
    for item in signals:
        if item.getName() == "init_col[0]":
            temp = item.getTransitionArray()
            col += temp[0].getLevel()*4
            break

    for item in signals:
        if item.getName() == "init_row[2]":
            temp = item.getTransitionArray()
            row += temp[0].getLevel()
    for item in signals:
        if item.getName() == "init_row[1]":
            temp = item.getTransitionArray()
            row += temp[0].getLevel()*2
    for item in signals:
        if item.getName() == "init_row[0]":
            temp = item.getTransitionArray()
            row += temp[0].getLevel()*4

    board_data[int(row)][int(col)] = cell_spawn


def remove_player():
    for i in range(0, 8):
        for j in range(0, 8):
            if board_data[i][j] == cell_player:
                board_data[i][j] = cell_empty

def parse_player(time):
    col = 0
    row = 0
    for item in signals:
        if item.getName() == "col[2]":
            temp = item.getTransitionArray()
            for period in temp:
                total = period.getDuration()
                if total >= time:
                    col += period.getLevel()

                    break
    for item in signals:
        if item.getName() == "col[1]":
            temp = item.getTransitionArray()
            for period in temp:
                total = period.getDuration()
                if total >= time:
                    col += period.getLevel()*2
                    break
    for item in signals:
        if item.getName() == "col[0]":
            temp = item.getTransitionArray()

            for period in temp:
                total = period.getDuration()
                if total >= time:
                    col += period.getLevel()*4
                    break

    for item in signals:
        if item.getName() == "row[2]":
            temp = item.getTransitionArray()
            for period in temp:
                total = period.getDuration()
                if total > time:
                    row += period.getLevel()
                    break
    for item in signals:
        if item.getName() == "row[1]":
            temp = item.getTransitionArray()
            for period in temp:
                total = period.getDuration()
                if total > time:
                    row += period.getLevel()*2
                    break

    for item in signals:
        if item.getName() == "row[0]":
            temp = item.getTransitionArray()
            for period in temp:
                total = period.getDuration()
                if total > time:
                    row += period.getLevel()*4
                    break

    print(str(time) + "::" + str(row) + "." + str(col))

    board_data[int(row)][int(col)] = cell_player

def parse_blocked():
    for item in signals:
        if item.getName() == "romOut[6]":
            temp = item.getTransitionArray()
            j = 0
            for i in range(0, 6):
                if ((i + 1) * 10 >= temp[j].getDuration()):
                    j += 1
                board_data[i][5] = temp[j].getLevel()
        elif item.getName() == "romOut[5]":
            temp = item.getTransitionArray()
            j = 0
            for i in range(0, 6):
                if ((i + 1) * 10 >= temp[j].getDuration()):
                    j += 1
                board_data[i][4] = temp[j].getLevel()
        elif item.getName() == "romOut[4]":
            temp = item.getTransitionArray()
            j = 0
            for i in range(0, 6):
                if ((i + 1) * 10 >= temp[j].getDuration()):
                    j += 1
                board_data[i][3] = temp[j].getLevel()
        elif item.getName() == "romOut[3]":
            temp = item.getTransitionArray()
            j = 0
            for i in range(0, 6):
                if ((i + 1) * 10 >= temp[j].getDuration()):
                    j += 1
                board_data[i][2] = temp[j].getLevel()
        elif item.getName() == "romOut[2]":
            temp = item.getTransitionArray()
            j = 0
            for i in range(0, 6):
                if ((i + 1) * 10 >= temp[j].getDuration()):
                    j += 1
                board_data[i][1] = temp[j].getLevel()
        elif item.getName() == "romOut[1]":
            temp = item.getTransitionArray()
            j = 0
            for i in range(0, 6):
                if ((i + 1) * 10 >= temp[j].getDuration()):
                    j += 1
                board_data[i][0] = temp[j].getLevel()


def boardDataRefresh(time):
    parse_spawn()
    remove_player()
    parse_player(time)

def initial_parse():
    parse_spawn()

def testPrint():
    for item in signals:
        print(item.getName())
        for i in range(0, item.getTransitionCount()):
            print(str(int(item.getTransition(i).getLevel())) + " - " + str(item.getTransition(i).getDuration()))


lines = []
signals = []
signal_cursor = 0


class Transition:
    level = 0.0
    duration = 0.0

    def __init__(self, level, duration):
        self.duration = duration
        self.level = level

    def getLevel(self):
        return int(self.level)

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
    i = -1
    for item in signals:
        i += 1
        if item.getName() == name:
            return i


if(len(sys.argv)==1):
    print("No file directory handed over. Abort.")
    exit(-5)
f = open(sys.argv[1], 'r')
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
    if each_line.find(searchString + "(\"") != -1:  # -1 is returned when substring is not found.
        input_index = each_line.find(searchString)
        found_signal = True
        signals[signal_cursor].setName(each_line[input_index + len(searchString) + 2: len(each_line) - 3])
        continue

    searchString = "TRANSITION_LIST"
    if each_line.find(searchString + "(\"") != -1:  # -1 is returned when substring is not found.
        input_index = each_line.find(searchString)
        found_transition = True
        transition_destination_index = getIndexOfSignal_ByName(
            each_line[input_index + len(searchString) + 2: len(each_line) - 3])
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
            if(each_line[each_line.find("LEVEL") + 6]=='X'):
                temp0 = 0
            else:
                temp0 = float(each_line[each_line.find("LEVEL") + 6])
                add_flag = True
        if each_line.find("FOR") != -1:
            temp1 = float(each_line[each_line.find("FOR") + 4: -2])
            temp2 = temp1 + temp2
            add_flag = True

        if add_flag:
            signals[transition_destination_index].addTransition(Transition(temp0, temp2))

        # signals[signal_cursor].addTransition(Transition())
        continue

signals = signals[:-1]

f.close()




class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.timer_count = 0

        self.setFixedSize(360, 420)
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setRowCount(6)
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()
        self.setCentralWidget(self.table)

        self.button = QPushButton("Bon Voyage")
        self.button.clicked.connect(self.start_timer)
        self.button.setFixedHeight(30)

        tb = QToolBar()
        tb.setFixedHeight(40)
        tb.setFloatable(False)
        tb.setMovable(False)
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        tb.addWidget(left_spacer)
        tb.addWidget(self.button)
        tb.addWidget(right_spacer)
        self.addToolBar(tb)

        self.tb2 = QToolBar()
        self.tb2.setFloatable(False)
        self.tb2.setMovable(False)
        self.txt = QLabel("")
        left_spacer2 = QWidget()
        left_spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_spacer2 = QWidget()
        right_spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tb2.addWidget(left_spacer2)
        self.tb2.addWidget(self.txt)
        self.tb2.addWidget(right_spacer2)
        self.tb2.setFixedHeight(20)
        self.addToolBar(Qt.BottomToolBarArea, self.tb2)

        for i in range(0, 6):
            self.table.setRowHeight(i, 60)
            self.table.setColumnWidth(i, 60)

        initial_parse()

        # for i in range(0, 1001):
        #     self.start_timer()

    def timerCountUpdate(self, time=0):
        self.txt.setText(str(self.timer_count))
        self.tb2.setFixedHeight(20)
        self.addToolBar(Qt.BottomToolBarArea, self.tb2)

    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.setInterval(interval)
        self.timer.timeout.connect(self.draw)
        self.button.setDisabled(True)
        self.timer.start()

    def draw(self):
        self.timer.setInterval(interval)
        self.timerCountUpdate(self.timer_count)
        self.timer_count += 10
        if self.timer_count >= 1001:
            self.timer.stop()

        did_clear_flag = 0

        if (did_clear_game(self.timer_count)):
            self.timer.stop()
            print("You beat the game. I just had to tell you this in terminal :)")
            self.txt.setText("You beat the game in "+str(self.timer_count)+" nanoseconds.")
            did_clear_flag = 1

        boardDataRefresh(self.timer_count)

        did_die_flag = 0

        for i in range(self.timer_count, self.timer_count + interval):
            if did_die(i) == 1:
                did_die_flag = 1
                break

        for row in range(6):
            for column in range(6):
                if did_die_flag == 1:
                    temp = QTableWidgetItem()
                    temp.setFlags(Qt.ItemIsSelectable)
                    temp.setFlags(Qt.ItemIsEnabled)
                    temp.setBackground(QColor(255, 0, 0))
                    self.table.setItem(row, column, temp)
                else:
                    temp = QTableWidgetItem()
                    temp.setFlags(Qt.ItemIsSelectable)
                    temp.setFlags(Qt.ItemIsEnabled)
                    if board_data[row+1][column+1] == cell_empty:
                        temp.setBackground(color_background)
                        self.table.removeCellWidget(row, column)
                    elif board_data[row+1][column+1] == cell_blocked:
                        temp.setBackground(color_blocked)
                        self.table.removeCellWidget(row, column)
                    elif board_data[row+1][column+1] == cell_goal:
                        # temp.setBackground(color_goal)
                        temp = QLabel()
                        pixmap = QPixmap(os.path.dirname(os.path.realpath(__file__)) + '/arrival.png').scaled(60, 60, Qt.KeepAspectRatio,
                                                            Qt.SmoothTransformation)
                        temp.setPixmap(pixmap)
                        self.table.setCellWidget(row, column, temp)
                        continue
                    elif board_data[row+1][column+1] == cell_obstacle:
                        temp.setBackground(color_obstacle)
                        self.table.removeCellWidget(row, column)
                    elif board_data[row+1][column+1] == cell_spawn:
                        # temp.setBackground(color_spawn)
                        temp = QLabel()
                        pixmap = QPixmap(os.path.dirname(os.path.realpath(__file__)) + '/spawn.png').scaled(60, 60,
                                                                                                              Qt.KeepAspectRatio,
                                                                                                              Qt.SmoothTransformation)
                        temp.setPixmap(pixmap)
                        self.table.setCellWidget(row, column, temp)
                        continue
                    elif board_data[row+1][column+1] == cell_player:
                        temp = QLabel()
                        pixmap = QPixmap(os.path.dirname(os.path.realpath(__file__)) + '/test.png').scaled(60, 60, Qt.KeepAspectRatio,
                                                            Qt.SmoothTransformation)
                        temp.setPixmap(pixmap)
                        self.table.setCellWidget(row, column, temp)
                        continue

                    if did_clear_flag == 1:
                        if board_data[row+1][column+1] == cell_empty:
                            temp.setBackground(QColor(200, 200, 255))

                    self.table.setIconSize(QSize(60, 60))
                    self.table.setItem(row, column, temp)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
