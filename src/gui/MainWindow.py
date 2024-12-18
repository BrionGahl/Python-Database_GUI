from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor, QPalette, QRegExpValidator
from PyQt5.QtWidgets import *
from PyQt5 import uic

import sys
from os import path
import csv

from sql.SQL import SQLConnection
from gui.Flags import *
from gui.LoginWindow import LoginWindow
from gui.AddUpdateWindow import AddUpdateWindow

# Linux support
PATH = path.dirname(path.abspath(__file__)) 

class GUI:
    _app = None
    _window = None

    def __init__(self):
        self._app = QApplication(sys.argv)
        self._app.setWindowIcon(QtGui.QIcon('assets\icons\window_logo.png'))
        self.initStyle()

        self._window = MainWindow()
        self._window.show()
        sys.exit(self._app.exec_())
        
    def initStyle(self):
        self._app.setStyle("Fusion")

        darkPalette = QPalette()

        darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
        darkPalette.setColor(QPalette.WindowText, Qt.white)
        darkPalette.setColor(QPalette.Base, QColor(25, 25, 25))
        darkPalette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
        darkPalette.setColor(QPalette.ToolTipText, Qt.white)
        darkPalette.setColor(QPalette.Text, Qt.white)
        darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
        darkPalette.setColor(QPalette.ButtonText, Qt.white)
        darkPalette.setColor(QPalette.BrightText, Qt.red)
        darkPalette.setColor(QPalette.Link, QColor(42, 130, 218))
        darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        darkPalette.setColor(QPalette.HighlightedText, Qt.black)

        self._app.setPalette(darkPalette)

        self._app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

        
