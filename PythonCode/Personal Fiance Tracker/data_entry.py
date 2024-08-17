from datetime import datetime

dateformate = "%d-%m-%Y"
CATEGORIES = {"I":"Income","E":"Expense"}

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(dateformate)
    
    try:
        valid_date = datetime.strptime(date_str,dateformate)
        return valid_date.strftime(dateformate)
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyy format")
        return get_date(prompt,allow_default)

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a non-negative non-zero value")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_categotry():
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    
    print("Invalid catefory. Pleae enter 'I' for Income or 'E' for Expense.")
    return get_categotry()

def get_description():
    return input("Enter a description (optional): ")



