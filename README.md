# CS430 Project

Brion Gahl

## Installation and Requirements

Project was developed with Python 3.9.0, however, I believe the project should work for versions ~3.6-3.8 as well, although to be safe Python 3.9.0 should be used.
Once installed, utilize the python package manager, pip to install the required modules for the project, given by the requirements.txt file included with the project.

```bash
pip install -r requirements.txt
```

Once installed navigate to the src directory, assign the required permissions to the main.py file, and run said file.

## Functionality for Guests

As it is a Guest user has the ability to only view information regarding the offered courses. This includes seeing the course ID, department, course name, instructor, meeting time, room, currently enrolled, and course capacity. With this guests have the ability to search the database by ID, department, course name, instructor name, meeting time, and room. A guest may also login to another user (Student, Faculty, or Staff), accessed via the login button and by utilizing a given ID. ID's range from 100-399, with 100-199 being designated for students, 200-299 for faculty, and 300-399 for staff. This was done primarily for ease of use, but could easily be altered.

## Functionality for Students

Student users have the ability to view all offered course, similar to a guest user, as well as their currently enrolled courses, allowing them to see their grades for their enrolled courses. With this student users are able to enroll themselves in new courses by utilizing the enroll button, located at the top of the GUI and indicated by the check button and the 'Enroll' tooltip. Similar to a guest user a student may search either schema in various means, similar to the guest user. For the My Courses tab, they may search by ID, department, course name, and instructor. The student user is also able to utilize the logout button in the top left to return to a guest user.

Sample ID - 100

## Functionality for Faculty

Temp

Sample ID - 200

## Functionality for Staff

Temp

Sample ID - 300

## Closing Statement

Temp