class MainWindow(QMainWindow):
    userIDType = User.GUEST
    userID = None
    userName = None

    database = None

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(path.join(PATH, '../../assets/ui/MainUI.ui'), self)
        self.setWindowTitle("Brion Gahl - CS430 Project")
        self.stackedWidget.setCurrentIndex(self.userIDType.value)

        self.database = SQLConnection(False)

        self._setupGuest()
        self._setupStudent()
        self._setupFaculty()
        self._setupStaff()

        self.search_button.clicked.connect(self.executeGuestSearch)
        self.login_button.clicked.connect(self.executeLogin)

        self.database.queryStudentCourses()
        self._populateTable(self.courses_table, 8)
    
    def _populateTable(self, table, columns):
        currRow = 0
        table.setRowCount(currRow)
        for row in self.database.cursor:
            if row == None:
                break
            currRow += 1
            table.setRowCount(currRow)
            for currColumn in range(columns):
                table.setItem(currRow-1, currColumn, QtWidgets.QTableWidgetItem(str(row[currColumn])))
                if (row[currColumn] == None):
                    table.setItem(currRow-1, currColumn, QtWidgets.QTableWidgetItem(''))

    def _switchView(self):
        self.stackedWidget.setCurrentIndex(self.userIDType.value)
        self._loadTables()

    def _loadTables(self): 
        def loadStudent():            
            self.database.queryStudentCourses()
            self._populateTable(self.student_courses_table, 8)

            self.database.queryStudentMyCourses(self.userID)
            self._populateTable(self.student_mycourses_table, 7)
        
        def loadFaculty():
            self.database.queryStudent()
            self._populateTable(self.faculty_student_table, 5)

            self.database.queryCourses()
            self._populateTable(self.faculty_courses_table, 6)
            
            self.database.queryEnrolled()
            self._populateTable(self.faculty_enrolled_table, 5)
            
            self.database.queryFaculty()
            self._populateTable(self.faculty_faculty_table, 3)
            
            self.database.queryStaff()
            self._populateTable(self.faculty_staff_table, 3)
            
            self.database.queryDepartment()
            self._populateTable(self.faculty_department_table, 2)

        def loadStaff():
            self.database.queryStudent()
            self._populateTable(self.staff_student_table, 5)

            self.database.queryCourses()
            self._populateTable(self.staff_courses_table, 6)
            
            self.database.queryEnrolled()
            self._populateTable(self.staff_enrolled_table, 5)
            
            self.database.queryFaculty()
            self._populateTable(self.staff_faculty_table, 3)
            
            self.database.queryStaff()
            self._populateTable(self.staff_staff_table, 3)
            
            self.database.queryDepartment()
            self._populateTable(self.staff_department_table, 2)
        
        if (self.userIDType == User.STAFF):
            loadStaff()
        elif (self.userIDType == User.FACULTY):
            loadFaculty()
        elif (self.userIDType == User.STUDENT):
            loadStudent()
        elif (self.userIDType == User.GUEST):
            self.database.queryStudentCourses()
            self._populateTable(self.courses_table, 8)
            
    def _fetchTableRow(self, table):
        row = []
        selected = table.currentItem()
        for i in range(table.columnCount()):
            row.append(table.item(selected.row(), i).text())
        return row



    def _setupGuest(self):
        alpha_rx = QRegExp("^[A-Za-z0-9]+((\s)?([A-Za-z0-9])+)*$")
        self.search_bar.setValidator(QRegExpValidator(alpha_rx, self.search_bar))

        self.courses_table.setHorizontalHeaderLabels(['Course ID', 'Department', 'Course Name', 'Instructor', 'Meeting Time', 'Room', 'Currently Enrolled', 'Capacity']) 
        header = self.courses_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)

    def _setupStudent(self):
        alpha_rx = QRegExp("^[A-Za-z0-9]+((\s)?([A-Za-z0-9])+)*$")
        self.student_search_bar.setValidator(QRegExpValidator(alpha_rx, self.student_search_bar))
        
        self.student_courses_table.setHorizontalHeaderLabels(['Course ID', 'Department', 'Course Name', 'Instructor', 'Meeting Time', 'Room', 'Currently Enrolled', 'Capacity'])
        header = self.student_courses_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)

        self.student_mycourses_table.setHorizontalHeaderLabels(['Course ID', 'Department', 'Course Name', 'Instructor', 'Exam 1', 'Exam 2', 'Final'])
        header = self.student_mycourses_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)

        self.student_logout_button.clicked.connect(self.executeLogout)
        self.student_enroll_button.clicked.connect(self.executeEnroll)
        self.student_withdraw_button.clicked.connect(self.executeWithdraw)
        self.student_search_button.clicked.connect(self.executeStudentSearch)

    def _setupFaculty(self):
        alpha_rx = QRegExp("^[A-Za-z0-9]+((\s)?([A-Za-z0-9])+)*$")
        self.faculty_search_bar.setValidator(QRegExpValidator(alpha_rx, self.faculty_search_bar))

        self.faculty_student_table.setHorizontalHeaderLabels(['Student ID', 'Student Name', 'Major', 'Level', 'Age'])
        header = self.faculty_student_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

        self.faculty_courses_table.setHorizontalHeaderLabels(['Course ID', 'Course Name', 'Meeting Time', 'Room', 'Faculty ID', 'Capacity'])
        header = self.faculty_courses_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)

        self.faculty_enrolled_table.setHorizontalHeaderLabels(['Student ID', 'Course ID', 'Exam 1', 'Exam 2', 'Final'])
        header = self.faculty_enrolled_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

        self.faculty_faculty_table.setHorizontalHeaderLabels(['Faculty ID', 'Faculty Name', 'Department ID'])
        header = self.faculty_faculty_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.faculty_staff_table.setHorizontalHeaderLabels(['Staff ID', 'Staff Name', 'Department ID'])
        header = self.faculty_staff_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.faculty_department_table.setHorizontalHeaderLabels(['Department ID', 'Department Name'])
        header = self.faculty_department_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.faculty_logout_button.clicked.connect(self.executeLogout)
        self.faculty_export_button.clicked.connect(self.executeExport)
        self.faculty_search_button.clicked.connect(self.executeFacultySearch)

    def _setupStaff(self): 
        alpha_rx = QRegExp("^[A-Za-z0-9]+((\s)?([A-Za-z0-9])+)*$")
        self.staff_search_bar.setValidator(QRegExpValidator(alpha_rx, self.staff_search_bar))

        self.staff_student_table.setHorizontalHeaderLabels(['Student ID', 'Student Name', 'Major', 'Level', 'Age'])
        header = self.staff_student_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

        self.staff_courses_table.setHorizontalHeaderLabels(['Course ID', 'Course Name', 'Meeting Time', 'Room', 'Faculty ID', 'Capacity'])
        header = self.staff_courses_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)

        self.staff_enrolled_table.setHorizontalHeaderLabels(['Student ID', 'Course ID', 'Exam 1', 'Exam 2', 'Final'])
        header = self.staff_enrolled_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

        self.staff_faculty_table.setHorizontalHeaderLabels(['Faculty ID', 'Faculty Name', 'Department ID'])
        header = self.staff_faculty_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.staff_staff_table.setHorizontalHeaderLabels(['Staff ID', 'Staff Name', 'Department ID'])
        header = self.staff_staff_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.staff_department_table.setHorizontalHeaderLabels(['Department ID', 'Department Name'])
        header = self.staff_department_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.staff_logout_button.clicked.connect(self.executeLogout)
        self.staff_export_button.clicked.connect(self.executeExport)
        self.staff_add_button.clicked.connect(self.executeAdd)
        self.staff_delete_button.clicked.connect(self.executeDelete)
        self.staff_update_button.clicked.connect(self.executeUpdate)
        self.staff_search_button.clicked.connect(self.executeStaffSearch)



