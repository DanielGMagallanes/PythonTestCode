import pandas as pd
import csv
from datetime import datetime


class CSV:
    CSV_File = "Finance_data.csv"

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


CSV.initialize_csv()
CSV.add_entry("19-07-2024",1230.65,"Income","Payday")
CSV.add_entry("20-07-2024",117.43,"Expense","Food")