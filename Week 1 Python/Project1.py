#Student ReportCard Generator


class srg:
    
    def __init__(self,std_id,std_name,no_of_sub):
        self.details={}
        self.student_id=std_id
        self.student_name=std_name
        self.details["student_id"]=std_id
        self.details["name"]=std_name
        self.no_of_sub=no_of_sub
        self.details["sub_mark"]={}
        self.grd=""
        self.avg=0

    def sub_mark(self,subject,mark):
        self.details["sub_mark"][subject]=mark

    def average(self):
        self.avg=0
        for key,value in self.details["sub_mark"].items():
            self.avg+=value

        self.avg=self.avg//self.no_of_sub
        return self.avg

    def grade(self):
        if self.avg >=90:
            self.grd="A"
        elif self.avg>=70:
            self.grd="B"
        elif self.avg>=50:
            self.grd="C"
        else:
            self.grd="F"
        return self.grd

    def view_report_card(self):
        print("                                     Report Card                                                 ")
        print()
        print(f"                                    Haii {self.student_name}                                    ")
        print()
        print("-------------------------------------------------------------------------------------------------")
        print()
        print(f"                            you scored {self.average()} as average                              ")
        print()
        print("-------------------------------------------------------------------------------------------------")
        print()
        print(f"                               So your grade is {self.grade()}                                  ")
        


def report_card_generator():
    flag_id=True
    flag_name=True
    flag_count=True
    flag_sub_marks=True
    obj_created=False
    while(True):
        if flag_id:
            try:
                std_id=int(input("Enter your student id:"))
                flag_id=False
            except Exception:
                print(f"please verify your student id {std_id}")
                flag_id=True
                continue
        if flag_name:
            try:
                std_name=input("Enter your name:")
                flag_name=False
            except Exception:
                print(f"please verify your student name {std_name}")
                flag_name=True
                continue
        if flag_count:
            try:
                no_of_sub=int(input("Enter the number of subject"))
                flag_count=False
            except Exception:
                print(f"please verify your subcount {no_of_sub}")
                flag_count=True
                continue
        if obj_created==False:
            std=srg(std_id,std_name,no_of_sub)
            obj_created=True
        if flag_sub_marks:
            try:
                for i in range(no_of_sub):
                    subject=input(f"Enter your {i+1}th subject : ")
                    mark=int(input(f"Enter you mark on {subject} : "))
                    std.sub_mark(subject,mark)
                flag_sub_marks=False
            except Exception:
                print(f"Be carefull while entring the marks else you have to reenter")
                flag_sub_marks=True
                continue
        
        if flag_id==False and flag_name==False and flag_count==False and flag_sub_marks==False:
            std.view_report_card()
            break

if __name__=="__main__":
    report_card_generator()