#
#  BUTTON METHODS
#
    def executeLogin(self):
        loginPage = LoginWindow()
        if loginPage.exec_() == QDialog.Accepted:
            self.userIDType = loginPage.idType 
            self.userID = loginPage.id
            self.userName = loginPage.name
        
        self._switchView()

        user_string = ("Logged in as: %s" % (self.userName))
        self.student_label.setText(user_string)
        self.faculty_label.setText(user_string)
        self.staff_label.setText(user_string)
        
        print("EXECUTED LOGIN")
        print("Logged in as {} {}".format(self.userID, self.userName))
        return

    def executeLogout(self): #
        qm = QMessageBox
        response = qm.question(self, 'Warning', 'Are you sure you want to logout?', qm.Yes | qm.No)
        if response == qm.No:
            return

        self.stackedWidget.setCurrentIndex(User.GUEST.value)
        self.userIDType = User.GUEST
        self.userID = None
        self.userName = None

        self._loadTables()

        print("EXECUTED LOGOUT")
        return



    def executeGuestSearch(self):
        string = self.search_bar.text()
        if string == "":
            self._loadTables()
            return
        self.database.searchStudentCourses(string)
        self._populateTable(self.courses_table, 8)

        print("EXECUTED SEARCH")
        return

    def executeStudentSearch(self):
        string = self.student_search_bar.text()
        if string == "":
            self._loadTables()
            return
        curr_tab = self.student_tabs.currentIndex()
        if (curr_tab == 0):
            self.database.searchStudentCourses(string)
            self._populateTable(self.student_courses_table, 8)
        elif (curr_tab == 1):
            self.database.searchStudentMyCourses(self.userID, string)
            self._populateTable(self.student_mycourses_table, 7)

        print("EXECUTED SEARCH")
        return

    def executeStaffSearch(self, string): 
        string = self.staff_search_bar.text()
        if string == "":
            self._loadTables()
            return
        curr_tab = self.staff_tabs.currentIndex()
        if (curr_tab == 0):
            self.database.searchStudent(string)
            self._populateTable(self.staff_student_table, 5)
        elif (curr_tab == 1):
            self.database.searchCourses(string)
            self._populateTable(self.staff_courses_table, 6)
        elif (curr_tab == 2):
            self.database.searchEnrolled(string)
            self._populateTable(self.staff_enrolled_table, 5)
        elif (curr_tab == 3):
            self.database.searchFaculty(string)
            self._populateTable(self.staff_faculty_table, 3)
        elif (curr_tab == 4):
            self.database.searchStaff(string)
            self._populateTable(self.staff_staff_table, 3)
        elif (curr_tab == 5):
            self.database.searchDepartment(string)
            self._populateTable(self.staff_department_table, 2)
        print("EXECUTED SEARCH")
        return
    
    def executeFacultySearch(self, string): 
        string = self.faculty_search_bar.text()
        if string == "":
            self._loadTables()
            return
        curr_tab = self.faculty_tabs.currentIndex()
        print(curr_tab)
        if (curr_tab == 0):
            self.database.searchStudent(string)
            self._populateTable(self.faculty_student_table, 5)
        elif (curr_tab == 1):
            self.database.searchCourses(string)
            self._populateTable(self.faculty_courses_table, 6)
        elif (curr_tab == 2):
            self.database.searchEnrolled(string)
            self._populateTable(self.faculty_enrolled_table, 5)
        elif (curr_tab == 3):
            self.database.searchFaculty(string)
            self._populateTable(self.faculty_faculty_table, 3)
        elif (curr_tab == 4):
            self.database.searchStaff(string)
            self._populateTable(self.faculty_staff_table, 3)
        elif (curr_tab == 5):
            self.database.searchDepartment(string)
            self._populateTable(self.faculty_department_table, 2)
        print("EXECUTED SEARCH")
        return



    def executeEnroll(self):
        table = self.student_courses_table
        try:
            record = self._fetchTableRow(table)
            updatedRecord = [self.userID, record[0], 'NULL', 'NULL', 'NULL']
            if (self.database.checkIDExists("Enrolled", self.userID, record[0])):
                QMessageBox.warning(self, 'Error', 'You are already enrolled in that course.')
                return    
            if (record[6] == record[7]):
                QMessageBox.warning(self, 'Error', 'That class is at full capacity.')
                return    

            qm = QMessageBox
            response = qm.question(self, 'Warning', 'Are you sure you want to enroll in this course?', qm.Yes | qm.No)
            if response == qm.No:
                return

            self.database.insertEntry("Enrolled", updatedRecord)
        except:
            QMessageBox.warning(self, 'Error', 'A row must be selected.')
            return
        self._loadTables()
        print("EXECUTED ENROLL")
        return

    def executeWithdraw(self):
        table = self.student_mycourses_table
        try:
            record = self._fetchTableRow(table)
            if (record[4] != '' or record[5] != '' or record[6] != ''):
                QMessageBox.warning(self, 'Error', 'Unable to Withdraw. A grade has already been posted.')
                return
        
            qm = QMessageBox
            response = qm.question(self, 'Warning', 'Are you sure you want to withdraw from this course?', qm.Yes | qm.No)
            if response == qm.No:
                return
            self.database.deleteEntry('Enrolled', self.userID, record[0])
        except:
            QMessageBox.warning(self, 'Error', 'A row must be selected.')
            return
        self._loadTables()
        print("EXECUTED WITHDRAW")
        return



    def executeAdd(self):
        curr_tab = self.staff_tabs.currentIndex()
        addWindow = AddUpdateWindow(curr_tab, Option.ADD)
        record = []
        if addWindow.exec_() == QDialog.Accepted:
            record = addWindow.record
        if not record:        
            return

        record[:] = ["NULL" if x == '' else x for x in record]
        try:
            if (curr_tab == 0):
                self.database.insertEntry("Student", record)
            elif (curr_tab == 1):
                self.database.insertEntry("Courses", record)
            elif (curr_tab == 2):
                self.database.insertEntry("Enrolled", record)
            elif (curr_tab == 3):
                self.database.insertEntry("Faculty", record)
            elif (curr_tab == 4):
                self.database.insertEntry("Staff", record)
            elif (curr_tab == 5):
                self.database.insertEntry("Department", record)
        except:
            QMessageBox.warning(self, 'Error', 'Something went wrong.')
        self._loadTables()
        print("EXECUTED ADD")
        return

    def executeDelete(self): 
        qm = QMessageBox
        response = qm.question(self, 'Warning', 'Are you sure you want to delete this row?', qm.Yes | qm.No)
        if response == qm.No:
            return

        curr_tab = self.staff_tabs.currentIndex()
        try:
            if (curr_tab == 0):
                table = self.staff_student_table
                record = self._fetchTableRow(table)

                self.database.deleteEntry("Student", "sid", record[0])
                table.clearSelection()
            elif (curr_tab == 1):
                table = self.staff_courses_table
                record = self._fetchTableRow(table)

                self.database.deleteEntry("Courses", "cid", "'" + record[0] + "'")
            elif (curr_tab == 2):
                table = self.staff_enrolled_table
                record = self._fetchTableRow(table)

                self.database.deleteEntry("Enrolled", record[0], record[1])
            elif (curr_tab == 3):
                table = self.staff_faculty_table
                record = self._fetchTableRow(table)
                
                self.database.deleteEntry("Faculty", "fid", record[0])
            elif (curr_tab == 4):
                table = self.staff_staff_table
                record = self._fetchTableRow(table)
                
                self.database.deleteEntry("Staff", "sid", record[0])
            elif (curr_tab == 5):
                table = self.staff_department_table
                record = self._fetchTableRow(table)
                
                self.database.deleteEntry("Department", "did", record[0])
        except:
            QMessageBox.warning(self, 'Error', 'A row must be selected.')
            return
        self._loadTables()
        print("EXECUTED DELETE")
        return

    def executeUpdate(self):
        def createWindow(record):
            updateWindow = AddUpdateWindow(curr_tab, Option.UPDATE, record)
            if updateWindow.exec_() == QDialog.Accepted:
                updatedRecord = updateWindow.record
                return updatedRecord
            return

        updatedRecord = []

        curr_tab = self.staff_tabs.currentIndex()
        try:
            if (curr_tab == 0):
                table = self.staff_student_table
                record = self._fetchTableRow(table)
            elif (curr_tab == 1):
                table = self.staff_courses_table
                record = self._fetchTableRow(table)
            elif (curr_tab == 2):
                table = self.staff_enrolled_table
                record = self._fetchTableRow(table)
            elif (curr_tab == 3):
                table = self.staff_faculty_table
                record = self._fetchTableRow(table)
            elif (curr_tab == 4):
                table = self.staff_staff_table
                record = self._fetchTableRow(table)
            elif (curr_tab == 5):
                table = self.staff_department_table
                record = self._fetchTableRow(table)
        except:
           QMessageBox.warning(self, 'Error', 'A row must be selected.')
           return
        updatedRecord = createWindow(record)
        if not updatedRecord:        
            return
        updatedRecord[:] = ["NULL" if x == '' else x for x in updatedRecord]
        try:
            if (curr_tab == 0):
                self.database.updateEntry("Student", updatedRecord)
            elif (curr_tab == 1):
                self.database.updateEntry("Courses", updatedRecord)
            elif (curr_tab == 2):
                self.database.updateEntry("Enrolled", updatedRecord)
            elif (curr_tab == 3):
                self.database.updateEntry("Faculty", updatedRecord)
            elif (curr_tab == 4):
                self.database.updateEntry("Staff", updatedRecord)
            elif (curr_tab == 5):
                self.database.updateEntry("Department", updatedRecord)
        except:
            QMessageBox.warning(self, 'Error', 'Something went wrong.')
        self._loadTables()
        print("EXECUTED UPDATE")
        return

    def executeExport(self):
        if (self.userIDType == User.STAFF):
            curr_tab = self.staff_tabs.currentIndex()
            if (curr_tab == 0):
                table = self.staff_student_table
                header = ['Student ID', 'Student Name', 'Major', 'Level', 'Age']
            elif (curr_tab == 1):
                table = self.staff_courses_table
                header = ['Course ID', 'Course Name', 'Meeting Time', 'Room', 'Faculty ID', 'Capacity']
            elif (curr_tab == 2):
                table = self.staff_enrolled_table
                header = ['Student ID', 'Course ID', 'Exam 1', 'Exam 2', 'Final']
            elif (curr_tab == 3):
                table = self.staff_faculty_table
                header = ['Faculty ID', 'Faculty Name', 'Department ID']
            elif (curr_tab == 4):
                table = self.staff_staff_table
                header = ['Staff ID', 'Staff Name', 'Department ID']
            elif (curr_tab == 5):
                table = self.staff_department_table
                header = ['Department ID', 'Department Name']
        else:
            curr_tab = self.faculty_tabs.currentIndex()
            if (curr_tab == 0):
                table = self.faculty_student_table
                header = ['Student ID', 'Student Name', 'Major', 'Level', 'Age']
            elif (curr_tab == 1):
                table = self.faculty_courses_table
                header = ['Course ID', 'Course Name', 'Meeting Time', 'Room', 'Faculty ID', 'Capacity']
            elif (curr_tab == 2):
                table = self.faculty_enrolled_table
                header = ['Student ID', 'Course ID', 'Exam 1', 'Exam 2', 'Final']
            elif (curr_tab == 3):
                table = self.faculty_faculty_table
                header = ['Faculty ID', 'Faculty Name', 'Department ID']
            elif (curr_tab == 4):
                table = self.faculty_staff_table
                header = ['Staff ID', 'Staff Name', 'Department ID']
            elif (curr_tab == 5):
                table = self.faculty_department_table
                header = ['Department ID', 'Department Name']
        try:
            with open('exported_data.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(header)
                for x in range(table.rowCount()):
                    row = []
                    for y in range(table.columnCount()):
                        row.append(table.item(x, y).text())
                    writer.writerow(row)
        except:
            QMessageBox.warning(self, 'Error', 'Unable to write to file. Is it open?')
            return

        QMessageBox.information(self, 'Success', 'Data for this table has been exported.')
        print("EXECUTED EXPORT")
        return

#
# EVENTS
#

    def closeEvent(self, e):
        print("CONNECTION CLOSED IN MAIN GUI")
        self.database.closeConnection()
        print(self.userIDType)
        print(self.userName)


