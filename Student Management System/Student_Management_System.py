import json
import os
from datetime import datetime
from abc import ABC, abstractmethod

DATA_FILE = "students.json"


class Person(ABC):
    """A base class for a person with name, email and phone."""

    def __init__(self, name, email, phone):
        """Set the person's name, email and phone number."""
        self._name = name
        self._email = email
        self._phone = phone

    @abstractmethod
    def get_role(self):
        """Return the role of this person (e.g. Student)."""
        pass

    def get_name(self):
        """Return the person's name."""
        return self._name

    def get_email(self):
        """Return the person's email."""
        return self._email

    def set_email(self, email):
        """Change the person's email to a new one."""
        self._email = email

    def __str__(self):
        """Return a readable string showing name, email and phone."""
        return f"{self._name} | {self._email} | {self._phone}"


class Student(Person):
    """A student enrolled in a course with grades."""

    def __init__(self, student_id, name, email, phone, course, year):
        """Set student ID, name, email, phone, course, year and empty grades."""
        super().__init__(name, email, phone)
        self._student_id = student_id
        self._course = course
        self._year = year
        self._grades = {}

    def get_role(self):
        """Return 'Student' as the role."""
        return "Student"

    def get_student_id(self):
        """Return the student's ID number."""
        return self._student_id

    def get_course(self):
        """Return the course the student is in."""
        return self._course

    def set_course(self, course):
        """Change the student's course."""
        self._course = course

    def get_year(self):
        """Return the current year of study (1-4)."""
        return self._year

    def set_year(self, year):
        """Change the student's year of study."""
        self._year = year

    def add_grade(self, subject, grade):
        """Add a grade (0-100) for a subject."""
        self._grades[subject] = grade

    def get_grades(self):
        """Return all grades as a dictionary {subject: grade}."""
        return self._grades

    def get_average_grade(self):
        """Return the average of all grades, or 0.0 if none."""
        if not self._grades:
            return 0.0
        return sum(self._grades.values()) / len(self._grades)

    def to_dict(self):
        """Turn the student data into a dictionary for saving to file."""
        return {
            "student_id": self._student_id,
            "name": self._name,
            "email": self._email,
            "phone": self._phone,
            "course": self._course,
            "year": self._year,
            "grades": self._grades,
        }

    @staticmethod
    def from_dict(data):
        """Create a Student object from a dictionary loaded from file."""
        s = Student(
            data["student_id"], data["name"], data["email"],
            data["phone"], data["course"], data["year"]
        )
        s._grades = data.get("grades", {})
        return s

    def __str__(self):
        """Return a readable string with ID, name, course, year and average."""
        return (f"[{self._student_id}] {self._name} | {self._course} Year {self._year} "
                f"| Avg: {self.get_average_grade():.1f}")


class Course:
    """A course with a code, name and number of credits."""

    def __init__(self, code, name, credits):
        """Set the course code, name and credits."""
        self._code = code
        self._name = name
        self._credits = credits

    def get_code(self):
        """Return the course code (e.g. CS101)."""
        return self._code

    def get_name(self):
        """Return the course name."""
        return self._name

    def __str__(self):
        """Return a readable string showing code, name and credits."""
        return f"{self._code}: {self._name} ({self._credits} cr)"


