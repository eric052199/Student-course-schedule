import mysql
import mysql.connector
db = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    passwd = "", #your password
    database = "m5"
)

mycursor = db.cursor()

############# CREATE DATABASE ##############
#mycursor.execute("CREATE DATABASE m5")



######### FUNCTIONS ###########
def get_id(student_name, course_name):
    info = (student_name, course_name)
    query = ("SELECT student_id, course_id "
              "FROM students s JOIN courses c "
              "WHERE s.student_name = %s AND c.course_name = %s ")
    mycursor.execute(query, info)
    student_id = 0
    course_id = 0
    for x in mycursor:
        student_id = x[0]
        course_id = x[1]
    return (student_id, course_id)

def enroll(student_name):
    #add new student into students table
    query = "INSERT INTO students (student_name) VALUES (%s)"
    name = [student_name]
    mycursor.execute(query, name)
    db.commit()
    print(student_name + " has enrolled in the program successfully.")

def intoduce_new_course(course_name, course_day, course_time):
    #add new course into courses table
    query = "INSERT INTO courses (course_name, course_day, course_time) VALUES (%s, %s, %s)"
    course_info = (course_name, course_day, course_time)
    mycursor.execute(query, course_info)
    db.commit()
    print(course_name + " has been registered in the course list successfully.")

def student_enroll_in_course(student_name, course_name):
    #put student into course
    query = "INSERT INTO student_course (student_id, course_id) VALUES (%s, %s)"
    #id = get_id(student_name, course_name)
    id = get_id(student_name, course_name)
    if id == (0,0):
        print("Please check student name or course name.")
        return
    
    mycursor.execute(query,id)
    db.commit()
    print(student_name + " has enrolled in " + course_name)

def students_in_courses(course_name):
    #cout all students enrolled in each course
    info = [course_name]
    query = ("SELECT DISTINCT course_name, student_name "
             "FROM courses c "
	         "JOIN student_course sc "
                 "ON c.course_id = sc.course_id "
             "JOIN students s "
                 "ON s.student_id = sc.student_id "
             "HAVING c.course_name = %s"
             "ORDER BY course_name, student_name")
    mycursor.execute(query, info)
    
    course_student = {}
    for (course_name, student_name) in mycursor:
        course_student.setdefault(course_name, []).append(student_name)
        
    for key, value in course_student.items():
        print(key, ": ", value)
        return
    
    if not mycursor.fetchall():
        print(course_name + " has no student yet.")
        

def courses_students_take(student_name):
    #cout all courses each student take
    info = [student_name]
    query = ("SELECT DISTINCT student_name, course_name "
            "FROM courses c "
	        "JOIN student_course sc "
                "ON c.course_id = sc.course_id "
            "JOIN students s "
                "ON s.student_id = sc.student_id "
            "HAVING s.student_name = %s "
            "ORDER BY student_name, course_name")

    mycursor.execute(query, info)

    student_course = {}
    for (student_name, course_name) in mycursor:
        student_course.setdefault(student_name, []).append(course_name)
        
    for key, value in student_course.items():
        print(key, ": ", value)
        return

    if not mycursor.fetchall():
        print(student_name + " has no class yet.")

def course_that_day(student_name, course_day):
    #cout all classes and time the student have on that day
    info = (student_name, course_day)
    query = ("SELECT DISTINCT c.course_name, c.course_time "
            "FROM courses c " 
            "JOIN student_course sc "
                "ON c.course_id = sc.course_id "
            "JOIN students s "
                "ON s.student_id = sc.student_id "
            "WHERE s.student_name = %s AND c.course_day = %s "
            "ORDER BY c.course_time, c.course_name")
    mycursor.execute(query, info)
    for x in mycursor:
        print("Course Name: " + x[0] + ", Course Time: " + x[1])
        return

    if not mycursor.fetchall():
        print(student_name + " has no class on " + course_day + ".")


while True:
    print("\n=============================================================")
    command = input("What do you want to do?\n"
                    "1: Enroll students into program.\n"
                    "2: Introduce new course.\n"
                    "3: Student enroll in course.\n"
                    "4: See students in each course.\n"
                    "5: See which courses each student is in.\n"
                    "6: Query course and time for a student on a chosen day.\n"
                    "7: Exit.\n"
                    "=============================================================\n")

    if command == "1":
        student_name = input("Please enter student's name: ")
        enroll(student_name)

    elif command == "2":
        course_name = input("Please enter course name: ")
        course_day = input("Please enter course day: ")
        course_time = input("Please enter course time: ")
        intoduce_new_course(course_name, course_day, course_time)

    elif command == "3":
        student_name = input("Please enter student name: ")
        course_name = input("Please enter course name: ")
        student_enroll_in_course(student_name, course_name)

    elif command == "4":
        course_name = input("Please enter course name: ")
        students_in_courses(course_name)

    elif command == "5":
        student_name = input("Please enter student name: ")
        courses_students_take(student_name)

    elif command == "6":
        student_name = input("Please enter student name: ")
        course_day = input("Please enter course day: ")
        course_that_day(student_name, course_day)

    elif command == "7":
        break
    
    else:
        print("Incorrect command.")

