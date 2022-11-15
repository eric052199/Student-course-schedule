USE m5;

SET foreign_key_checks = 0;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS student_course;
SET foreign_key_checks = 1;

CREATE TABLE students 
(
  student_id     INT           PRIMARY KEY   AUTO_INCREMENT, 
  student_name    VARCHAR(50)   NOT NULL
);

CREATE TABLE courses 
(
  course_id      INT            PRIMARY KEY   AUTO_INCREMENT, 
  course_name    VARCHAR(50)    NOT NULL,
  course_day	 VARCHAR(50)	NOT NULL,
  course_time	 VARCHAR(50)	NOT NULL
);

CREATE TABLE student_course
(
  student_id   INT    NOT NULL, 
  CONSTRAINT fk_student 
	FOREIGN KEY (student_id) REFERENCES students (student_id), 
    
  course_id    INT    NOT NULL,
  CONSTRAINT fk_course 
	FOREIGN KEY (course_id) REFERENCES courses (course_id)
);