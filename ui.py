from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys
import os
import re

import main
import helper

class Window(QWidget):
    def __init__(self, windowTitle, geom):
        super(Window, self).__init__()

        self.initUI(windowTitle, geom)

    def initUI(self, windowTitle, geom):
        QToolTip.setFont(QFont("SansSerif", 10))

        self.setGeometry(geom[0], geom[1], geom[2], geom[3])
        self.setStyleSheet("background-color: #fff;")
        self.setWindowTitle(windowTitle)
        self.show()

    def specifyFile(self):
        path = QFileDialog.getOpenFileName(self, "Open File",
                                           "/home",
                                           "Text files (*.txt)")
        if path!= "":
            self.close()
            fileInput = open(path, "r", 1)
            main.main(fileInput, False)


    def specifyDir(self):
        path = QFileDialog.getExistingDirectory(self, "Open Directory",
                                                "/home",
                                                QFileDialog.ShowDirsOnly)
        if path != "":
            fileName = helper.followDir(path, False)
            self.close()
            fileInput = open(path + "/" + fileName, "r", 1)
            main.main(fileInput, False)


class playerBox(QWidget):
    def __init__(self, player, handCount, bigBlind, parent = None):
        #  super(playerBox, parent).__init__()
        QWidget.__init__(self, parent)

        self.initUI(player, handCount, bigBlind)

    def initUI(self, player, handCount, bigBlind):
        self.setStyleSheet("background-color: #f5f5f5;")
        playerBoxLayout = QGridLayout(self)

        self.nameLabel = QLabel()
        self.nameLabel.setAlignment(Qt.AlignCenter)
        playerBoxLayout.addWidget(self.nameLabel, 0, 0, 2, 1)

        self.vpipLabel = QLabel()
        self.vpipLabel.setAlignment(Qt.AlignCenter)
        playerBoxLayout.addWidget(self.vpipLabel, 0, 1)

        self.pfrLabel = QLabel()
        self.pfrLabel.setAlignment(Qt.AlignCenter)
        playerBoxLayout.addWidget(self.pfrLabel, 0, 2)

        if player.preFlopAggresor > 0:
            self.fcbetLabel = QLabel()
            self.fcbetLabel.setAlignment(Qt.AlignCenter)
            playerBoxLayout.addWidget(self.fcbetLabel, 1, 1, 1, 2)
        else:
            self.fcbetLabel = QLabel("FCBet: N/A")
            self.fcbetLabel.setAlignment(Qt.AlignCenter)
            playerBoxLayout.addWidget(self.fcbetLabel, 1, 1, 1, 2)

        self.updateUI(player, handCount, bigBlind)

        self.setLayout(playerBoxLayout)

    def updateUI(self, player, handCount, bigBlind):
        self.nameLabel.setText(player.name + "\n("
                               + str(round(player.chipCount/bigBlind)) + " BB)")
        self.vpipLabel.setText("VPIP: " + str(round(player.vpip/handCount
                                        * 100, 2)) + "%")
        self.pfrLabel.setText("PFR: " + str(round(player.pfr/handCount*100, 2))
                                      + "%")
        if player.preFlopAggresor > 0:
            self.fcbetLabel.setText("FCBet: " + str(round(player.flopCbet
                                              /player.preFlopAggresor
                                              * 100, 2)) + "%")


def gui():
    window = Window("Pokerhontas Init", [300, 300, 250, 100])
    window.setFixedSize(250, 100)


    layout = QGridLayout(window)

    label = QLabel("Would you like to specify a file?")
    label.setAlignment(Qt.AlignCenter)
    layout.addWidget(label, 0, 0, 1, 2)

    yesBtn = QPushButton("&Yes")
    path = yesBtn.clicked.connect(window.specifyFile)
    layout.addWidget(yesBtn, 1, 0)

    noBtn = QPushButton("&No")
    path = noBtn.clicked.connect(window.specifyDir)
    layout.addWidget(noBtn, 1, 1)

    window.setLayout(layout)

    return window


def cli(path):
    if path[-1:] != "/":
        path += "/"

    print("Specify a file? ", end="")
    answered = False
    while not answered:
        userIn = input()
        if re.match("[yY](es)?", userIn):
            files = os.listdir(path)
            n = 0

            form = "{0:>3}: {1}"
            for f in files:
                print(form.format(str(n + 1), f))
                n += 1

            correctNumber = False
            print("Please enter a number between 1 and " + str(n)\
                  + " to select a file: ", end="")
            fileNumber = int(input()) - 1

            while not correctNumber:
                if fileNumber >= 0 and fileNumber < n:
                    fileName = files[fileNumber]
                    correctNumber = True

            print("Tracking " + fileName + "...")
            fileInput = open(path + fileName, "r", 1)
            answered = True

        elif re.match("[nN]o?", userIn):
            print("Watching " + path + " for new files...")
            fileName = helper.followDir(path, True)
            print("Found " + fileName + ". Tracking...")
            fileInput = open(path + fileName, "r", 1)
            answered = True

        else:
            print("Please enter yes or no: ", end="")

        main.main(fileInput, True)
