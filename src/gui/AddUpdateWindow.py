from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import *
from PyQt5 import uic

from sql.SQL import SQLConnection
from gui.Flags import *
from os import path

PATH = path.dirname(path.abspath(__file__))

class AddUpdateWindow(QDialog):
    _index = None
    _record = None

    @property
    def index(self):
        return self._index
    @property
    def record(self):
        return self._record

    database = None

    def __init__(self, index, flag, *args):
        super(AddUpdateWindow, self).__init__()
        uic.loadUi(path.join(PATH, '../../assets/ui/AddUpdateUI.ui'), self)
        self.stackedWidget.setCurrentIndex(index)

        self.setWindowFlag(Qt.FramelessWindowHint)

        self.database = SQLConnection(True)

        self._setupValidator()
        self._index = index
        if (flag == Option.ADD):
            self._setupAdd()
        elif (flag == Option.UPDATE):
            self._setupUpdate(args[0])
        
        self._record = []
     
    def _setupValidator(self): #cap validator length
        names_rx = QRegExp("^[A-Za-z]+((\s)?([A-Za-z])+)*$") 
        course_names_rx = QRegExp("^[A-Za-z]+((\s)?([A-Za-z0-9])+)*$")
        alpha_rx = QRegExp("^[A-Za-z0-9]{1,32}$")

        self.student_sid.setValidator(QIntValidator(1, 100000000, self.student_sid)) #100, 199
        self.student_sname.setValidator(QRegExpValidator(names_rx, self.student_sname))
        self.student_age.setValidator(QIntValidator(10, 150, self.student_age))
        self._populateMajors()
        
        self.courses_cid.setValidator(QRegExpValidator(alpha_rx, self.courses_cid))
        self.courses_cname.setValidator(QRegExpValidator(course_names_rx, self.courses_cname))
        self.courses_room.setValidator(QRegExpValidator(alpha_rx, self.courses_room))
        self.courses_fid.setValidator(QIntValidator(1, 100000000, self.courses_fid)) #200, 299
        self.courses_limitnum.setValidator(QIntValidator(1, 100, self.courses_limitnum))

        self.enrolled_sid.setValidator(QIntValidator(1, 100000000, self.enrolled_sid)) #100, 199
        self.enrolled_cid.setValidator(QRegExpValidator(alpha_rx, self.enrolled_cid))
        self.enrolled_exam1.setValidator(QIntValidator(0, 100, self.enrolled_exam1))
        self.enrolled_exam2.setValidator(QIntValidator(0, 100, self.enrolled_exam2))
        self.enrolled_final.setValidator(QIntValidator(0, 100, self.enrolled_final))

        self.faculty_fid.setValidator(QIntValidator(1, 100000000, self.faculty_fid)) #200, 299
        self.faculty_fname.setValidator(QRegExpValidator(names_rx, self.faculty_fname))
        self.faculty_deptid.setValidator(QIntValidator(1, 100000000, self.faculty_deptid)) #400, 499

        self.staff_sid.setValidator(QIntValidator(1, 100000000, self.staff_sid)) #300, 399
        self.staff_sname.setValidator(QRegExpValidator(names_rx, self.staff_sname))
        self.staff_deptid.setValidator(QIntValidator(1, 100000000, self.staff_deptid)) #400, 499

        self.department_did.setValidator(QIntValidator(1, 100000000, self.department_did)) #400, 499
        self.department_dname.setValidator(QRegExpValidator(names_rx, self.department_dname))

    def _populateMajors(self):
        self.database.getDepartmentNames()
        for item in self.database.cursor:
            self.student_major.addItem(item[0])

    def _setupAdd(self):
        if (self._index == 0):
            self.student_confirm_button.clicked.connect(self.handleAddConfirm)
            self.student_close_button.clicked.connect(self.handleClose)
        elif (self._index == 1):
            self.courses_confirm_button.clicked.connect(self.handleAddConfirm)
            self.courses_close_button.clicked.connect(self.handleClose)
        elif (self._index == 2):
            self.enrolled_confirm_button.clicked.connect(self.handleAddConfirm)
            self.enrolled_close_button.clicked.connect(self.handleClose)
        elif (self._index == 3):
            self.faculty_confirm_button.clicked.connect(self.handleAddConfirm)
            self.faculty_close_button.clicked.connect(self.handleClose)
        elif (self._index == 4):
            self.staff_confirm_button.clicked.connect(self.handleAddConfirm)
            self.staff_close_button.clicked.connect(self.handleClose)
        elif (self._index == 5):
            self.department_confirm_button.clicked.connect(self.handleAddConfirm)
            self.department_close_button.clicked.connect(self.handleClose)
    
    def _setupUpdate(self, record):
        if (self._index == 0):
            self.student_sid.setText(record[0])
            self.student_sname.setText(record[1])
            self.student_major.setCurrentIndex(self.student_major.findText(record[2]))
            self.student_slevel.setCurrentIndex(self.student_slevel.findText(record[3]))
            self.student_age.setText(record[4])
            
            self.student_sid.setReadOnly(True)

            self.student_confirm_button.clicked.connect(self.handleUpdateConfirm)
            self.student_close_button.clicked.connect(self.handleClose)
        elif (self._index == 1):
            self.courses_cid.setText(record[0])
            self.courses_cname.setText(record[1])
            
            time = record[2].split()
            self.courses_meetsat_day.setCurrentIndex(self.courses_meetsat_day.findText(time[0]))
            self.courses_meetsat_time.setTime(QTime.fromString(time[1], "hh:mm:ss"))

            self.courses_room.setText(record[3])
            self.courses_fid.setText(record[4])
            self.courses_limitnum.setText(record[5])

            self.courses_cid.setReadOnly(True)

            self.courses_confirm_button.clicked.connect(self.handleUpdateConfirm)
            self.courses_close_button.clicked.connect(self.handleClose)
        elif (self._index == 2):
            self.enrolled_sid.setText(record[0])
            self.enrolled_cid.setText(record[1])
            self.enrolled_exam1.setText(record[2])
            self.enrolled_exam2.setText(record[3])
            self.enrolled_final.setText(record[4])

            self.enrolled_sid.setReadOnly(True)
            self.enrolled_cid.setReadOnly(True)

            self.enrolled_confirm_button.clicked.connect(self.handleUpdateConfirm)
            self.enrolled_close_button.clicked.connect(self.handleClose)
        elif (self._index == 3):
            self.faculty_fid.setText(record[0])
            self.faculty_fname.setText(record[1])
            self.faculty_deptid.setText(record[2])

            self.faculty_fid.setReadOnly(True)

            self.faculty_confirm_button.clicked.connect(self.handleUpdateConfirm)
            self.faculty_close_button.clicked.connect(self.handleClose)
        elif (self._index == 4):
            self.staff_sid.setText(record[0])
            self.staff_sname.setText(record[1])
            self.staff_deptid.setText(record[2])

            self.staff_sid.setReadOnly(True)

            self.staff_confirm_button.clicked.connect(self.handleUpdateConfirm)
            self.staff_close_button.clicked.connect(self.handleClose)
        elif (self._index == 5):
            self.department_did.setText(record[0])
            self.department_dname.setText(record[1])

            self.department_did.setReadOnly(True)

            self.department_confirm_button.clicked.connect(self.handleUpdateConfirm)
            self.department_close_button.clicked.connect(self.handleClose)

    def handleAddConfirm(self):
        record = []
        if (self._index == 0): # no values can be empty
            record.append(self.student_sid.text())
            record.append(self.student_sname.text())
            record.append(self.student_major.currentText())
            record.append(self.student_slevel.currentText())
            record.append(self.student_age.text())
            #check valid id
            if "" in record:
                QMessageBox.warning(self, 'Error', 'Cannot submit an empty line.')
                return
            elif (self.database.checkIDExists("Student", record[0])): #or not (int(record[0]) >= 100 and int(record[0]) < 200)
                QMessageBox.warning(self, 'Error', 'Invalid ID/ID already in use.')
                return
        elif (self._index == 1): # no values can be empty
            record.append(self.courses_cid.text())
            record.append(self.courses_cname.text())
            cat = self.courses_meetsat_day.currentText() + " " + self.courses_meetsat_time.time().toString()
            record.append(cat)
            record.append(self.courses_room.text())
            record.append(self.courses_fid.text())
            record.append(self.courses_limitnum.text())
            #check valid id
            if "" in record:
                QMessageBox.warning(self, 'Error', 'Cannot submit an empty line.')
                return
            elif (self.database.checkIDExists("Courses", record[0])):
                QMessageBox.warning(self, 'Error', 'Invalid ID/ID already in use.')
                return
            elif (not self.database.checkIDExists("Faculty", record[4])):
                QMessageBox.warning(self, 'Error', 'A faculty member matching that ID does not exist.')
                return
        elif (self._index == 2): # more error checking, in case we try to add an existing combination
            record.append(self.enrolled_sid.text())
            record.append(self.enrolled_cid.text())
            record.append(self.enrolled_exam1.text())
            record.append(self.enrolled_exam2.text())
            record.append(self.enrolled_final.text())
            #check valid id
            if (record[0] == "" or record[1] == ""):
                QMessageBox.warning(self, 'Error', 'Student ID and Course ID must be given some value.')
                return
            elif (not self.database.checkIDExists("Student", record[0]) or not self.database.checkIDExists("Courses", record[1])):
                QMessageBox.warning(self, 'Error', 'One or more given ID may not exist.')
                return
            elif (self.database.checkIDExists("Enrolled", record[0], record[1])):
                QMessageBox.warning(self, 'Error', 'Student is already enrolled in that course.')
                return
            elif ((not (record[2] == "") and (int(record[2]) > 100)) or (not (record[3] == "") and (int(record[3]) > 100)) or (not (record[4] == "") and (int(record[4]) > 100))):
                QMessageBox.warning(self, 'Error', 'Grades must be in range 0 - 100')
                return
        elif (self._index == 3): # no values can be empty
            record.append(self.faculty_fid.text())
            record.append(self.faculty_fname.text())
            record.append(self.faculty_deptid.text())
            #check valid id
            if "" in record:
                QMessageBox.warning(self, 'Error', 'Cannot submit an empty line.')
                return
            elif (self.database.checkIDExists("Faculty", record[0])): # or not (int(record[0]) >= 200 and int(record[0]) < 300)
                QMessageBox.warning(self, 'Error', 'Invalid ID/ID already in use.')
                return
            elif (not self.database.checkIDExists("Department", record[2])):
                QMessageBox.warning(self, 'Error', 'Department does not exist.')
                return
        elif (self._index == 4): # no values can be empty
            record.append(self.staff_sid.text())
            record.append(self.staff_sname.text())
            record.append(self.staff_deptid.text())
            #check valid id
            if "" in record:
                QMessageBox.warning(self, 'Error', 'Cannot submit an empty line.')
                return
            elif (self.database.checkIDExists("Staff", record[0])): # or not (int(record[0]) >= 300 and int(record[0]) < 400)
                QMessageBox.warning(self, 'Error', 'Invalid ID/ID already in use.')
                return
            elif (not self.database.checkIDExists("Department", record[2])):
                QMessageBox.warning(self, 'Error', 'Department does not exist.')
                return
        elif (self._index == 5): # no values can be empty
            record.append(self.department_did.text())
            record.append(self.department_dname.text())
            #check valid id
            if "" in record:
                QMessageBox.warning(self, 'Error', 'Cannot submit an empty line.')
                return
            elif (self.database.checkIDExists("Department", record[0])): # or not (int(record[0]) >= 400 and int(record[0]) < 500)
                QMessageBox.warning(self, 'Error', 'Invalid ID/ID already in use.')
                return
        self._record = record
        self.accept()
        self.close()
        return

    def handleUpdateConfirm(self):
        record = []
        if (self._index == 0): # no values can be empty
            record.append(self.student_sid.text())
            record.append(self.student_sname.text())
            record.append(self.student_major.currentText())
            record.append(self.student_slevel.currentText())
            record.append(self.student_age.text())
            #check valid id
            if "" in record:
                QMessageBox.warning(self, 'Error', 'Cannot submit an empty line.')
                return
        elif (self._index == 1): # no values can be empty
            record.append(self.courses_cid.text())
            record.append(self.courses_cname.text())
            cat = self.courses_meetsat_day.currentText() + " " + self.courses_meetsat_time.time().toString()
            record.append(cat)
            record.append(self.courses_room.text())
            record.append(self.courses_fid.text())
            record.append(self.courses_limitnum.text())
            #check valid id
            if "" in record:
                QMessageBox.warning(self, 'Error', 'Cannot submit an empty line.')
                return
            elif (not self.database.checkIDExists("Faculty", record[4])):
                QMessageBox.warning(self, 'Error', 'A faculty member matching that ID does not exist.')
                return
        elif (self._index == 2): # more error checking, in case we try to add an existing combination
            record.append(self.enrolled_sid.text())
            record.append(self.enrolled_cid.text())
            record.append(self.enrolled_exam1.text())
            record.append(self.enrolled_exam2.text())
            record.append(self.enrolled_final.text())
            #check valid id
            if ((not (record[2] == "") and (int(record[2]) > 100)) or (not (record[3] == "") and (int(record[3]) > 100)) or (not (record[4] == "") and (int(record[4]) > 100))):
                QMessageBox.warning(self, 'Error', 'Grades must be in range 0 - 100')
                return
        elif (self._index == 3): # no values can be empty
            record.append(self.faculty_fid.text())
            record.append(self.faculty_fname.text())
            record.append(self.faculty_deptid.text())
            #check valid id
            if "" in record:
                QMessageBox.warning(self, 'Error', 'Cannot submit an empty line.')
                return
            elif (not self.database.checkIDExists("Department", record[2])):
                QMessageBox.warning(self, 'Error', 'Department does not exist.')
                return
        elif (self._index == 4): # no values can be empty
            record.append(self.staff_sid.text())
            record.append(self.staff_sname.text())
            record.append(self.staff_deptid.text())
            #check valid id
            if "" in record:
                QMessageBox.warning(self, 'Error', 'Cannot submit an empty line.')
                return
            elif (not self.database.checkIDExists("Department", record[2])):
                QMessageBox.warning(self, 'Error', 'Department does not exist.')
                return
        elif (self._index == 5): # no values can be empty
            record.append(self.department_did.text())
            record.append(self.department_dname.text())
            #check valid id
            if "" in record:
                QMessageBox.warning(self, 'Error', 'Cannot submit an empty line.')
                return
        self._record = record
        self.accept()
        self.close()
        return

    def handleClose(self):
        self.close()
        return
    
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    
    def closeEvent(self, e):
        print("CONNECTION CLOSED IN ADD/UPDATE")
        self.database.closeConnection()