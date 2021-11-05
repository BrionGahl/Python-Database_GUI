from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import *
from PyQt5 import uic
from SQL import sqlConnection
from Flags import *

class AddUpdateWindow(QDialog):
    index = None
    record = None

    database = None

    def __init__(self, index, flag, *args): #args is for existing values for update option
        super(AddUpdateWindow, self).__init__()
        uic.loadUi('AddUpdateUI_temp_stacked.ui', self)
        self.stackedWidget.setCurrentIndex(index)

        self.database = sqlConnection()

        self._setupValidator()
        self.index = index
        if (flag == Option.ADD):
            self._setupAdd()
        elif (flag == Option.UPDATE):
            self._setupUpdate(args[0])
        
        self.record = []
     
    def _setupValidator(self):
        names_rx = QRegExp("^[A-Za-z]+((\s)?([A-Za-z])+)*$") #names ##### MAKE VALIDATORS LIMITED TO SPACE IN DB
        alpha_rx = QRegExp("^[A-Za-z0-9]+$")

        self.student_sid.setValidator(QIntValidator(100, 199, self.student_sid))
        self.student_sname.setValidator(QRegExpValidator(names_rx, self.student_sname))
        self.student_age.setValidator(QIntValidator(10, 150, self.student_age))
        self._populateMajors()
        
        self.courses_cid.setValidator(QRegExpValidator(alpha_rx, self.courses_cid))
        self.courses_cname.setValidator(QRegExpValidator(names_rx, self.courses_cname))
        self.courses_room.setValidator(QRegExpValidator(alpha_rx, self.courses_room))
        self.courses_fid.setValidator(QIntValidator(200, 299, self.courses_fid))
        self.courses_limitnum.setValidator(QIntValidator(1, 100, self.courses_limitnum))

        self.enrolled_sid.setValidator(QIntValidator(100, 199, self.enrolled_sid))
        self.enrolled_cid.setValidator(QRegExpValidator(alpha_rx, self.enrolled_cid))
        self.enrolled_exam1.setValidator(QIntValidator(0, 100, self.enrolled_exam1))
        self.enrolled_exam2.setValidator(QIntValidator(0, 100, self.enrolled_exam2))
        self.enrolled_final.setValidator(QIntValidator(0, 100, self.enrolled_final))

        self.faculty_fid.setValidator(QIntValidator(200, 299, self.faculty_fid))
        self.faculty_fname.setValidator(QRegExpValidator(names_rx, self.faculty_fname))
        self.faculty_deptid.setValidator(QIntValidator(400, 499, self.faculty_deptid))

        self.staff_sid.setValidator(QIntValidator(300, 399, self.staff_sid))
        self.staff_sname.setValidator(QRegExpValidator(names_rx, self.staff_sname))
        self.staff_deptid.setValidator(QIntValidator(400, 499, self.staff_deptid))

        self.department_did.setValidator(QIntValidator(400, 499, self.department_did))
        self.department_dname.setValidator(QRegExpValidator(names_rx, self.department_dname))

    def _populateMajors(self):
        self.database.getDepartmentNames()
        for item in self.database.cursor:
            self.student_major.addItem(item[0])

    def _setupAdd(self): #maybe move validators to own method
        self.setWindowTitle("Add Record")
        if (self.index == 0):
            self.student_confirm_button.clicked.connect(self.handleAddConfirm)
        elif (self.index == 1):
            self.courses_confirm_button.clicked.connect(self.handleAddConfirm)
        elif (self.index == 2):
            self.enrolled_confirm_button.clicked.connect(self.handleAddConfirm)
        elif (self.index == 3):
            self.faculty_confirm_button.clicked.connect(self.handleAddConfirm)
        elif (self.index == 4):
            self.staff_confirm_button.clicked.connect(self.handleAddConfirm)
        elif (self.index == 5):
            self.department_confirm_button.clicked.connect(self.handleAddConfirm)
    
    def _setupUpdate(self, record):
        self.setWindowTitle("Update Record")
        if (self.index == 0):
            self.student_sid.setText(record[0])
            self.student_sname.setText(record[1])
            self.student_major.setCurrentIndex(self.student_major.findText(record[2]))
            self.student_slevel.setCurrentIndex(self.student_slevel.findText(record[3]))
            self.student_age.setText(record[4])
            
            self.student_sid.setReadOnly(True)

            self.student_confirm_button.clicked.connect(self.handleUpdateConfirm)
        elif (self.index == 1):
            self.courses_cid.setText(record[0])
            self.courses_cname.setText(record[1])
            
            time = record[2].split()
            print(time)
            self.courses_meetsat_day.setCurrentIndex(self.courses_meetsat_day.findText(time[0]))
            self.courses_meetsat_time.setTime(QTime.fromString(time[1], "hh:mm:ss"))

            self.courses_room.setText(record[3])
            self.courses_fid.setText(record[4])
            self.courses_limitnum.setText(record[5])

            self.courses_cid.setReadOnly(True)

            self.courses_confirm_button.clicked.connect(self.handleUpdateConfirm)
        elif (self.index == 2):
            self.enrolled_sid.setText(record[0])
            self.enrolled_cid.setText(record[1])
            self.enrolled_exam1.setText(record[2])
            self.enrolled_exam2.setText(record[3])
            self.enrolled_final.setText(record[4])

            self.enrolled_sid.setReadOnly(True)
            self.enrolled_cid.setReadOnly(True)

            self.enrolled_confirm_button.clicked.connect(self.handleUpdateConfirm)
        elif (self.index == 3):
            self.faculty_fid.setText(record[0])
            self.faculty_fname.setText(record[1])
            self.faculty_deptid.setText(record[2])

            self.faculty_fid.setReadOnly(True)

            self.faculty_confirm_button.clicked.connect(self.handleUpdateConfirm)
        elif (self.index == 4):
            self.staff_sid.setText(record[0])
            self.staff_sname.setText(record[1])
            self.staff_deptid.setText(record[2])

            self.staff_sid.setReadOnly(True)

            self.staff_confirm_button.clicked.connect(self.handleUpdateConfirm)
        elif (self.index == 5):
            self.department_did.setText(record[0])
            self.department_dname.setText(record[1])

            self.department_did.setReadOnly(True)

            self.department_confirm_button.clicked.connect(self.handleUpdateConfirm)

    def handleAddConfirm(self):
        record = []
        if (self.index == 0): # no values can be empty
            record.append(self.student_sid.text())
            record.append(self.student_sname.text())
            record.append(self.student_major.currentText())
            record.append(self.student_slevel.currentText())
            record.append(self.student_age.text())
            #check valid id
            if "" in record:
                QMessageBox.warning(self, 'Error', 'Cannot submit an empty line.')
                return
            elif (self.database.checkIDExists("Student", record[0]) or not (int(record[0]) >= 100 and int(record[0]) < 200)):
                QMessageBox.warning(self, 'Error', 'Invalid ID/ID already in use.')
                return
        elif (self.index == 1): # no values can be empty
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
        elif (self.index == 2): # more error checking, in case we try to add an existing combination
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
        elif (self.index == 3): # no values can be empty
            record.append(self.faculty_fid.text())
            record.append(self.faculty_fname.text())
            record.append(self.faculty_deptid.text())
            #check valid id
            if "" in record:
                QMessageBox.warning(self, 'Error', 'Cannot submit an empty line.')
                return
            elif (self.database.checkIDExists("Faculty", record[0]) or not (int(record[0]) >= 200 and int(record[0]) < 300)):
                QMessageBox.warning(self, 'Error', 'Invalid ID/ID already in use.')
                return
            elif (not self.database.checkIDExists("Department", record[2])):
                QMessageBox.warning(self, 'Error', 'Department does not exist.')
                return
        elif (self.index == 4): # no values can be empty
            record.append(self.staff_sid.text())
            record.append(self.staff_sname.text())
            record.append(self.staff_deptid.text())
            #check valid id
            if "" in record:
                QMessageBox.warning(self, 'Error', 'Cannot submit an empty line.')
                return
            elif (self.database.checkIDExists("Staff", record[0]) or not (int(record[0]) >= 300 and int(record[0]) < 400)):
                QMessageBox.warning(self, 'Error', 'Invalid ID/ID already in use.')
                return
            elif (not self.database.checkIDExists("Department", record[2])):
                QMessageBox.warning(self, 'Error', 'Department does not exist.')
                return
        elif (self.index == 5): # no values can be empty
            record.append(self.department_did.text())
            record.append(self.department_dname.text())
            #check valid id
            if "" in record:
                QMessageBox.warning(self, 'Error', 'Cannot submit an empty line.')
                return
            elif (self.database.checkIDExists("Department", record[0]) or not (int(record[0]) >= 400 and int(record[0]) < 500)):
                QMessageBox.warning(self, 'Error', 'Invalid ID/ID already in use.')
                return
        self.record = record
        self.accept()
        self.close()
        return

    def handleUpdateConfirm(self):
        record = []
        if (self.index == 0): # no values can be empty
            record.append(self.student_sid.text())
            record.append(self.student_sname.text())
            record.append(self.student_major.currentText())
            record.append(self.student_slevel.currentText())
            record.append(self.student_age.text())
            #check valid id
            if "" in record:
                QMessageBox.warning(self, 'Error', 'Cannot submit an empty line.')
                return
        elif (self.index == 1): # no values can be empty
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
        elif (self.index == 2): # more error checking, in case we try to add an existing combination
            record.append(self.enrolled_sid.text())
            record.append(self.enrolled_cid.text())
            record.append(self.enrolled_exam1.text())
            record.append(self.enrolled_exam2.text())
            record.append(self.enrolled_final.text())
            #check valid id
            if ((not (record[2] == "") and (int(record[2]) > 100)) or (not (record[3] == "") and (int(record[3]) > 100)) or (not (record[4] == "") and (int(record[4]) > 100))):
                QMessageBox.warning(self, 'Error', 'Grades must be in range 0 - 100')
                return
        elif (self.index == 3): # no values can be empty
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
        elif (self.index == 4): # no values can be empty
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
        elif (self.index == 5): # no values can be empty
            record.append(self.department_did.text())
            record.append(self.department_dname.text())
            #check valid id
            if "" in record:
                QMessageBox.warning(self, 'Error', 'Cannot submit an empty line.')
                return
        self.record = record
        self.accept()
        self.close()
        return
    
    def closeEvent(self, e):
        print("Connection Closed")
        self.database.closeConnection()