import sqlite3 
# This line imports the SQLite libraries from python

# Function to create a new database using SQLite
def connect_db(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    return conn, cursor

# Function to create tables if they don't exist
def create_tables(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS Classes (
                        id INTEGER PRIMARY KEY,
                        class_name TEXT UNIQUE)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Students (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        class_id INTEGER,
                        FOREIGN KEY (class_id) REFERENCES Classes(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Assignments (
                        id INTEGER PRIMARY KEY,
                        assignment_name TEXT,
                        type TEXT,
                        class_id INTEGER,
                        FOREIGN KEY (class_id) REFERENCES Classes(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Grades (
                        id INTEGER PRIMARY KEY,
                        student_id INTEGER,
                        assignment_id INTEGER,
                        grade INTEGER,
                        FOREIGN KEY (student_id) REFERENCES Students(id),
                        FOREIGN KEY (assignment_id) REFERENCES Assignments(id))''')

# Function to add a new class
def add_class(cursor, class_name):
    cursor.execute('''INSERT INTO Classes (class_name) VALUES (?)''', (class_name,))
    cursor.connection.commit()

# Function to add a new student
def add_student(cursor, name, class_id):
    cursor.execute('''INSERT INTO Students (name, class_id) VALUES (?, ?)''', (name, class_id))
    cursor.connection.commit()

# Function to add a new assignment
def add_assignment(cursor, assignment_name, type, class_id):
    cursor.execute('''INSERT INTO Assignments (assignment_name, type, class_id) VALUES (?, ?, ?)''', (assignment_name, type, class_id))
    cursor.connection.commit()

# Function to record grades
def record_grade(cursor, student_id, assignment_id, grade):
    cursor.execute('''INSERT INTO Grades (student_id, assignment_id, grade) VALUES (?, ?, ?)''', (student_id, assignment_id, grade))
    cursor.connection.commit()

# Function to calculate overall class grade for a student
def calculate_class_grade(cursor, student_id):
    cursor.execute('''SELECT AVG(grade) FROM Grades WHERE student_id = ?''', (student_id,))
    avg_grade = cursor.fetchone()[0]
    return avg_grade

# Function to convert percentage to letter grade
def percentage_to_letter_grade(percentage):
    if percentage >= 90:
        return 'A'
    elif percentage >= 80:
        return 'B'
    elif percentage >= 70:
        return 'C'
    elif percentage >= 60:
        return 'D'
    else:
        return 'F'

# Function to display all student assignment and grades information
def display_student_info(cursor):
    cursor.execute('''SELECT Students.name, Assignments.assignment_name, Grades.grade
                      FROM Students
                      JOIN Grades ON Students.id = Grades.student_id
                      JOIN Assignments ON Assignments.id = Grades.assignment_id''')
    student_info = cursor.fetchall()
    for info in student_info:
        print(f"Student: {info[0]}, Assignment: {info[1]}, Grade: {info[2]}")

# Function to delete an assignment grade for a student
def delete_grade(cursor, student_id, assignment_id):
    cursor.execute('''DELETE FROM Grades WHERE student_id = ? AND assignment_id = ?''', (student_id, assignment_id))
    cursor.connection.commit()
    print("Grade deleted successfully.")

# Function to edit an assignment grade for a student
def edit_grade(cursor, student_id, assignment_id, new_grade):
    cursor.execute('''UPDATE Grades SET grade = ? WHERE student_id = ? AND assignment_id = ?''', (new_grade, student_id, assignment_id))
    cursor.connection.commit()
    print("Grade updated successfully.")

# Main function to interact with the application
def main():
    conn, cursor = connect_db("student_grades.db")
    create_tables(cursor)

    try:
        while True:
            print("\nWelcome to the Student Grading Application\n")
            print("1. Add Class")
            print("2. Add Student")
            print("3. Add Assignment")
            print("4. Record Grade")
            print("5. Calculate Class Grade")
            print("6. Display Student Assignment and Grades Information")
            print("7. Delete an assignment grade for Student")
            print("8. Edit an assignment grade for Student")
            print("9. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                class_name = input("Enter class name: ")
                add_class(cursor, class_name)
                print("Class added successfully!")

            elif choice == '2':
                name = input("Enter student name: ")
                class_id = int(input("Enter class ID: "))
                add_student(cursor, name, class_id)
                print("Student added successfully!")

            elif choice == '3':
                assignment_name = input("Enter assignment name: ")
                type = input("Enter type (Homework/Test): ")
                class_id = int(input("Enter class ID: "))
                add_assignment(cursor, assignment_name, type, class_id)
                print("Assignment added successfully!")

            elif choice == '4':
                student_id = int(input("Enter student ID: "))
                assignment_id = int(input("Enter assignment ID: "))
                grade = int(input("Enter grade: "))
                record_grade(cursor, student_id, assignment_id, grade)
                print("Grade recorded successfully!")

            elif choice == '5':
                student_id = int(input("Enter student ID: "))
                class_grade = calculate_class_grade(cursor, student_id)
                letter_grade = percentage_to_letter_grade(class_grade)
                print(f"Overall Class Grade: {class_grade}% ({letter_grade})")

            elif choice == '6':
                display_student_info(cursor)

            elif choice == '7':
                student_id = int(input("Enter student ID: "))
                assignment_id = int(input("Enter assignment ID: "))
                delete_grade(cursor, student_id, assignment_id)

            elif choice == '8':
                student_id = int(input("Enter student ID: "))
                assignment_id = int(input("Enter assignment ID: "))
                new_grade = int(input("Enter new grade: "))
                edit_grade(cursor, student_id, assignment_id, new_grade)

            elif choice == '9':
                break

            else:
                print("Invalid choice. Please try again.")

    except ValueError as ve:
        print("Error:", ve)
        print("Please enter a valid input.")
    except sqlite3.Error as sqle:
        print("Database error:", sqle)
    finally:
        conn.close()
        print("Thank you for using the Student Grading Application!")


if __name__ == "__main__":
    main()
