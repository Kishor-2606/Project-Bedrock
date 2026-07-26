#Personal Expense Tracker
class Expense:
    def __init__(self,expense_title,expense_price,expense_category):
        self.expense_title=expense_title
        self.expense_price=expense_price
        self.expense_category=expense_category

class ExpenseTracker:

    def __init__(self):
        self.expense_collection=[]

    def add_expense_obj(self,expense_obj):
        self.expense_collection.append(expense_obj)

    def get_expenses(self):
        return self.expense_collection

    def delete_expense(self,expense_delete):
        flag=False
        deleted_expense=[]
        for expense in self.expense_collection:
            if expense.expense_title==expense_delete:
                deleted_expense.append(expense)
                flag=True
        for expense in deleted_expense:
            if expense in self.expense_collection:
                self.expense_collection.remove(expense)
        return flag,len(deleted_expense)

    def show_total(self):
        total=0
        for expense in self.expense_collection:
            total+=expense.expense_price
        return total

    def filter_title(self,filter_title):
        filtered_obj=[]
        for expense in self.expense_collection:
            if expense.expense_title==filter_title:
                filtered_obj.append(expense)
        return filtered_obj
    
    def filter_price(self,price_min,price_max):
        filtered_obj=[]
        for expense in self.expense_collection:
            if (expense.expense_price>=price_min) and (expense.expense_price<=price_max):
                filtered_obj.append(expense)
        return filtered_obj

    def filter_category(self,filter_category):
        filtered_obj=[]
        for expense in self.expense_collection:
            if expense.expense_category==filter_category:
                filtered_obj.append(expense)
        return filtered_obj


class Application:

    def __init__(self):
        self.tracker=ExpenseTracker()

    def display_total(self,total):
        print(f"total   {total}")

    def view_all_expenses(self):
        for expense in self.tracker.get_expenses():
            print(f"{expense.expense_title}   {expense.expense_price}   {expense.expense_category}")

    def display_filtered_expense(self,expenses):
        if len(expenses)==0:
            print("No matching expense found.")
        for expense in expenses:
            print(f"{expense.expense_title}   {expense.expense_price}   {expense.expense_category}")

    def menu_options(self,option):
        if option==1:
            expense_title,expense_price,expense_category=self.add_expense()
            expense_obj=Expense(expense_title,expense_price,expense_category)
            self.tracker.add_expense_obj(expense_obj)
            
        elif option==2:
            while True:
                try:
                    expense_delete=input("Enter the expense title to delete :").lower().strip()
                    if expense_delete=="":
                        print("Please enter the valid expense")
                        continue
                except ValueError:
                    print("Please enter the valid expense title")
                    continue
                else:
                    delete,count=self.tracker.delete_expense(expense_delete)
                    if delete:
                        print(f"deleted {count} expenses successfully")
                    else:
                        print(f"expense {expense_delete} doen't exhist")
                        break
        elif option==3:
            total=self.tracker.show_total()
            self.display_total(total)
        elif option==4:
            while True:
                try:
                    filter_option=int(input("""Press 1 to filter with expense title :
                    Press 2 to filter with expense price :
                    Press 3 to filter with expense category """))
                    if filter_option<1 or filter_option>3:
                        print("Please enter the valid option")
                        continue
                except ValueError:
                    print("Please enter valid filter")
                    continue
                else:
                    if filter_option==1:
                        while True:
                            try:
                                filter_title=input("enter the expense title").lower().strip()
                                if filter_title=="":
                                    print("Please enter the valid title")
                                    continue
                            except ValueError:
                                print("Please enter valid title")
                                continue
                            else:
                                expenses=self.tracker.filter_title(filter_title)
                                break
                    if filter_option==2:
                        while True:
                            try:
                                price_min=float(input("enter the min price"))
                                price_max=float(input("enter the max price"))
                                if price_min<1 or price_max<1 or price_max<price_min:
                                    print("Please enter the valid price")
                                    continue
                            except ValueError:
                                print("Please enter valid price")
                                continue
                            else:
                                expenses=self.tracker.filter_price(price_min,price_max)
                                break

                    if filter_option==3:
                        while True:
                            try:
                                filter_category=(input("enter the expense category").lower()).strip()
                                if filter_category=="":
                                    print("Please enter the valid category")
                                    continue
                            except ValueError:
                                print("Please enter valid category")
                                continue
                            else:
                                expenses=self.tracker.filter_category(filter_category)
                                break
                    self.display_filtered_expense(expenses)
                    break
        elif option==5:
            self.view_all_expenses()

    def menu(self):
        while True:
            try:
                option=int(input("""
                Press 1 to ADD EXPENSE
                Press 2 to DELETE EXPENSE
                Press 3 to SHOW TOTAL
                Press 4 to FILTER
                Press 5 to VIEW EXPENSES
                Press 6 to QUIT
                """))

                if option==6:
                    print("Thank you!, Come again")
                    break
                if option<1 or option>6:
                    print("please enter the valid option")
                    continue
            except ValueError:
                print("Enter the valid option")
                continue
            else:
                self.menu_options(option)

    def add_expense(self):
        print("This is your Expense Tracker")
        while True:
            try:
                expense_title=input("Enter your expense title : ").strip()
                if expense_title=="":
                    continue
                elif (expense_title.replace(" ","").isdigit()):
                    print("Please enter the valid expense Title")
                    continue
                else:
                    expense_title=expense_title.lower()
            except ValueError:
                print("Please enter the valid expense Title")
                continue
            else:
                break
        while True:
            try:
                expense_price=float(input("Enter your expense price : "))
                if expense_price<=0:
                    continue
            except ValueError:
                print("Please enter the valid expense price")
                continue
            else:
                break
        while True:
            try:
                expense_category=input("describe your expense category in single word like(food,travel,house rent,snack,entertainment,etc..): ").strip()
                if expense_category=="":
                    continue
                elif (expense_category.replace(" ","").isdigit()):
                    print("Please enter the valid expense category")
                    continue
                else:
                    expense_category=expense_category.lower()
            except ValueError:
                print("Please enter the valid expense category")
                continue
            else:
                break
        return expense_title,expense_price,expense_category

if __name__=="__main__":
    app=Application()
    app.menu()

        