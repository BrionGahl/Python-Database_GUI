import mysql.connector
from mysql.connector import errorcode

CONFIG = {
    'user': 'root',
    'password': '1422',
    'host': '127.0.0.1',
    'database': 'cs430'
}

class sqlConnection:
    _cursor = None
    _cnx = None

    @property
    def cursor(self):
        return self._cursor

    @property
    def cnx(self):
        return self._cnx

    def __init__(self):
        self.initConnection()
        self._cnx.start_transaction()
        #transaction isolation level here
    def initConnection(self):
        try:
            self._cnx = mysql.connector.connect(**CONFIG)
            self._cursor = self._cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Incorrect name or password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("DB does not exist")
            else:
                print(err)
        

#
#  Student Queries
#
    def queryStudentCourses(self):
        query = ("SELECT c.cid, d.dname, c.cname, f.fname, c.meets_at, c.room, e.num, c.limit_num FROM Courses c, Department d, Faculty f, (SELECT Courses.cid, COUNT(sid) AS num FROM Courses LEFT JOIN Enrolled ON Courses.cid = Enrolled.cid GROUP BY cid) as e WHERE c.cid = e.cid AND c.fid = f.fid AND f.deptid = d.did;")
        self._cursor.execute(query)
    def queryStudentMyCourses(self, id):
        query = ("SELECT c.cid, d.dname, c.cname, f.fname, e.exam1, e.exam2, e.final FROM Courses c, Department d, Faculty f, Enrolled e WHERE c.cid = e.cid AND c.fid = f.fid AND f.deptid = d.did AND e.sid = %s" % (id))
        self._cursor.execute(query)

#
#  Staff and Faculty Queries
#
    def queryStudent(self):
        query = ("SELECT * FROM Student;")
        self._cursor.execute(query)
    def queryCourses(self):
        query = ("SELECT * FROM Courses;")
        self._cursor.execute(query)
    def queryEnrolled(self):
        query = ("SELECT * FROM Enrolled;")
        self._cursor.execute(query)
    def queryFaculty(self):
        query = ("SELECT * FROM Faculty;")
        self._cursor.execute(query)
    def queryStaff(self):
        query = ("SELECT * FROM Staff;")
        self._cursor.execute(query)
    def queryDepartment(self):
        query = ("SELECT * FROM Department;")
        self._cursor.execute(query)

#
# General Queries
#
    def checkIDExists(self, schema, *args):
        if (schema == 'Student'):
            query = ("SELECT * FROM Student WHERE sid = %s;" % (args[0]))
        elif (schema == 'Faculty'):
            query = ("SELECT * FROM Faculty WHERE fid = %s;" % (args[0]))
        elif (schema == 'Staff'):
            query = ("SELECT * FROM Staff WHERE sid = %s;" % (args[0]))
        elif(schema == 'Enrolled'):
            query = ("SELECT * FROM Enrolled WHERE sid = %s AND cid = '%s';" % (args[0], args[1]))
        elif (schema == 'Courses'):
            query = ("SELECT * FROM Courses WHERE cid = '%s';" % (args[0]))
        elif (schema == 'Department'):
            query = ("SELECT * FROM Department WHERE did = %s;" % (args[0]))
        self._cursor.execute(query)

        if (self.fetchRow() == None):
            return False

        return True
    def getStudentName(self, id):
        query = ("SELECT sname from Student WHERE sid = %s" % (id))
        self._cursor.execute(query)
        return self.fetchRow()[0]
    def getFacultyName(self, id):
        query = ("SELECT fname from Faculty WHERE fid = %s" % (id))
        self._cursor.execute(query)
        return self.fetchRow()[0]
    def getStaffName(self, id):
        query = ("SELECT sname from Staff WHERE sid = %s" % (id))
        self._cursor.execute(query)
        return self.fetchRow()[0]

    def getDepartmentNames(self):
        query = ("SELECT dname from Department")
        self._cursor.execute(query)

#
# DELETE/INSERT/UPDATE
#
    def deleteEntry(self, schema, *args):
        if (schema == "Enrolled"):
            query = ("DELETE FROM %s WHERE sid = %s AND cid = %s;" % (schema, args[0], args[1]))
        else:
            query = ("DELETE FROM %s WHERE %s = %s;" % (schema, args[0], args[1]))
        self._cursor.execute(query)
        return

    def insertEntry(self, schema, record):
        if (schema == "Enrolled"):
            query = ("INSERT INTO %s VALUES (%s, %s, %s, %s, %s);" % (schema, record[0], record[1], record[2], record[3], record[4]))
        else:
            query = ("INSERT INTO %s VALUES %s;" % (schema, tuple(record)))
        self._cursor.execute(query)
        return

    def updateEntry(self, schema, record):
        if (schema == "Enrolled"):
            query = ("UPDATE %s SET exam1 = %s, exam2 = %s, final = %s WHERE sid = %s and cid = %s;" % (schema, record[2], record[3], record[4], record[0], record[1]))
        elif (schema == "Student"):
            query = ("UPDATE %s SET sname = '%s', major = '%s', s_level = '%s', age = %s WHERE sid = %s" % (schema, record[1], record[2], record[3], record[4], record[0]))
        elif (schema == "Courses"):
            query = ("UPDATE %s SET cname = '%s', meets_at = '%s', room = '%s', fid = %s, limit_num = %s WHERE cid = %s" % (schema, record[1], record[2], record[3], record[4], record[5], record[0]))
        elif (schema == "Faculty"):
            query = ("UPDATE %s SET fname = '%s', deptid = %s WHERE fid = %s" % (schema, record[1], record[2], record[0]))
        elif (schema == "Staff"):
            query = ("UPDATE %s SET sname = '%s', deptid = %s WHERE sid = %s" % (schema, record[1], record[2], record[0]))
        elif (schema == "Department"):
            query = (("UPDATE %s SET dname = '%s' WHERE did = %s" % (schema, record[1], record[0])))
        print("UPDATE: %s" % query)
        self._cursor.execute(query)
        return



#
# General Methods
#
    def fetchRow(self):
        return self._cursor.fetchone()

    def closeConnection(self):
        self._cnx.commit()
        self._cnx.close()
