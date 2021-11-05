from PyQt5.QtCore import *
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *
from PyQt5 import uic
from Flags import User

from SQL import sqlConnection

class LoginWindow(QDialog):
    _idType = None
    _id = None
    _name = None

    #getters
    @property
    def idType(self):
        return self._idType
    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name

    database = None
    
    def __init__(self):
        super(LoginWindow, self).__init__()
        uic.loadUi('LoginUI.ui', self)
        self.setWindowTitle("CS430 LOGIN")
        
        self.database = sqlConnection()

        self.login_line.setValidator(QIntValidator(100,399, self.login_line))
        self.login_button.clicked.connect(self.executeLogin)
        


    # handleLogin takes input from lineedit box and queries tables for users depending on id given. Returns enum for respective ID.
    def executeLogin(self):
        id = self.login_line.text()
        
        if (" " not in id and id[0] == '1' and self.database.checkIDExists('Student', id)):
            self.accept()
            self._idType = User.STUDENT
            self._id = id
            self._name = self.database.getStudentName(id) #maybe get rid of this and pull from cursor during initial query.
        elif (" " not in id and id[0] == '2' and self.database.checkIDExists('Faculty', id)):
            self.accept()
            self._idType = User.FACULTY
            self._id = id
            self._name = self.database.getFacultyName(id)
        elif (" " not in id and id[0] == '3' and self.database.checkIDExists('Staff', id)):
            self.accept()
            self._idType = User.STAFF
            self._id = id
            self._name = self.database.getStaffName(id)
        else:
            QMessageBox.warning(self, 'Error', 'Bad ID.')
            return
        self.database.closeConnection()
        print("Connection Closed")
        return

    def closeEvent(self, e):
        self.database.closeConnection()
        print("Connection Closed")

