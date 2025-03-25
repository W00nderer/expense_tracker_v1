from datetime import datetime, timedelta
from collections import defaultdict

categories = defaultdict(list)

class Expense(): 
    def __init__(self, name: str, category: str, amount: float, date: datetime, payment_method: str) -> None:
        self.name = name
        self.category = category
        self.amount = amount
        self.date = date
        self.payment_method = payment_method
        self.total_amount = amount
        self.remaining = amount
        self.last_payment_date = date

    def to_dict(self):
        return{
            "name": self.name,
            "category": self.category,
            "amount": self.amount,
            "date": self.date.strftime("%d-%m-%Y"),
            "payment_method": self.payment_method,
            "total_amount": self.total_amount,
            "remaining": self.remaining,
            "last_payment_date": self.last_payment_date.strftime("%d-%m-%Y")
        }
    
    @staticmethod
    def from_dict(data):
        expense = Expense(
            data["name"],
            data["category"],
            data["amount"],
            datetime.strptime(data["date"], "%d-%m-%Y"),
            data["payment_method"]
        )
        expense.total_amount = data.get("total_amount", data["amount"]) 
        expense.remaining = data.get("remaining", data["amount"])
        expense.last_payment_date = datetime.strptime(data.get("last_payment_date", data["date"]), "%d-%m-%Y")
        cat = expense.category.strip().capitalize()
        categories[cat].append(expense)
        return expense
    
    def __str__(self):
        return f'Name: {self.name}, Category: {self.category}, Amount: {self.amount}, Date: {self.date.strftime("%d-%m-%Y")}, Payment method: {self.payment_method}'

def print_categories() -> None:
    for category, expenses in categories.items():
        print(f"Category: {category}")
        if not expenses:
            print(" No record")
        else:
            for exp in sorted(expenses, key=lambda x: x.date):
                print(f" - {exp}")
        print()