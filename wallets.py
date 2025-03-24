from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP


from expense_category import *

def round2(n):
    return float(Decimal(n).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

# WALLET (abstract class)            
class Wallet(ABC):
    wallet_count = 0
    def __init__(self,name: str, balance: float) -> None:
        self.balance = balance
        Wallet.wallet_count+=1
        self.name = name

    def __str__(self):
        return f' Account name: {self.name}\n'
    
    def transfer(self, other, amount: float) -> None:
        if isinstance(other, CreditCard) or isinstance(self, CreditCard):
            print("Cannot transfer money to or from a credit card")
        elif amount > self.balance:
            print("Insufficient funds")
        elif amount <= 0:
            print("The amount must be a positive number.")

        else:
            self.balance -= amount
            other.balance += amount
            print('Transfer success')
    
    @abstractmethod
    def purchase(self, amount: float, category: str, name: str, date: datetime) -> None:
        pass

    def print_purchase_list(self) -> None:
        print(f"Purchase list for the account '{self.name}': ")
        for exp in sorted(self.purchase_list, key=lambda x: x.date):
            print(f" - {exp}, Remaining: {exp.remaining}")


# DEBIT
class DebitCard(Wallet):
    debit_card_count = 0
    def __init__(self, name: str, balance: float) -> None:
        DebitCard.debit_card_count +=1
        super().__init__(name, balance)
        self.type = "Debit card"
        self.purchase_list = []


    def __str__(self):
        return super().__str__() + f'  Account type: {self.type}\n  Account balance: {self.balance}\n'

    def transfer(self, other, amount: float) -> None:
        super().transfer(other, amount)

    def purchase(self, amount: float, category: str, name: str, date: datetime) -> None:
        if amount < 0:
            print("The amount must be a positive number")
        elif amount > self.balance:
            print("Insufficient funds")
        else:
            self.balance-=amount
            exp: Expense = Expense(name, category, amount, date, payment_method = "debit card")
            category = category.strip().capitalize()
            categories[category].append(exp)
            self.purchase_list.append(exp)
            exp.remaining = 0
            print("Purchase success")
    def print_purchase_list(self):
        return super().print_purchase_list()


# CREDIT
class CreditCard(Wallet):
    credit_card_count = 0

    def __init__(self, name: str, limit: int, rate: float) -> None:
        CreditCard.credit_card_count +=1
        super().__init__(name, 0)
        self.type = "Credit card"
        self.credit_limit = limit
        self.interest_rate = rate
        self.purchase_list = []

    def __str__(self):
        return super().__str__() + f'  Account type: {self.type}\n  Outstanding balance: {self.calc_outstanding_balance()}\n  Credit limit: {self.credit_limit}\n  Interest rate: {self.interest_rate}'
    
    def purchase(self, amount: float, category: str, name: str, date: datetime) -> None:
        outstanding = self.calc_outstanding_balance()
        if outstanding > self.credit_limit:
            print(f'You have exceeded your credit card limit. Limit: "{self.credit_limit}". Outstanding balance: "{outstanding}"')
            return
        if amount < 0:
            print("The amount must be a positive number")
            return
        
        exp: Expense = Expense(name, category, amount, date, "credit card")

        category = category.strip().capitalize()
        categories[category].append(exp)
        self.purchase_list.append(exp)

        print("Purchase success")


    def calc_outstanding_balance(self) -> float:
        def months_between(start_date: datetime, end_date: datetime) -> int:
            return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

        now = datetime.now()
        result = 0
        monthly_rate = self.interest_rate / 12

        for exp in self.purchase_list:
            if exp.remaining == 0:
                continue
            months_passed = months_between(exp.last_payment_date, now)
            if months_passed > 0:
                total_due = exp.remaining * pow(1 + monthly_rate, months_passed)
            else:
                total_due = exp.remaining
            exp.total_amount = total_due
            
            result += total_due

        return round2(result)

    
    def make_payment(self, other, amount: float, date: datetime) -> None:
        if isinstance(other, CreditCard):
            print("You cannot make payment from another credit card")
            return

        outstanding = self.calc_outstanding_balance()
        print(f"Outstanding balance: {outstanding}")

        if amount > other.balance:
            print("Insufficient funds")
            return
        elif amount > outstanding:
            print(f"The amount must be less than or equal to the outstanding balance, which is currently: {outstanding}")
            return
        elif amount <= 0:
            print("The amount must be a positive number")
            return

        for exp in sorted(self.purchase_list, key=lambda x: x.date):
            if exp.date > date:
                print("Date error. You cannot register a credit card payment on the day prior to the day of the first unpaid purchase")
                return 
            if amount <= 0:
                break
            if exp.total_amount > 0:
                payment_applied = min(amount, exp.total_amount)
                exp.total_amount -= payment_applied
                amount -= payment_applied
                exp.remaining = exp.total_amount
                exp.last_payment_date = date
        other.balance -= amount
                
        new_outstanding = self.calc_outstanding_balance()
        print(f"Payment success. Current outstanding balance: {new_outstanding}")

    def print_purchase_list(self):
        return super().print_purchase_list()

# CASH
class Cash(Wallet):
    cash_count = 0
    def __init__(self, name, balance) -> None:
        Cash.cash_count +=1
        super().__init__(name, balance)
        self.type = "Cash"
        self.purchase_list = []

    def __str__(self):
        return super().__str__() + f'  Account type: {self.type}\n  Account balance: {self.balance}\n'

    def transfer(self, other, amount: float) -> None:
        super().transfer(other, amount)

    def purchase(self, amount: float, category: str, name: str, date: datetime) -> None:
        if amount < 0:
            print("The amount must be a positive number")
        elif amount > self.balance:
            print("Insufficient funds")
        else:
            self.balance-=amount
            print("Purchase success")
            exp: Expense = Expense(name, category, amount, date, "cash")
            category = category.strip().capitalize()
            categories[category].append(exp)
            exp.remaining = 0
            self.purchase_list.append(exp)
    def print_purchase_list(self):
        return super().print_purchase_list()