class StudentManager:
    """Manages all students — add, remove, update, search, grades and file save/load."""

    def __init__(self):
        """Start with an empty student list and some default courses."""
        self._students = {}
        self._courses = [
            Course("CS101", "Intro to Programming", 4),
            Course("CS201", "Data Structures", 4),
            Course("CS301", "Algorithms", 4),
            Course("CS401", "Software Engineering", 3),
            Course("MATH101", "Calculus I", 3),
            Course("MATH201", "Linear Algebra", 3),
            Course("ENG101", "English Composition", 2),
        ]

    def add_student(self, student_id, name, email, phone, course, year):
        """Add a new student. Returns True if successful, False if ID already exists."""
        if student_id in self._students:
            print(f"Student ID '{student_id}' already exists.")
            return False
        self._students[student_id] = Student(student_id, name, email, phone, course, year)
        print(f"Student '{name}' added successfully.")
        return True

    def remove_student(self, student_id):
        """Remove a student by ID. Returns True if successful, False if not found."""
        if student_id not in self._students:
            print(f"Student ID '{student_id}' not found.")
            return False
        name = self._students[student_id].get_name()
        del self._students[student_id]
        print(f"Student '{name}' removed successfully.")
        return True

    def update_student(self, student_id, name=None, email=None, phone=None, course=None, year=None):
        """Update a student's details. Only changes fields that are provided."""
        s = self._students.get(student_id)
        if not s:
            print(f"Student ID '{student_id}' not found.")
            return False
        if name:
            s._name = name
        if email:
            s._email = email
        if phone:
            s._phone = phone
        if course:
            s._course = course
        if year:
            s._year = year
        print(f"Student '{student_id}' updated.")
        return True

    def search_student(self, query):
        """Find students by name (partial match) or exact ID. Returns a list."""
        results = [s for s in self._students.values()
                   if query.lower() in s.get_name().lower() or query == s.get_student_id()]
        return results

    def get_student(self, student_id):
        """Return the Student object for the given ID, or None if not found."""
        return self._students.get(student_id)

    def list_all_students(self):
        """Print a table of all students with ID, name, course, year and average grade."""
        if not self._students:
            print("No students registered.")
            return
        print(f"\n{'ID':<12} {'Name':<20} {'Course':<25} {'Year':<6} {'Avg Grade':<10}")
        print("-" * 75)
        for s in self._students.values():
            print(f"{s.get_student_id():<12} {s.get_name():<20} {s.get_course():<25} "
                  f"{s.get_year():<6} {s.get_average_grade():<10.1f}")
        print(f"\nTotal students: {len(self._students)}")

    def add_grade(self, student_id, subject, grade):
        """Add a grade (0-100) for a student in a subject. Returns True if successful."""
        s = self._students.get(student_id)
        if not s:
            print(f"Student ID '{student_id}' not found.")
            return False
        if not (0 <= grade <= 100):
            print("Grade must be between 0 and 100.")
            return False
        s.add_grade(subject, grade)
        print(f"Grade {grade} added for {s.get_name()} in {subject}.")
        return True

    def save_to_file(self, filename=DATA_FILE):
        """Save all student data to a JSON file."""
        data = {
            "students": [s.to_dict() for s in self._students.values()],
            "saved_at": datetime.now().isoformat(),
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename} ({len(self._students)} students).")

    def load_from_file(self, filename=DATA_FILE):
        """Load student data from a JSON file. Returns True if successful."""
        if not os.path.exists(filename):
            print(f"No save file found ({filename}).")
            return False
        with open(filename, "r") as f:
            data = json.load(f)
        self._students = {
            s["student_id"]: Student.from_dict(s) for s in data["students"]
        }
        print(f"Loaded {len(self._students)} students from {filename}.")
        return True

    def get_statistics(self):
        """Return stats: total students, average grade, top student, course distribution."""
        if not self._students:
            return {"total": 0}
        grades = []
        course_count = {}
        for s in self._students.values():
            grades.append(s.get_average_grade())
            c = s.get_course()
            course_count[c] = course_count.get(c, 0) + 1
        avg = sum(grades) / len(grades)
        top = max(s for s in self._students.values() if s.get_average_grade() == max(grades))
        return {
            "total": len(self._students),
            "average": round(avg, 1),
            "top_student": top.get_name(),
            "top_avg": max(grades),
            "course_distribution": course_count,
        }


