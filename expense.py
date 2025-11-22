import csv
from datetime import datetime

# File to store data
FILENAME = "expenses.csv"

# Function to ensure the file is ready
def start_app():
    try:
        # Try to open the file in exclusive creation mode 'x'
        # This fails if the file already exists
        with open(FILENAME, "x", newline="") as f:
            wr = csv.writer(f)
            wr.writerow(["Date", "Category", "Amount", "Note"])
    except FileExistsError:
        # If file exists, do nothing
        pass

def add_data():
    # Get today's date automatically
    d = datetime.now().strftime("%Y-%m-%d")
    
    print("\n" + "="*30)
    print("      ADD NEW EXPENSE")
    print("="*30)
    
    print("Category (Food, Travel, etc): ", end="")
    c = input()
    
    # Need to make sure amount is a number
    try:
        print("Amount: ", end="")
        a = float(input())
    except:
        print("Error: Amount must be a number!")
        return

    print("Note (optional): ", end="")
    n = input()

    # Append to CSV
    with open(FILENAME, "a", newline="") as f:
        wr = csv.writer(f)
        wr.writerow([d, c, a, n])
    
    print("-" * 30)
    print("Saved Successfully!")
    print("-" * 30)

def view_list():
    print("\n" + "="*40)
    print("           YOUR EXPENSES")
    print("="*40)
    try:
        with open(FILENAME, "r") as f:
            rd = csv.reader(f)
            temp_data = list(rd)
            
            # Check if file is empty (just header)
            if len(temp_data) <= 1:
                print("No expenses yet.")
                return

            # Header for the table
            print(f"{'No.':<4} | {'Date':<12} | {'Category':<10} | {'Amount':<10}")
            print("-" * 45)

            # Skip the first row (header)
            # Enumerate starts from 1 to show user-friendly numbers
            for index, item in enumerate(temp_data[1:], start=1):
                # Using f-string for nice alignment
                # :<12 means align left with 12 spaces padding
                print(f"{index:<4} | {item[0]:<12} | {item[1]:<10} | Rs. {item[2]}")
                
    except FileNotFoundError:
        print("File not found. Add an expense first.")
    print("="*40)

def delete_data():
    print("\n" + "="*30)
    print("      DELETE EXPENSE")
    print("="*30)
    try:
        # 1. Read all data
        with open(FILENAME, "r") as f:
            rd = csv.reader(f)
            all_rows = list(rd)

        if len(all_rows) <= 1:
            print("Nothing to delete.")
            return

        # 2. Show options
        # Skip header for display
        for i, row in enumerate(all_rows[1:], start=1):
            print(f"[{i}] {row[1]} - Rs. {row[2]} ({row[0]})")

        # 3. Ask user
        try:
            print("-" * 30)
            print("Enter number to delete: ", end="")
            num = int(input())
            
            # Validate choice (must be between 1 and list length)
            if 1 <= num <= len(all_rows) - 1:
                removed = all_rows.pop(num) # remove the item
                print(f"Deleted: {removed[1]} - Rs. {removed[2]}")
                
                # 4. Save back to file
                with open(FILENAME, "w", newline="") as f:
                    wr = csv.writer(f)
                    wr.writerows(all_rows)
            else:
                print("Invalid number.")
                
        except ValueError:
            print("Please enter a valid number.")

    except FileNotFoundError:
        print("File not found.")

def calc_sum():
    s = 0.0
    try:
        with open(FILENAME, "r") as f:
            rd = csv.reader(f)
            next(f) # Skip header line
            
            for x in rd:
                if len(x) > 0: # Check for empty lines
                    s = s + float(x[2])
        
        print("\n" + "*"*30)            
        print(f" TOTAL SPENT: Rs. {s}")
        print("*"*30)
    except:
        print("Could not calculate total.")

def search_cat():
    print("Enter category name to search: ", end="")
    query = input().lower()
    subtotal = 0
    flag = False
    
    print(f"\n--- Expenses for '{query}' ---")
    print("-" * 30)
    try:
        with open(FILENAME, "r") as f:
            rd = csv.reader(f)
            next(f) # skip header
            
            for row in rd:
                # Compare lowercase to match even if user types differently
                if row[1].lower() == query:
                    print(f"{row[0]} | Rs. {row[2]} | {row[3]}")
                    subtotal += float(row[2])
                    flag = True
        
        print("-" * 30)
        if flag:
            print(f"Total for {query}: Rs. {subtotal}")
        else:
            print("No expenses found in this category.")
            
    except:
        print("Something went wrong reading the file.")

# Main loop
def main():
    print("\n" + "#"*40)
    print("   Welcome to Expense Manager!   ")
    print("#"*40)
    
    start_app() # Make sure CSV exists
    
    while True:
        # Making the menu look like a box
        print("\n" + "-"*30)
        print("   POCKET EXPENSE TRACKER")
        print("-" * 30)
        print(" [1] Add New Expense")
        print(" [2] View All Expenses")
        print(" [3] See Total Spending")
        print(" [4] View Category Wise")
        print(" [5] Delete an Expense")
        print(" [6] Exit App")
        print("-" * 30)
        
        print(" Select option (1-6): ", end="")
        opt = input()
        
        if opt == '1':
            add_data()
        elif opt == '2':
            view_list()
        elif opt == '3':
            calc_sum()
        elif opt == '4':
            search_cat()
        elif opt == '5':
            delete_data()
        elif opt == '6':
            print("\n" + "#"*40)
            print(" Thank you for using Expense Manager. ")
            print("           Goodbye!           ")
            print("#"*40 + "\n")
            break
        else:
            print("\n!!! Wrong input, please try again !!!")

# Run the program
if __name__ == "__main__":
    main()