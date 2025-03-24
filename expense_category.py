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
    def __str__(self):
        return f'Name: {self.name}, Category: {self.category}, Amount: {self.amount}, Date: {self.date.strftime("%d-%m-%Y")}, Payment method: {self.payment_method}'

def print_categories() -> None:
    for category, expenses in categories.items():
        print(f"Category: {category}")
        if not expenses:
            print(" No record")
        else:
            for exp in expenses:
                print(f" - {exp}")
        print()