import os
from pyairtable import Api
from pyairtable.formulas import match
from dotenv import load_dotenv

load_dotenv()

api = Api(os.getenv('AIRTABLE_PAT'))
table = api.table(os.getenv('BASE_ID'), os.getenv('TABLE_ID'))

def main():
    print("""
    Welcome to Bookshelf Manager.
    What would you like to do?

    (f)etch a book record  
          """)
    
    choice  = input("> ")

    if choice == "f":
        isbn = input("Please enter the ISBN number of the book you are looking for: ")

        searchformula = match({"ISBN": isbn})
        records = table.all(formula=searchformula)

        if not records:
                print("No matching records found.")
        else:
            for record in records:
                print("ISBN: " + record['fields']['ISBN']['text'])
                print("Title: " + record['fields']['Title'])
                print("Author: " + record['fields']['Author'])
    else:
        print("Invalid Selection")

main()