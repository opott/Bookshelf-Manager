import os
import time
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
    (c)reate a book record
    (e)dit a book record
    (d)elete a book record
          """)

    choice = input("> ")

    if choice == "f":
        isbn = input(
            "Please enter the ISBN number of the book you are looking for: ")

        searchformula = match({"ISBN": isbn})
        records = table.all(formula=searchformula)

        if not records:
            print("No matching records found.")
        else:
            for record in records:
                print("ISBN: " + record['fields']['ISBN']['text'])
                print("Title: " + record['fields']['Title'])
                print("Author: " + record['fields']['Author'])
                print("Shelf: " + record['fields']['Shelf'])
                print("Available: " + record['fields']['Available'])

        time.sleep(3)

    elif choice == "c":
        isbn = int(input("Please enter the ISBN number of the book: "))
        title = input("Please enter the title of the book: ")
        author = input("Please enter the author of the book: ")
        shelf = input("Please enter the bookshelf: ")
        available = input("Available? (y/n): ")

        while available not in ["y", "n"]:
            print(
                "Invalid input for availability. Please enter either 'y' or 'n'."
            )
            available = input("Available? (y/n): ")

        if available == "y":
            available = "Yes"
        else:
            available = "No"

        table.create({
            'ISBN': isbn,
            'Title': title,
            'Author': author,
            'Shelf': shelf,
            'Available': available
        })
        print("Record created sucessfully.")

        time.sleep(3)

    elif choice == "e":
        isbn = int(
            input(
                "Please enter the ISBN number of the book you want to edit: "))

        searchformula = match({"ISBN": isbn})
        records = table.all(formula=searchformula)

        if not records:
            print("No matching records found.")
        else:
            for record in records:
                id = record['id']

        title = input("Please enter the new title: ")
        author = input("Please enter the new author: ")
        shelf = input("Please enter the new shelf: ")
        available = input("Please enter the new availability (y/n): ")

        while available not in ["y", "n"]:
            print(
                "Invalid input for availability. Please enter either 'y' or 'n'."
            )
            available = input("Available? (y/n): ")

        if available == "y":
            available = "Yes"
        else:
            available = "No"

        table.update(
            id, {
                'Title': title,
                'Author': author,
                'Shelf': shelf,
                'Available': available
            })
        print("Record updated sucessfully.")

    elif choice == "d":
        isbn = int(
            input(
                "Please enter the ISBN number of the book you want to delete: "
            ))

        searchformula = match({"ISBN": isbn})
        records = table.all(formula=searchformula)

        if not records:
            print("No matching records found.")
        else:
            for record in records:
                id = record['id']

        print("Are you sure you wish to delete this record? (y/n)")
        confirm = input("Confirm deletion: ")

        while confirm not in ["y", "n"]:
            print(
                "Invalid input for confirmation. Please enter either 'y' or 'n'."
            )
            confirm = input("Confirm deletion: ")

        if confirm == "y":
            table.delete(id)
            print("Record deleted sucessfully.")
            time.sleep(3)
        elif confirm == "n":
            print("Deletion cancelled.")
            time.sleep(3)
        else:
            print("Invalid input.")
            time.sleep(3)

    else:
        print("Invalid Selection")
        time.sleep(3)


while True:
    main()