class Menu:
    """A menu-based interface for the Student Management System."""

    def __init__(self):
        """Create a new StudentManager to work with."""
        self._manager = StudentManager()

    def display_header(self):
        """Print the system title banner."""
        print("\n" + "=" * 55)
        print("          STUDENT MANAGEMENT SYSTEM")
        print("=" * 55)

    def display_menu(self):
        """Print the main menu options."""
        print("\n--- MAIN MENU ---")
        print("1. Add Student")
        print("2. Remove Student")
        print("3. Update Student")
        print("4. Search Student")
        print("5. List All Students")
        print("6. Add Grade")
        print("7. View Grades")
        print("8. Statistics")
        print("9. Save Data")
        print("10. Load Data")
        print("0. Exit")
        print("-" * 20)

    def run(self):
        """Start the menu loop. Loads saved data and handles user choices."""
        self._manager.load_from_file()
        while True:
            self.display_header()
            self.display_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.remove_student()
            elif choice == "3":
                self.update_student()
            elif choice == "4":
                self.search_student()
            elif choice == "5":
                self._manager.list_all_students()
            elif choice == "6":
                self.add_grade()
            elif choice == "7":
                self.view_grades()
            elif choice == "8":
                self.show_statistics()
            elif choice == "9":
                self._manager.save_to_file()
            elif choice == "10":
                self._manager.load_from_file()
            elif choice == "0":
                self._manager.save_to_file()
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

            input("\nPress Enter to continue...")

    def add_student(self):
        """Ask the user for student details and add a new student."""
        print("\n--- ADD STUDENT ---")
        sid = input("Student ID: ").strip()
        name = input("Name: ").strip()
        email = input("Email: ").strip()
        phone = input("Phone: ").strip()
        course = input("Course: ").strip()
        year = input("Year (1-4): ").strip()
        if not year.isdigit() or not (1 <= int(year) <= 4):
            print("Invalid year. Must be 1-4.")
            return
        self._manager.add_student(sid, name, email, phone, course, int(year))

    def remove_student(self):
        """Ask for a student ID and remove that student."""
        print("\n--- REMOVE STUDENT ---")
        sid = input("Enter Student ID to remove: ").strip()
        self._manager.remove_student(sid)

    def update_student(self):
        """Ask for a student ID and let the user change their details."""
        print("\n--- UPDATE STUDENT ---")
        sid = input("Enter Student ID to update: ").strip()
        s = self._manager.get_student(sid)
        if not s:
            print(f"Student ID '{sid}' not found.")
            return
        print(f"Current: {s}")
        name = input(f"New name [{s.get_name()}]: ").strip()
        email = input(f"New email [{s.get_email()}]: ").strip()
        phone = input(f"New phone [{s._phone}]: ").strip()
        course = input(f"New course [{s.get_course()}]: ").strip()
        year_str = input(f"New year [{s.get_year()}]: ").strip()
        year = int(year_str) if year_str.isdigit() else None
        self._manager.update_student(
            sid,
            name=name or None,
            email=email or None,
            phone=phone or None,
            course=course or None,
            year=year,
        )

    def search_student(self):
        """Ask for a name or ID and show matching students."""
        print("\n--- SEARCH STUDENT ---")
        query = input("Enter name or ID to search: ").strip()
        results = self._manager.search_student(query)
        if not results:
            print("No matching students found.")
            return
        print(f"\nFound {len(results)} result(s):")
        for s in results:
            print(f"  {s}")

    def add_grade(self):
        """Ask for a student ID, subject and grade, then add the grade."""
        print("\n--- ADD GRADE ---")
        sid = input("Enter Student ID: ").strip()
        subject = input("Subject: ").strip()
        grade_str = input("Grade (0-100): ").strip()
        if not grade_str.replace(".", "").isdigit():
            print("Invalid grade.")
            return
        self._manager.add_grade(sid, subject, float(grade_str))

    def view_grades(self):
        """Ask for a student ID and show all their grades with average."""
        print("\n--- VIEW GRADES ---")
        sid = input("Enter Student ID: ").strip()
        s = self._manager.get_student(sid)
        if not s:
            print(f"Student ID '{sid}' not found.")
            return
        print(f"\nStudent: {s.get_name()} ({s.get_student_id()})")
        grades = s.get_grades()
        if not grades:
            print("No grades recorded yet.")
            return
        print(f"\n{'Subject':<25} {'Grade':<10}")
        print("-" * 35)
        for subj, grade in grades.items():
            print(f"{subj:<25} {grade:<10.1f}")
        print(f"\nAverage: {s.get_average_grade():.1f}")

    def show_statistics(self):
        """Print overall stats: student count, average grade, top student, course distribution."""
        print("\n--- STATISTICS ---")
        stats = self._manager.get_statistics()
        if stats["total"] == 0:
            print("No students to analyze.")
            return
        print(f"Total Students:      {stats['total']}")
        print(f"Overall Avg Grade:   {stats['average']}")
        print(f"Top Student:         {stats['top_student']} ({stats['top_avg']:.1f})")
        print("\nCourse Distribution:")
        for course, count in stats["course_distribution"].items():
            print(f"  {course}: {count} student(s)")


if __name__ == "__main__":
    menu = Menu()
    menu.run()
