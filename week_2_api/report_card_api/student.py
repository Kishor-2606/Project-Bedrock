class Student:

    def __init__(self, student_id, student_name, subject_marks):
        self.student_id = student_id
        self.student_name = student_name
        self.subject_marks = subject_marks

    def calculate_average(self):
        return round(sum(self.subject_marks.values()) / len(self.subject_marks))

    def calculate_grade(self, average):
        if average >= 90:
            return "A"
        elif average >= 70:
            return "B"
        elif average >= 50:
            return "C"
        return "F"

    def generate_report(self):
        average = self.calculate_average()

        return {
            "student_id": self.student_id,
            "student_name": self.student_name,
            "average": average,
            "grade": self.calculate_grade(average)
        }