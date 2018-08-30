from __future__ import print_function
import sys
import signal, os, subprocess
from subprocess import call
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from time import sleep
from datetime import datetime
from window_ui import Ui_MainWindow
from scipy.ndimage import imread
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from Email import *

# this string serves to delete files from DSLR to prevent crowding
clearCommand = ["gphoto2", "--folder", "store_0002001/DCIM/100CANON", \
                "-R", "--delete-all_files"]
captureCommand = ["gphoto2", "--capture-image-and-download"]
location = "derp"
greeting = "Hello pal! Here's that picture you took. -tom"


def take_shot():
    kill_process()
    shotTime = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    global location
    location = "/home/tom/Desktop/weddingPics/" + shotTime + "/"
    os.mkdir(location)
    os.chdir(location)
    call(captureCommand)
    

# you can't shoot if a process is all up in there already  
def kill_process():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    print("kill fn started")
    out, err = p.communicate()

    for line in out.splitlines():
        if b'gphoto' in line:
            print("something found")
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)
        elif b'gvsf-gphoto2' in line:
            print("something else found")
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)

class MainWin(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        # Hide all of the items not needed right now
        self.tryAgainButton.hide()
        self.saveButton.hide()
        self.cancelButton.hide()
        self.plainTextEdit.hide()
        self.label.hide()
        self.saveButton_2.hide()
        self.label_2.hide()
        self.label_3.hide()
        self.label_4.hide()
        self.countdown_label.hide()
        
        self.picture = QLabel(self)
        self.repaint()
        
        # When someone hits the main button, call the shotclicked fn
        self.pushButton.clicked.connect(lambda: self.shot_clicked())

        # When someone hits the tryAgainButton, call that fn
        self.tryAgainButton.clicked.connect(lambda: self.try_again_clicked())

        # When someone hits the Cancel button
        self.cancelButton.clicked.connect(lambda: self.cancel_clicked())

        # When someone hits the save button
        self.saveButton.clicked.connect(lambda: self.save_clicked())

        #When someone hits the 2nd save Button
        #self.saveButton_2.clicked.connect(lambda: self.save2_clicked())

    def try_again_clicked(self):
        self.tryAgainButton.hide()
        self.picture.hide()
        self.saveButton.hide()
        self.cancelButton.hide()
        self.label.hide()
        self.shot_clicked()

    def cancel_clicked(self):
        self.tryAgainButton.hide()
        self.picture.hide()
        self.saveButton.hide()
        self.cancelButton.hide()
        self.pushButton.show()
        self.label.hide()
        self.repaint()

    def shot_clicked(self):
        # Hide the main button, call gphoto code, then display the next buttons
        self.pushButton.hide()
        self.repaint()
        #self.countdown_label.setFont(Font(96))
        self.countdown_label.show()
        counts = ['5','4','3','2','shoot..']
        # countdown from 5
        for x in counts:
            sleep(1)
            self.countdown_label.setText(x)
            self.repaint()
            
        
        take_shot()
        self.countdown_label.hide()
        self.tryAgainButton.show()
        self.saveButton.show()
        self.cancelButton.show()
        self.label.show()
        self.repaint()
        
        # Display photo in the label/frame
        pixmap = QPixmap(location + "capt0000.jpg")
        print(location + "capt0000.jpg")
        self.picture.setScaledContents(True)
        self.picture.setGeometry(QtCore.QRect(5, 10, 1043, 700)) # x, y, height, width
        self.picture.setPixmap(pixmap)
        self.picture.show()
        self.picture.repaint()
        self.repaint()
        
    def save_clicked(self):
        self.tryAgainButton.hide()
        self.saveButton.hide()
        self.cancelButton.hide()
        self.picture.hide()
        #self.plainTextEdit.show()
        self.label.hide()
        #self.label_2.show()
        #self.saveButton_2.show()
        
        # I added this line for the modified, non email version
        self.pushButton.show()
        self.repaint()

    def save2_clicked(self):
        self.update()
        email_address = self.plainTextEdit.toPlainText()
        self.label_4.show()
        self.saveButton_2.hide()
        self.plainTextEdit.hide()
        self.plainTextEdit.clear()
        self.label_2.hide()
        self.repaint()
        
        #email to the recipient. if fail, save to txt
        try:
            #print(location + "capt0000.jpg is where the file is being sent from.......")
            #message = compose_mail_with_attachment('bomtucker343@gmail.com',
                                                   #email_address, 'Wedding Pic',
                                                   #greeting, location
                                                   #+ "capt0000.jpg")
            #print("message created")
            #credentials = get_credentials()
            #service = build('gmail', 'v1', http=credentials.authorize(Http()))
            #print("sent..?")

            create_message_and_send('bomtucker343@gmail.com',
                                    email_address, 'Wedding Pic',
                                    greeting, None, location + 'capt0000.jpg')

        except Exception as e:
            print(e)
            f = open(location + "address.txt", "w+")
            f.write(email_address)
            f.close()
        

        self.label_4.hide()
        self.label_3.show()
        self.repaint()
        sleep(2)
        self.label_3.hide()
        self.pushButton.show()
        self.repaint()

        
        
        
        
app = QApplication(sys.argv)
widget = MainWin()
widget.show()
sys.exit(app.exec_())
