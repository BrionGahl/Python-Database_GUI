import mysql.connector
from mysql.connector import errorcode
import sys
import json

#
# By default mysql connector is set to repeatable read, and creates transactions for every execute.
#

class SQLConnection:
    _cursor = None
    _cnx = None

    @property
    def cursor(self):
        return self._cursor

    @property
    def cnx(self):
        return self._cnx

    def __init__(self, bool):
        with open('config.json') as cred:
            config = json.load(cred)
        self.initConnection(config)
        self._cnx.autocommit = False
        if (bool):
            self._cnx.start_transaction(consistent_snapshot=False, isolation_level='READ COMMITTED', readonly=bool)
    
    def initConnection(self, config):
        try:
            self._cnx = mysql.connector.connect(**config)
            self._cursor = self._cnx.cursor(prepared=True)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Incorrect name or password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("DB does not exist")
            else:
                print(err)
            sys.exit()

#
#  Student Queries
#
    def queryStudentCourses(self):
        query = ("SELECT c.cid, d.dname, c.cname, f.fname, c.meets_at, c.room, e.num, c.limit_num "
                 "FROM Courses c, Department d, Faculty f, (SELECT Courses.cid, COUNT(sid) AS num FROM Courses LEFT JOIN Enrolled ON Courses.cid = Enrolled.cid GROUP BY cid) as e "
                 "WHERE c.cid = e.cid AND c.fid = f.fid AND f.deptid = d.did;")
        self._cursor.execute(query)
    def queryStudentMyCourses(self, id):
        query = ("SELECT c.cid, d.dname, c.cname, f.fname, e.exam1, e.exam2, e.final FROM Courses c, Department d, Faculty f, Enrolled e WHERE c.cid = e.cid AND c.fid = f.fid AND f.deptid = d.did AND e.sid = %s" % (id))
        self._cursor.execute(query)
    def searchStudentCourses(self, string):
        query = """SELECT c.cid, d.dname, c.cname, f.fname, c.meets_at, c.room, e.num, c.limit_num 
        FROM Courses c, Department d, Faculty f, (SELECT Courses.cid, COUNT(sid) AS num FROM Courses LEFT JOIN Enrolled ON Courses.cid = Enrolled.cid GROUP BY cid) as e 
        WHERE c.cid = e.cid AND c.fid = f.fid AND f.deptid = d.did AND d.dname LIKE '%s%%' 
        UNION 
        SELECT c.cid, d.dname, c.cname, f.fname, c.meets_at, c.room, e.num, c.limit_num 
        FROM Courses c, Department d, Faculty f, (SELECT Courses.cid, COUNT(sid) AS num FROM Courses LEFT JOIN Enrolled ON Courses.cid = Enrolled.cid GROUP BY cid) as e 
        WHERE c.cid = e.cid AND c.fid = f.fid AND f.deptid = d.did AND c.cname LIKE '%s%%' 
        UNION 
        SELECT c.cid, d.dname, c.cname, f.fname, c.meets_at, c.room, e.num, c.limit_num 
        FROM Courses c, Department d, Faculty f, (SELECT Courses.cid, COUNT(sid) AS num FROM Courses LEFT JOIN Enrolled ON Courses.cid = Enrolled.cid GROUP BY cid) as e 
        WHERE c.cid = e.cid AND c.fid = f.fid AND f.deptid = d.did AND f.fname LIKE '%s%%' 
        UNION 
        SELECT c.cid, d.dname, c.cname, f.fname, c.meets_at, c.room, e.num, c.limit_num 
        FROM Courses c, Department d, Faculty f, (SELECT Courses.cid, COUNT(sid) AS num FROM Courses LEFT JOIN Enrolled ON Courses.cid = Enrolled.cid GROUP BY cid) as e 
        WHERE c.cid = e.cid AND c.fid = f.fid AND f.deptid = d.did AND c.meets_at LIKE '%s%%' 
        UNION 
        SELECT c.cid, d.dname, c.cname, f.fname, c.meets_at, c.room, e.num, c.limit_num 
        FROM Courses c, Department d, Faculty f, (SELECT Courses.cid, COUNT(sid) AS num FROM Courses LEFT JOIN Enrolled ON Courses.cid = Enrolled.cid GROUP BY cid) as e 
        WHERE c.cid = e.cid AND c.fid = f.fid AND f.deptid = d.did AND c.room LIKE '%s%%' 
        UNION 
        SELECT c.cid, d.dname, c.cname, f.fname, c.meets_at, c.room, e.num, c.limit_num 
        FROM Courses c, Department d, Faculty f, (SELECT Courses.cid, COUNT(sid) AS num FROM Courses LEFT JOIN Enrolled ON Courses.cid = Enrolled.cid GROUP BY cid) as e 
        WHERE c.cid = e.cid AND c.fid = f.fid AND f.deptid = d.did AND c.cid = '%s';""" % (string, string, string, string, string, string)
        self._cursor.execute(query)
    def searchStudentMyCourses(self, id, string):
        query = """SELECT c.cid, d.dname, c.cname, f.fname, e.exam1, e.exam2, e.final 
        FROM Courses c, Department d, Faculty f, Enrolled e 
        WHERE c.cid = e.cid AND c.fid = f.fid AND f.deptid = d.did AND e.sid = %s AND c.cid = '%s' 
        UNION 
        SELECT c.cid, d.dname, c.cname, f.fname, e.exam1, e.exam2, e.final 
        FROM Courses c, Department d, Faculty f, Enrolled e 
        WHERE c.cid = e.cid AND c.fid = f.fid AND f.deptid = d.did AND e.sid = %s AND d.dname LIKE '%s%%' 
        UNION 
        SELECT c.cid, d.dname, c.cname, f.fname, e.exam1, e.exam2, e.final 
        FROM Courses c, Department d, Faculty f, Enrolled e 
        WHERE c.cid = e.cid AND c.fid = f.fid AND f.deptid = d.did AND e.sid = %s AND c.cname LIKE '%s%%' 
        UNION 
        SELECT c.cid, d.dname, c.cname, f.fname, e.exam1, e.exam2, e.final 
        FROM Courses c, Department d, Faculty f, Enrolled e 
        WHERE c.cid = e.cid AND c.fid = f.fid AND f.deptid = d.did AND e.sid = %s AND f.fname LIKE '%s%%';""" % (id, string, id, string, id, string, id, string)
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

    def searchStudent(self, string):
        if " " in string:
            query = """SELECT * FROM Student WHERE sname LIKE '%s%%' 
            UNION 
            SELECT * FROM Student WHERE major LIKE '%s%%' 
            UNION 
            SELECT * FROM Student WHERE s_level LIKE '%s%%';""" % (string, string, string)
        elif (string.isdigit()):
            query = """SELECT * FROM Student WHERE sid = %s 
            UNION 
            SELECT * FROM Student WHERE age = %s;""" % (string, string)
        else:
            query = """SELECT * FROM Student WHERE sname LIKE '%s%%' 
            UNION 
            SELECT * FROM Student WHERE major LIKE '%s%%' 
            UNION 
            SELECT * FROM Student WHERE s_level LIKE '%s%%';""" % (string, string, string)
        self._cursor.execute(query)
    def searchCourses(self, string):
        if " " in string:
            query = """
            SELECT * FROM Courses WHERE cname LIKE '%s%%' 
            UNION 
            SELECT * FROM Courses WHERE meets_at LIKE '%s%%' 
            UNION 
            SELECT * FROM Courses WHERE room LIKE '%s%%';""" % (string, string, string)
        elif (string.isdigit()):
            query = """SELECT * FROM Courses WHERE fid = %s 
            UNION 
            SELECT * FROM Courses WHERE limit_num = %s;""" % (string, string)
        else:
            query = """SELECT * FROM Courses WHERE cid = '%s' 
            UNION 
            SELECT * FROM Courses WHERE cname LIKE '%s%%' 
            UNION 
            SELECT * FROM Courses WHERE meets_at LIKE '%s%%' 
            UNION 
            SELECT * FROM Courses WHERE room LIKE '%s%%';""" % (string, string, string, string)
        self._cursor.execute(query)
    def searchEnrolled(self, string):
        if " " in string:
            return
        query = "SELECT * FROM Enrolled WHERE cid = '%s'" % (string)
        self._cursor.execute(query)
    def searchFaculty(self, string):
        if (string.isdigit()):
            query = """SELECT * FROM Faculty WHERE fid = %s UNION SELECT * FROM Faculty where deptid = %s;""" % (string, string)
        else:
            query = """SELECT * FROM Faculty where fname LIKE '%s%%';""" % (string)
        self._cursor.execute(query)
    def searchStaff(self, string):
        if (string.isdigit()):
            query = """SELECT * FROM Staff where sid = %s UNION SELECT * FROM Staff where deptid = %s;""" % (string, string)
        else:
            query = """SELECT * FROM Staff where sname LIKE '%s%%';""" % (string)
        self._cursor.execute(query)
    def searchDepartment(self, string):
        if (string.isdigit()):
            query = "SELECT * FROM Department where did = %s;" % (string)
        else:
            query = "SELECT * FROM Department where dname LIKE '%s%%';" % (string) 
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
        self.commit()
        if (schema == "Enrolled"):
            query = ("DELETE FROM %s WHERE sid = %s AND cid = '%s';" % (schema, args[0], args[1]))
        else:
            query = ("DELETE FROM %s WHERE %s = %s;" % (schema, args[0], args[1]))
        self._cursor.execute(query)
        self.commit()
        return

    def insertEntry(self, schema, record):
        self.commit()
        if (schema == "Enrolled"):
            query = ("INSERT INTO %s VALUES (%s, '%s', %s, %s, %s);" % (schema, record[0], record[1], record[2], record[3], record[4]))
        else:
            query = ("INSERT INTO %s VALUES %s;" % (schema, tuple(record)))
        self._cursor.execute(query)
        self.commit()
        return

    def updateEntry(self, schema, record):
        self.commit()
        if (schema == "Enrolled"):
            query = ("UPDATE %s SET exam1 = %s, exam2 = %s, final = %s WHERE sid = %s and cid = '%s';" % (schema, record[2], record[3], record[4], record[0], record[1]))
        elif (schema == "Student"):
            query = ("UPDATE %s SET sname = '%s', major = '%s', s_level = '%s', age = %s WHERE sid = %s" % (schema, record[1], record[2], record[3], record[4], record[0]))
        elif (schema == "Courses"):
            query = ("UPDATE %s SET cname = '%s', meets_at = '%s', room = '%s', fid = %s, limit_num = %s WHERE cid = '%s'" % (schema, record[1], record[2], record[3], record[4], record[5], record[0]))
        elif (schema == "Faculty"):
            query = ("UPDATE %s SET fname = '%s', deptid = %s WHERE fid = %s" % (schema, record[1], record[2], record[0]))
        elif (schema == "Staff"):
            query = ("UPDATE %s SET sname = '%s', deptid = %s WHERE sid = %s" % (schema, record[1], record[2], record[0]))
        elif (schema == "Department"):
            query = (("UPDATE %s SET dname = '%s' WHERE did = %s" % (schema, record[1], record[0])))
        self._cursor.execute(query)
        self.commit()
        return



#
# General Methods
#
    def fetchRow(self):
        return self._cursor.fetchone()

    def commit(self):
        self._cnx.commit()

    def closeConnection(self):
        if (self._cnx.in_transaction):
            self._cnx.commit()
        self._cnx.close()
