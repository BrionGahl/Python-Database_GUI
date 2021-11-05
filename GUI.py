from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
from SQL import sqlConnection
from Flags import *

from LoginWindow import LoginWindow
from AddUpdateWindow import AddUpdateWindow

database = sqlConnection()




class GUI:
    app = None
    window = None
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle("Fusion")
        self.window = MainWindow()
        self.window.show()
        sys.exit(self.app.exec_())
        
    def initiateWindow(self):
        self.window = MainWindow()
        

#look into tab change event
class MainWindow(QMainWindow):
    userIDType = User.GUEST
    userID = None
    userName = None

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('MainUI_temp_stacked.ui', self)
        self.setWindowTitle("CS430 DB Access")
        self.stackedWidget.setCurrentIndex(self.userIDType.value)

        self.courses_table.setHorizontalHeaderLabels(['Course ID', 'Department', 'Course Name', 'Instructor', 'Meeting Time', 'Room', 'Currently Enrolled', 'Capacity']) 
        database.queryStudentCourses()
        self._populateTable(self.courses_table, 8)

        self._setupStudent()
        self._setupFaculty()
        self._setupStaff()

        self.login_button.clicked.connect(self.executeLogin)
        
    def _populateTable(self, table, columns):
        currRow = 0
        for row in database.cursor:
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
            self.student_courses_table.setHorizontalHeaderLabels(['Course ID', 'Department', 'Course Name', 'Instructor', 'Meeting Time', 'Room', 'Currently Enrolled', 'Capacity'])
            database.queryStudentCourses()
            self._populateTable(self.student_courses_table, 8)

            self.student_mycourses_table.setHorizontalHeaderLabels(['Course ID', 'Department', 'Course Name', 'Instructor', 'Exam 1', 'Exam 2', 'Final'])
            database.queryStudentMyCourses(self.userID)
            self._populateTable(self.student_mycourses_table, 7)
        
        def loadFaculty():
            self.faculty_student_table.setHorizontalHeaderLabels(['Student ID', 'Student Name', 'Major', 'Level', 'Age'])
            database.queryStudent()
            self._populateTable(self.faculty_student_table, 5)

            self.faculty_courses_table.setHorizontalHeaderLabels(['Course ID', 'Course Name', 'Meeting Time', 'Room', 'Faculty ID', 'Capacity'])
            database.queryCourses()
            self._populateTable(self.faculty_courses_table, 6)
            
            self.faculty_enrolled_table.setHorizontalHeaderLabels(['Student ID', 'Course ID', 'Exam 1', 'Exam 2', 'Final'])
            database.queryEnrolled()
            self._populateTable(self.faculty_enrolled_table, 5)
            
            self.faculty_faculty_table.setHorizontalHeaderLabels(['Faculty ID', 'Faculty Name', 'Department ID'])
            database.queryFaculty()
            self._populateTable(self.faculty_faculty_table, 3)
            
            self.faculty_staff_table.setHorizontalHeaderLabels(['Staff ID', 'Staff Name', 'Department ID'])
            database.queryStaff()
            self._populateTable(self.faculty_staff_table, 3)
            
            self.faculty_department_table.setHorizontalHeaderLabels(['Department ID', 'Department Name'])
            database.queryDepartment()
            self._populateTable(self.faculty_department_table, 2)

        def loadStaff():
            self.staff_student_table.setHorizontalHeaderLabels(['Student ID', 'Student Name', 'Major', 'Level', 'Age'])
            database.queryStudent()
            self._populateTable(self.staff_student_table, 5)

            self.staff_courses_table.setHorizontalHeaderLabels(['Course ID', 'Course Name', 'Meeting Time', 'Room', 'Faculty ID', 'Capacity'])
            database.queryCourses()
            self._populateTable(self.staff_courses_table, 6)
            
            self.staff_enrolled_table.setHorizontalHeaderLabels(['Student ID', 'Course ID', 'Exam 1', 'Exam 2', 'Final'])
            database.queryEnrolled()
            self._populateTable(self.staff_enrolled_table, 5)
            
            self.staff_faculty_table.setHorizontalHeaderLabels(['Faculty ID', 'Faculty Name', 'Department ID'])
            database.queryFaculty()
            self._populateTable(self.staff_faculty_table, 3)
            
            self.staff_staff_table.setHorizontalHeaderLabels(['Staff ID', 'Staff Name', 'Department ID'])
            database.queryStaff()
            self._populateTable(self.staff_staff_table, 3)
            
            self.staff_department_table.setHorizontalHeaderLabels(['Department ID', 'Department Name'])
            database.queryDepartment()
            self._populateTable(self.staff_department_table, 2)
        
        if (self.userIDType == User.STAFF):
            loadStaff()
        elif (self.userIDType == User.FACULTY):
            loadFaculty()
        elif (self.userIDType == User.STUDENT):
            loadStudent()
        

    def _fetchTableRow(self, table):
        row = []
        selected = table.currentItem()
        for i in range(table.columnCount()):
            row.append(table.item(selected.row(), i).text())
        return row

    def _setupStudent(self):
        self.student_logout_button.clicked.connect(self.executeLogout)
        self.student_enroll_button.clicked.connect(self.executeEnroll)
        self.student_search_button.clicked.connect(self.executeStudentSearch)
        print('student')

    def _setupFaculty(self):
        self.faculty_logout_button.clicked.connect(self.executeLogout)
        self.faculty_search_button.clicked.connect(self.executeSearch)
        print('faculty')

    def _setupStaff(self): 
        self.staff_logout_button.clicked.connect(self.executeLogout)
        self.staff_add_button.clicked.connect(self.executeAdd)
        self.staff_delete_button.clicked.connect(self.executeDelete)
        self.staff_update_button.clicked.connect(self.executeUpdate)
        self.staff_search_button.clicked.connect(self.executeSearch)

        print('staff')

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

    def executeLogout(self): #
        self.stackedWidget.setCurrentIndex(User.GUEST.value)
        self.userIDType = User.GUEST
        self.userID = None
        self.userName = None
        print("EXECUTED LOGOUT")

    def executeStudentSearch(self, string):
        print('pressed')

    def executeSearch(self, string): #UNION them all together
        print("pressed")

    def executeEnroll(self):
        table = self.student_courses_table
        try:
            record = self._fetchTableRow(table)
            updatedRecord = [self.userID, record[0], 'NULL', 'NULL', 'NULL']
            if (database.checkIDExists("Enrolled", self.userID, record[0])):
                QMessageBox.warning(self, 'Error', 'You are already enrolled in that course.')
                return    
            if (record[6] == record[7]):
                QMessageBox.warning(self, 'Error', 'That class is at full.')
                return    
            database.insertEntry("Enrolled", updatedRecord)
        except:
            QMessageBox.warning(self, 'Error', 'A row must be selected.')
            return
        database.cnx.commit()
        self._loadTables()
        return
    #
    # STAFF BUTTONS
    #
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
                database.insertEntry("Student", record)
            elif (curr_tab == 1):
                database.insertEntry("Courses", record)
            elif (curr_tab == 2):
                database.insertEntry("Enrolled", record)
            elif (curr_tab == 3):
                database.insertEntry("Faculty", record)
            elif (curr_tab == 4):
                database.insertEntry("Staff", record)
            elif (curr_tab == 5):
                database.insertEntry("Department", record)
        except:
            QMessageBox.warning(self, 'Error', 'Something went wrong.')
        database.cnx.commit()
        self._loadTables()
        return

    def executeDelete(self): #maybe stream line with enum
        qm = QMessageBox
        response = qm.question(self, 'Warning', 'Are you sure you want to delete this row?', qm.Yes | qm.No)
        if response == qm.No:
            return

        curr_tab = self.staff_tabs.currentIndex()
        try:
            if (curr_tab == 0):
                table = self.staff_student_table
                record = self._fetchTableRow(table)

                database.deleteEntry("Student", "sid", record[0])
            elif (curr_tab == 1):
                table = self.staff_courses_table
                record = self._fetchTableRow(table)

                database.deleteEntry("Courses", "cid", "'" + record[0] + "'")
            elif (curr_tab == 2):
                table = self.staff_enrolled_table
                record = self._fetchTableRow(table)

                database.deleteEntry("Enrolled", record[0], record[1])
            elif (curr_tab == 3):
                table = self.staff_faculty_table
                record = self._fetchTableRow(table)
                
                database.deleteEntry("Faculty", "fid", record[0])
            elif (curr_tab == 4):
                table = self.staff_staff_table
                record = self._fetchTableRow(table)
                
                database.deleteEntry("Staff", "sid", record[0])
            elif (curr_tab == 5):
                table = self.staff_department_table
                record = self._fetchTableRow(table)
                
                database.deleteEntry("Department", "did", record[0])
        except:
            QMessageBox.warning(self, 'Error', 'A row must be selected.')
            return
        database.cnx.commit()
        self._loadTables()
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

            updatedRecord = createWindow(record)
        except:
           QMessageBox.warning(self, 'Error', 'A row must be selected.')
           return
        if not updatedRecord:        
            return
        updatedRecord[:] = ["NULL" if x == '' else x for x in updatedRecord]
        print(updatedRecord)
        print("Starting")
        try:
            if (curr_tab == 0):
                database.updateEntry("Student", updatedRecord)
            elif (curr_tab == 1):
                database.updateEntry("Courses", updatedRecord)
            elif (curr_tab == 2):
                database.updateEntry("Enrolled", updatedRecord)
            elif (curr_tab == 3):
                database.updateEntry("Faculty", updatedRecord)
            elif (curr_tab == 4):
                database.updateEntry("Staff", updatedRecord)
            elif (curr_tab == 5):
                database.updateEntry("Department", updatedRecord)
        except:
            QMessageBox.warning(self, 'Error', 'Something went wrong.')
        database.cnx.commit()
        self._loadTables()
        return

        
 
        
#
# EVENTS
#

    def closeEvent(self, e):
        print("Connection Closed")
        database.closeConnection()
        print(self.userIDType)
        print(self.userName)


