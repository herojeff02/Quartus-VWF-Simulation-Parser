# print("hello.")
# print("This is HAL speaking.")
# print("You should NOTs entitle somebody a superuser, unless both of you are sure that you're going the right way.")

import string

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
    value_type = ""
    signal_type = ""
    width = ""
    lsb_index = ""
    direction = ""
    parent = ""
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
            temp0 = each_line[each_line.find("LEVEL")+6]
            add_flag = True
        if each_line.find("FOR") != -1:
            temp1 = each_line[each_line.find("FOR")+4: -2]
            add_flag = True

        if add_flag:
            signals[transition_destination_index].addTransition(Transition(temp0, temp1))

        # signals[signal_cursor].addTransition(Transition())
        continue

signals = signals[:-1]


for item in signals:
    print(item.getName())
    for i in range(0, item.getTransitionCount()):
        print(item.getTransition(i).getDuration())

f.close()