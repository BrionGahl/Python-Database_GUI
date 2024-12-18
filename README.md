# CS430 Project

Brion Gahl

## Installation and Requirements

Project was developed with Python 3.9.0, however, the project should work for versions ~3.6-3.8 as well, although to be safe Python 3.9.0 should be used.
Once installed, utilize the python package manager, pip to install the required modules for the project, given by the requirements.txt file included with the project.

```bash
pip install -r requirements.txt
```

If for some reason this does not work, open the requirements.txt and pip install each of the required modules manually.

In order to setup the database run the following scripts found in the /test directory, on a MySQL server either by using the source command or through the respective means for whichever OS is used. MySQL Workbench can also be used to execute the scripts.

```bash
mysql> source create_script.sql
```
From here alter the config.json file located in the top most directory and input all the server information needed to run it on your own MySQL server.

Once the needed files have been installed and configured, navigate to the src directory, assign the required permissions to the main.py file, and run said file.

# Functionality and Description.

This project serves as a focal point for the knowledge gained through our CS 430 class. This project is a university database, that stores information about students, courses, enrollment, faculty, staff, and departments. The entirety of this project was designed with usability in mind. One of the core features of this project is the modern UI and styling used to ensure the GUI is both usable and pleasing to the eye of the user. With this, icons were used in the place of buttons in order to allow for functionality to be accessed at a glance without much need for learning too much. To assist in this tooltips have been added to each button, and the buttons used follow the Google Material Dark, design philosophy in which certain icons indicate certain functions. This should allow users to be able to recognize buttons and their functions based on previous knowledge from any prior applications they have utilized. Besides look the program is laid out into four different user states, guest, student, faculty, and staff.

## Functionality for Guests

Guest user's have the ability to only view information regarding the offered courses. This includes seeing the course ID, department, course name, instructor, meeting time, room, currently enrolled, and course capacity. With this guests have the ability to search the database by ID, department, course name, instructor name, meeting time, and room. A guest may also login to another user (Student, Faculty, or Staff), accessed via the login button and by utilizing a given ID. ID's can consist of up to 9 digits, but for ease of use and testing purposes the majority of the included ID's range from 0-599.

## Functionality for Students

Student users have the ability to view all offered course, similar to a guest user, as well as their currently enrolled courses, allowing them to see their grades for their enrolled courses. With this student users are able to enroll themselves in new courses by utilizing the enroll button, located at the top of the GUI and indicated by the check button and the 'Enroll' tooltip. Similar to a guest user a student may search either schema in various means, similar to the guest user. For the My Courses tab, they may search by ID, department, course name, and instructor. A student user may also withdraw from a class so long as no grades have been published, by clicking the withdraw button indicated by the back icon, with the 'Withdraw' tooltip. The student user is also able to utilize the logout button in the top left to return to a guest user.

Sample ID - 100

## Functionality for Faculty

Faculty users have the ability to view all tables within the database. All tables are separated by tabs with the current table being indicated by a white line under the name of the table. Faculty users are able to search the database by most key words and ID's found within any table. This user also has access to the export button indicated by the 'Export' tool tip. This button allows the user to export their current view of a given table to a CSV file in order to utilize if for their own use. This is potentially useful for faculty members to search a given course in which they may be teaching in order to have an excel sheet of all students enrolled in that given course for grading purposes. Similar to a student user, this user is also able to logout.

Sample ID - 200

## Functionality for Staff

Staff users have the most access to interaction within the database. Besides being able to see and search the entire database in a similar way in which faculty can, they are also able to add, delete, and update values within it. These functions are indicated by the plus button, minus button, and redo button respectively, as well as indicated by tool tips on hover. The add button opens a new pop up window requesting information based on which table the staff user is currently looking at. Once filled out and given the information is error free, the data will be inserted and committed into the database. The update button while similar, also needs the staff user to select a row of on whichever table they intend to update. Once done it locks the primary keys of the table, and only allows the other attributes to be changed. Once finalized and error free, the data is updated within the table. Both the add and update buttons, depending on the table being influenced, ensure that any ID's given to it must exist in another table first. For instance, if the user wishes to create a new course, their must first exist a faculty with the given ID used before the course can be inserted. Moving forward, the delete button also takes a selected row from the table, and asks the user for confirmation before deleting the record. In this project I opted to cascade deletions on virtually all tables but those within the student/department table relation, as a university would most likely not want to drop students whose major is no longer offered but instead leaves them for staff to update/fix. Similar to the faculty user, staff can also utilize the export button to save any data to a CSV file.

Sample ID - 300

# Closing Statement

Overall I was able to learn a good amount from this project. Subjects such as python object oriented programming, database programming, and GUI programming were all present. The features that I believe to stand out the most within this project, is the overall design of the project with its modern UI, the ability to withdraw from classes, and the ability to export data to a CSV file depending on present table outlook.
