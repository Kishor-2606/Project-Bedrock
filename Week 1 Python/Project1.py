#Student ReportCard Generator


class Student:
    def __init__(self,std_id,std_name,subject_marks):
        self.student_id=std_id
        self.student_name=std_name
        self.subjects_marks=subject_marks

    def calculate_average(self):
        return (sum(self.subjects_marks.values()))/len(self.subjects_marks)

    def calculate_grade(self,average):
        if average >=90:
            return average,"A"
        elif average>=70:
            return average,"B"
        elif average>=50:
            return average,"C"
        else:
            return average,"F"

class Application:

    def __init__(self):
        student_id,student_name,no_of_sub=self.get_student_details()
        
        subject_marks=self.get_marks(no_of_sub)

        self.student=Student(student_id,student_name,subject_marks)
    
    

    def generate_report(self):
            average=self.calculate_average()
            grade=self.student.calculate_grade(average)
            return{
                "student_id":self.student.student_id,
                "student_name":self.student.student_name,
                "average":average,
                "grade":grade
            }

    def report_card_presentation(self,report):
        print("===================================================")
        print("                   Report Card                     ")
        print("===================================================")
        print("       Student ID : ",report["student_id"])
        print("       Name       : ",report["student_name"])
        print("       Average    : ",report["average"])
        print("       Grade      : ",report["grade"])

    
  
    def get_student_details(self):
        while True:
            try:
                std_id=int(input("Enter your student id :"))
                if std_id<=0:
                    print("Please enter the valid student_id ")
                    continue
            except ValueError:
                print(f"please verify your student id ")
            else:
                break

        while True:
            try:
                std_name=input("Enter your name :")
                if std_name=="":
                    print("Please enter the valid name")
                    continue
            except ValueError:
                print(f"please verify your student name {std_name}")
            else:
                break
        while True:
            try:
                no_of_sub=int(input("Enter the number of subject :"))
                if no_of_sub<0 or no_of_sub>10:
                    print("Please enter the valid subject count")
                    continue
            except ValueError:
                print(f"please verify your subcount {no_of_sub}")
            else:
                break

        return std_id,std_name,no_of_sub

    def get_marks(self,no_of_sub):
        subject_marks={}
        i=0
        while i<(no_of_sub):
            try:
                subject=input(f"Enter your {i+1}th subject : ")
                if subject=="":
                    print("please enter the valid subject name")
                    continue
                if subject in subject_marks:
                    print("This subject already exhist")
                    continue

                mark=int(input(f"Enter you mark on {subject} : "))
                if mark<0 or mark>100:
                    print("Please enter the valid marks")
                    continue
                
            except ValueError:
                print("Please enter the valid subject name and marks")
            else:
                i=i+1
                subject_marks[subject]=mark
        return subject_marks

app=Application()

report=app.generate_report()


app.report_card_presentation(report)

