import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_categotry, get_date, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_File = "Finance_data.csv"
    dateformat = "%d-%m-%Y"
    COLUMNS = ["Date", "Amount","Category","Description"]

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_File)
        except FileNotFoundError: 
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_File, index=False)

    @classmethod
    def add_entry(cls,date,amount,category,description):
        new_entry = {
            "Date": date,
            "Amount":amount,
            "Category": category,
            "Description": description
        }
        with open(cls.CSV_File,"a",newline="") as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry add successfully")


    @classmethod
    def get_transactions(cls,start_date, end_date):
        df = pd.read_csv(cls.CSV_File)
        df["Date"] = pd.to_datetime(df["Date"],format=CSV.dateformat)
        start_date = datetime.strptime(start_date,CSV.dateformat)
        end_date = datetime.strptime(end_date,CSV.dateformat)

        mask =  (df["Date"] >= start_date) & (df["Date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transaction found in the given data range")
        else:
            print(f"Transaction from {start_date.strftime(CSV.dateformat)} to {end_date.strftime(CSV.dateformat)}")
            print (filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.dateformat)}))

            total_income = filtered_df[filtered_df["Category"] == "Income"]["Amount"].sum()
            total_expense = filtered_df[filtered_df["Category"] == "Expense"]["Amount"].sum()
            print("\nSummary: ")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income-total_expense):.2f}")

            return filtered_df



def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default=True,)
    amount = get_amount()
    category = get_categotry()
    description = get_description()

    CSV.add_entry(date,amount, category,description)

def plot_transaction(df):
    df.set_index("Date",inplace=True)

    income_df = df[df["Category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["Category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(15,10))
    plt.plot(income_df.index, income_df["Amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["Amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title('Income and Expense Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

def pie_transaction(df):

    labels = "Net Sum", "Expense"
    sizes = [(df[df["Category"] == "Income"]["Amount"].sum()-df[df["Category"] == "Expense"]["Amount"].sum()),df[df["Category"] == "Expense"]["Amount"].sum()]

    fig, ax = plt.subplots()
    ax.pie(sizes,labels=labels,autopct='%1.1f%%')
    fig.show()


def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transaction and summary within a date rane")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ",allow_default=True)
            df = CSV.get_transactions(start_date,end_date)
            if input("Do you want to see plot? (y/n)").lower() == "y":
                plot_transaction(df)
            if input("Do you want to see Pie? (y/n)").lower() == "y":
                pie_transaction(df)
        elif choice == "3":
            print("Existing....Bye!")
            break
        else:
            print("Invalid choice. Enter 1 , 2, or 3")

if __name__ == "__main__":
    main()