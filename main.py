from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from collections import defaultdict
import json
import os

from wallets import *
from expense_category import *


# ACCOUNT STORAGE

debit_cards = []
credit_cards = []
cash_accounts = []

# LOAD ACCOUNT FROM LOCAL STORAGE

DATA_FILE = "Python\\expense_tracker\\accounts.json"

def load_accounts():
    if not os.path.exists(DATA_FILE):
        return
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

        for acc in data.get('debit_cards', []):
            debit_cards.append(DebitCard.from_dict(acc))
        for acc in data.get('credit_cards', []):
            credit_cards.append(CreditCard.from_dict(acc))
        for acc in data.get('cash_accounts', []):
            cash_accounts.append(Cash.from_dict(acc))
load_accounts()

all_accounts = [debit_cards, credit_cards, cash_accounts]


# ACCOUNT FINDING FUNCTIONS
def find_acc_name(name: str) -> bool:
    for account_list in all_accounts:
        for account in account_list:
            if account.name == name:
                return True
    return False
def get_acc_by_name(name: str) -> object:
    for account_list in all_accounts:
        for account in account_list:
            if account.name == name:
                return account
    return None

# START OF THE MAIN BLOCK

while True:
    print()
    print("\033[35mWelcome to Expense tracker!\033[0m")
    print("1: create an account(wallet)")
    print("2: transfer funds between accounts")
    print("3: record a purchase")
    print("4: pay off credit card debt")
    print("5: manage accounts(wallets)")
    print("6: view purchase history")
    print("7: exit")
    ans = input("Enter the number of operation: ")
    match ans:
        # ACCOUNT CREATION
        case "1":
            print()
            print("\033[34mChoose the type of account to create: \033[0m")
            print("1: debit card")
            print("2: credit card")
            print("3: cash account")
            print("4: exit")
            ans1 = input("Enter the number of operation: ")
            match ans1:
                # DEBIT CREATION            
                case "1":
                    print()
                    while True:
                        name = input("Enter the name of your card: ")
                        if find_acc_name(name):
                            print(f"\033[31mThere already exists an account with the name '{name}'. Please enter a different name.\033[0m")
                        else: break
                    while True:
                        try:
                            balance = float(input("Enter the initial balance of your card: "))
                            break
                        except ValueError:
                            print("\033[31mBalance must be a valid number. Please try again.\033[0m")
                    debit_card: DebitCard = DebitCard(name, balance)
                    debit_cards.append(debit_card)
                    print()
                    print("\033[32mSuccessfully created a debit card account:\033[0m")
                    print(f' {debit_card}')
                # CREDIT CREATION            
                case "2":
                    print()
                    while True:
                        name = input("Enter the name of your card: ")
                        if find_acc_name(name):
                            print(f"\033[31mThere already exists an account with the name '{name}'. Please enter a different name.\033[0m")
                        else: break
                    while(True):
                        try: 
                            limit = int(input("Enter the limit of your card: "))
                            rate = float(input("Enter the interest rate of your card: "))

                            if limit < 0:
                                print("Your limit must be a positive number. Please try again.")
                            else: break
                        except ValueError:
                            print("\033[31mLimit and interest rate must be valid numbers. Please try again.\033[0m")
                    credit_card: CreditCard = CreditCard(name, limit, rate)
                    credit_cards.append(credit_card)
                    print()
                    print("\033[32mSuccessfully created a credit card account:\033[0m")
                    print(f' {credit_card}')

                # CASH CREATION            
                case "3":
                    print()
                    while True:
                        name = input("Enter the name of your card: ")
                        if find_acc_name(name):
                            print(f"\033[31mThere already exists an account with the name '{name}'. Please enter a different name.\033[0m")
                        else: break
                    while True:
                        try:
                            balance = float(input("Enter the initial balance of your card: "))
                            break
                        except ValueError:
                            print("\033[31mBalance must be a valid number. Please try again.\033[0m")
                    cash: Cash = Cash(name, balance)
                    cash_accounts.append(cash)
                    print()
                    print("\033[32mSuccessfully created a cash account:\033[0m")
                    print(f' {cash}')                
                case "4":
                    ...
                case _:
                    print("\033[31mError: wrong command\033[0m")
        # FUND TRANSFER
        case "2":
            acc_name = input("Enter the name of the account you want to transfer money from: ")
            acc_name1 = input("Enter the name of the account you want to transfer money to: ")
            if acc_name == acc_name1:
                print("\033[31mCannot transfer to the same account.\033[0m")
                continue
            transfer_from = get_acc_by_name(acc_name)
            transfer_to = get_acc_by_name(acc_name1)

            if transfer_from and transfer_to:
                while True:
                    try:
                        amount = float(input("Enter the amount to transfer: "))
                        break
                    except ValueError:
                        print("\033[31mTransfer amount must be a valid number. Please try again.\033[0m")
                transfer_from.transfer(transfer_to, amount)  
            elif not transfer_from or not transfer_to:
                print(f"\033[31mNo account under '{acc_name}' and/or '{acc_name1}' was found.\033[0m")
        # PURCHASE FUNCTION
        case "3":
            name = input('Enter the name of the account to make a purchase with: ')

            acc = get_acc_by_name(name)

            if acc:
                purchase_name = input("Enter the name of the purchase: ")
                while True:
                    try:
                        amount = float(input("Enter the amount to transfer: "))
                        break
                    except ValueError:
                        print("\033[31mPurchase amount must be a valid number. Please try again.\033[0m")
                category = input("Enter the category of the purchase: ")
                while True:
                    try:
                        date = input("Enter the date of the purchase (day month year(after 2023)): ").split()
                        if len(date) != 3:
                            raise ValueError
                        date_obj = datetime(day=int(date[0]), month=int(date[1]), year=int(date[2]))
                        if int(date[2]) < 2023:
                            print("\033[31mPlease enter a year after 2023\033[0m")
                        else: break
                    except (ValueError,IndexError):
                        print("\033[31mThe date should include day, month and year which form a valid date. Please try again.\033[0m")
                acc.purchase(amount, category, purchase_name, date_obj)   
            else:
                print(f"\033[31mNo account under the name '{name}' was found\033[0m")   
        # PAY FOR CREDIT CARD            
        case "4":
            name = input("Enter the name of the credit card you want to make payment to: ")
            acc = get_acc_by_name(name)

            if acc and isinstance(acc, CreditCard):
                pay_name = input("Enter the name of the account that pays for the credit card: ")
                pay_acc = get_acc_by_name(pay_name)

                if pay_acc:
                    while True:
                        try:
                            amount = float(input("Enter the amount to pay: "))
                            break
                        except ValueError:
                            print("\033[31mPurchase amount must be a valid number. Please try again.\033[0m")
                    while True:
                        try:
                            date = input("Enter the date of the payment (day month year(after 2023)): ").split()
                            date_obj = datetime(day=int(date[0]), month=int(date[1]), year=int(date[2]))
                            if int(date[2]) < 2023:
                                print("\033[31mPlease enter a year after 2023\033[0m")
                            else: break
                        except ValueError:
                            print("\033[31mThe date should include day, month and year which form a valid date. Please try again.\033[0m")
                    acc.make_payment(pay_acc, amount, date_obj)
                else: print(f"\033[31mThere is no account under the name '{pay_name}'\033[0m")
            elif not acc: print(f"\033[31mThere is no account under the name '{name}'\033[0m")
            elif not isinstance(acc, CreditCard): print(f"\033[31mAccount '{acc.name}' is not a credit card\033[0m")
        # ACCOUNT MANAGEMENT            
        case "5":
            print()
            print("Enter the number of operation: ")
            print("1: show all accounts")
            print("2: delete an account")
            print("3: edit account details")
            print("4: show purchase history for a specific account")
            print("5: exit")
            ans1 = input("Enter the number of operation: ")
            match ans1:
                # SHOW ALL ACCOUNTS            
                case "1":
                    print()
                    print("Debit cards: ")
                    if not debit_cards:
                        print(" No debit cards found")
                    else:
                        for i in debit_cards:
                            print(f'-{i}')
                    print()
                    print("Credit cards: ")
                    if not credit_cards:
                        print(" No credit cards found")
                    else:
                        for i in credit_cards:
                            print(f'-{i}')
                    print()
                    print("Cash accounts: ")
                    if not cash_accounts:
                        print(" No cash accounts found")
                    else:
                        for i in cash_accounts:
                            print(f'-{i}')
                # DELETE ACCOUNT           
                case "2":
                    name = input('Enter the name of the account you want to delete: ')
                    deleted = False
                    for account_list in all_accounts:
                        for account in account_list[:]:
                            if account.name == name:
                                account_list.remove(account)
                                deleted = True
                                print(f"\033[32mAccount under the name '{name}' deleted successfully.\033[0m")
                                break
                        if deleted:
                            break
                    if not deleted:
                        print(f"\033[31mNo account under the name '{name}' was found\033[0m")
                # EDIT ACCOUNT          
                case "3":
                    name = input('Enter the name of the account you want to edit: ')
                    acc = get_acc_by_name(name)
                    if acc:
                        # EDIT DEBIT CARD/CASH
                        if isinstance(acc, DebitCard) or isinstance(acc, Cash):
                            while True:
                                char = input('Enter the characteristic you want to change (name, balance): ')
                                match char:
                                    case "name":
                                        new_name = input(f'Enter the new name for the account "{name}": ')
                                        name_taken = find_acc_name(new_name)
                                        if name_taken:
                                            print("\033[31mThis name is already taken by a different account. Please enter a different name\033[0m")
                                        else:
                                            acc.name = new_name
                                            print(f"\033[32mAccount's name successfully changed to '{acc.name}'\033[0m")
                                            break
                                    case "balance":
                                        try:
                                            new_balance = float(input(f'Enter the new balance for the account "{name}": '))
                                            if new_balance < 0:
                                                print("\033[31mThe new balance must be a positive number. Please try again\033[0m")
                                                continue
                                            acc.balance = new_balance
                                            print(f"\033[32mAccount's balance successfully changed to '{acc.balance}'.\033[0m")
                                            break
                                        except ValueError:
                                            print("\033[31mInvalid input. Please try again\033[0m")
                                    case _:
                                        print(f"\033[31mThere is no such characteristic as '{char}'. Please enter either 'name' or 'balance'.\033[0m")
                        # EDIT CREDIT CARD
                        elif isinstance(acc, CreditCard):
                            while True:
                                char = input('Enter the characteristic you want to change (name, limit, rate): ')
                                match char:
                                    case "name":
                                        new_name = input(f'Enter the new name for the account "{name}": ')
                                        name_taken = find_acc_name(new_name)
                                        if name_taken:
                                            print("\033[31mThis name is already taken by a different account. Please enter a different name\033[0m")
                                        else:
                                            acc.name = new_name
                                            print(f"\033[32mAccount's name successfully changed to '{acc.name}'\033[0m")
                                            break
                                    case "rate":
                                        try:
                                            new_rate = float(input(f'Enter the new rate for the account "{name}": '))
                                            if new_rate < 0:
                                                print("\033[31mThe new rate must be a positive number. Please try again.\033[0m")
                                                continue
                                            acc.interest_rate = new_rate
                                            print(f"\033[32mAccount's rate successfully changed to '{acc.interest_rate}'.\033[0m")
                                            break
                                        except ValueError:
                                            print("\033[31mInvalid input. Please try again.\033[0m")
                                    case "limit":
                                        try:
                                            new_limit = int(input(f'Enter the new limit for the account "{name}": '))
                                            if new_limit < 0:
                                                print("\033[31mThe new limit must be a positive number. Please try again.\033[0m")
                                                continue
                                            acc.credit_limit = new_limit
                                            print(f"\033[32mAccount's limit successfully changed to '{acc.credit_limit}'.\033[0m")
                                            break
                                        except ValueError:
                                            print("\033[31mInvalid input. Please try again.\033[0m")
                                    case _:
                                        print(f"\033[31mThere is no such characteristic as '{char}'. Please enter either 'name', 'limit' or 'rate'.\033[0m")
                        else: print(f'033[31mThere is no account under the name {name}033[0m')
                # PURCHASES OF AN ACCOUNT         
                case '4':
                    name = input("Enter the name of the account you wish to view purchase history of: ")
                    acc = get_acc_by_name(name)
                    if acc:
                        acc.print_purchase_list()
                case '5':
                    ...
        case "6":
            print_categories()
        case "7":
            break
        case _:
            print("\033[31mError: wrong command\033[0m")

# SAVE ALL ACCOUNT INFO BEFORE EXIT
def save_accounts():
    data = {
        "debit_cards": [account.to_dict() for account in debit_cards],
        "credit_cards": [account.to_dict() for account in credit_cards],
        "cash_accounts": [account.to_dict() for account in cash_accounts]
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=5)

save_accounts()
print("End of operation")
