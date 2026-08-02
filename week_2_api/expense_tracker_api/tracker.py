from expense import Expense


class ExpenseTracker:

    def __init__(self):
        self.expenses = []
        self.next_id = 1

    def add_expense(self, title, price, category):

        expense = Expense(
            self.next_id,
            title,
            price,
            category
        )

        self.expenses.append(expense)
        self.next_id += 1

        return expense

    def get_all_expenses(self):
        return self.expenses

    def get_expense(self, expense_id):

        for expense in self.expenses:
            if expense.id == expense_id:
                return expense

        return None

    def delete_expense(self, expense_id):

        for expense in self.expenses:

            if expense.id == expense_id:
                self.expenses.remove(expense)
                return True

        return False

    def calculate_total(self):

        total = 0

        for expense in self.expenses:
            total += expense.price

        return total

    def filter_by_title(self, title):

        result = []

        for expense in self.expenses:
            if expense.title.lower() == title.lower():
                result.append(expense)

        return result

    def filter_by_category(self, category):

        result = []

        for expense in self.expenses:
            if expense.category.lower() == category.lower():
                result.append(expense)

        return result

    def filter_by_price(self, min_price, max_price):

        result = []

        for expense in self.expenses:

            if min_price <= expense.price <= max_price:
                result.append(expense)

        return result

    def update_expense(
        self,
        expense_id,
        title=None,
        price=None,
        category=None
    ):

        expense = self.get_expense(expense_id)

        if expense is None:
            return None

        if title is not None:
            expense.title = title

        if price is not None:
            expense.price = price

        if category is not None:
            expense.category = category

        return expense