#[MINOR PROJECT]

# Import pickle to store data
import pickle
# Imported os to check if database file exists or not
import os

# Customer class for all customers
class Customer:
    # Username of customer
    Username = None
    # Customer's password
    Password = None
    # Customer's balance initially 1000
    Balance = 1000
    # Customer's Transacton history
    Transactions = ""

    # Constructor to Initialize a customer with username and password
    def __init__(self, Username, Password):    
        # Set Username as entered by user
        self.Username = Username
        # Set password as entered by user
        self.Password = Password

    # Method to check balance of customer
    def CheckBalance(self):
        # Return the balance
        return self.Balance
    
    # Method for matching customer's password
    def LoginWithPassword(self, Password):
        # Check if entered passeord matches with origional password
        if self.Password == Password:
            # return true if matches
            return True
        # Otherwise
        else:
            # return false
            return False
    
    # Method to update customer's balance after transaction
    def UpdateBalance(self, Balance, Action):
        # Check if transaction is debit
        if Action == "debit":
            # then debit amount
            self.Balance -= Balance
        # Otherwise if transaction is credit
        elif Action == "credit":
            # then credit amount
            self.Balance += Balance
        else: pass
    
    # method to check transaction history
    def CheckTransactions(self):
        # return the history
        return self.Transactions

    # Method to add transaction record after transaction
    def AddRecord(self, Record):
        # add given transaction to the record
        self.Transactions += Record

# List of all customers
AllCustomers = []
# Object of current logged customer
ActiveCustomer = None

# Function to load data from database
def Load():
    # Get global variables
    global ActiveCustomer
    global AllCustomers

    # Check if database exists or not
    if os.path.exists("Database"):
        # if exists then read the database
        with open("Database","rb") as db:
            # read and load all customer's data into AllCustomers List
            AllCustomers = pickle.load(db)
        # Check if any user is logged in or not
        if ActiveCustomer != None:
            # If user is logged in then refresh user's data
            ActiveCustomer = FindCustomer(ActiveCustomer.Username)[1]

# Function to store data into databse
def Dump():
    # Open database file
    with open("Database","wb") as db:
        # Put the data from AllCustomers list to the database
        pickle.dump(AllCustomers, db)

# Function to find out a customer by username
def FindCustomer(Username):
    # check if list of customers is empty or not
    if AllCustomers == []:
        # if empty then return false as no user exists
        return [False]
    
    # otherwise loop through all customers
    for Customer in AllCustomers:
        # and check is username of customer matches with the record or not
        if Customer.Username == Username:
            # if username is matched then return TRUE and the customer object
            return [True, Customer]
    # otherwise return FALSE as no customer is found
    return [False]

# Function to create new account
def CreateAccount():
    # print welcome messege
    print("\n[SIGNUP]\nCreate new Username and Password\n")
    # get username from user
    Username = str(input("Username: "))
    # load fresh data
    Load()
    # Check if user is already existing or not
    if FindCustomer(Username)[0] == True:
        # If username is already taken then show messege
        print("Username is already taken. Try again")
        return False
    # otherwise
    else:
        # get passeord from user
        Password = str(input("Password: "))
        # create new customer object
        NewCustomer = Customer(Username, Password)
        # add new customer to the list of all customers
        AllCustomers.append(NewCustomer)
        # store updated data to the database
        Dump()
        # show success messege
        print("Account created successfully.")

# Function to Log a user in
def Login():
    # Show welcome messege
    print("\n[LOGIN]\n")
    # get username input
    Username = str(input("Username: "))
    # get password input
    Password = str(input("Password: "))
    # Load fresh data
    Load()
    # Find user by entered username
    Data = FindCustomer(Username)
    # check if user exists and also if password matches or not
    if Data[0] == True and Data[1].LoginWithPassword(Password) == True:
        global ActiveCustomer
        # if password matches the set the active user as logged in
        ActiveCustomer = Data[1]
        # show sucess messege
        print("Logged In successfully.")
    # otherwise
    else:
        # show incorrect messege
        print("Either username or password was incorrect, try again")

# Fuction to transfer Fund
def FundTransfer():
    # show welcome messege
    print("\n[FUND TRANSFER]\nWhom you want to send money:")
    # get username from user
    Username = input("Username:")
    # load fresh data
    Load()
    # check is user exists or not
    if FindCustomer(Username)[0] == False:
        # If not then show messege
        print("No such user found. Try again.")
        return 0
    # otherwise check if user is not entering his own username
    if Username == ActiveCustomer.Username:
        # then show messege
        print("You can't send money to yourself.")
        return 0
    # otherwise get amount input from user
    Amount = int(input("Enter the amount: Rs."))
    # load new data
    Load()
    # check if amount is not less than 0
    if Amount < 1:
        print("Please Enter a valid amount.")
        return 0
    # check if user have sufficent balance to transfer
    if Amount > ActiveCustomer.Balance:
        print("You don't have enough money to send.")
        return 0
    # get other customer's object
    SecondCustomer = FindCustomer(Username)[1]
    # Update balance of other customer
    SecondCustomer.UpdateBalance(Amount, "credit")
    # Update balance of current customer
    ActiveCustomer.UpdateBalance(Amount, "debit")
    # Add transaction record to the history of current user
    ActiveCustomer.AddRecord("DEBIT  " + str(Amount) + " TO USER " + Username + "\n")
    # Add transaction record to the history of other user
    SecondCustomer.AddRecord("CREDIT " + str(Amount) + " BY USER " + ActiveCustomer.Username + "\n")
    # store updated data into database
    Dump()
    print("Transaction Successful.")

# Function to delete a customer account
def DeleteAccount():
    # load fresh data
    Load()
    # get global variables
    global AllCustomers
    global ActiveCustomer
    # find the customer to be deleted
    for index, user in enumerate(AllCustomers):
        if user.Username == ActiveCustomer.Username:
            # remove that customer form the record
            AllCustomers.pop(index)
    # logout the user as it has been deleted
    ActiveCustomer = None
    # store updated data
    Dump()

# Function for help
def Help():
    with open("help.txt") as h:
        print(h.read())

# show welcome messege
print("\n-----[ MUNISH'S BANK ]-----\n")
# show help text on start
Help()
# main loop
while True:
    # get action input from user
    UserInput = input(":> ").lower()

    # check if user wants to quit the close the program
    if UserInput in ["exit","close","quit","x"]:
        break

    # check if user needs help then show the help text from file
    elif UserInput in ["help","h"]:
        Help()

    # if user wants to create new account then..
    elif UserInput in ["signup","create account","new account","s"]:
        # check if there is no active user
        if ActiveCustomer == None:
            # then call the CreateAccount function
            CreateAccount()
        # otherwise show messege
        else:
            print("Please Logout before this action.")

    # check if user wants to login
    elif UserInput in ["login","l"]:
        # check if there is no active user
        if ActiveCustomer == None:
            # then call login
            Login()
        # otherwise show messege
        else:
            print("You are already logged in.")

    elif UserInput in ["logout","o"]:
        # check if user is logged in or not
        if ActiveCustomer == None:
            # if not then show messege
            print("You are not logged in.")
        # otherwise clear ActiveCustomer
        else:
            ActiveCustomer = None
            print("[LOGOUT]\nLogged out successfully.")

    # check if user wants to check balance
    elif UserInput in ["balance","b"]:
        # check if there is no active user
        if ActiveCustomer == None:
            # if not then show messege
            print("You are not logged in.")
        else:
            Load()
            print("Balance: Rs.",ActiveCustomer.CheckBalance())
    
    # check if user wants to transfer fund
    elif UserInput in ["transfer","t"]:
        # check if there is no active user
        if ActiveCustomer == None:
            # if not then show messege
            print("You are not logged in.")
        else:
            FundTransfer()
    
    # check if user want to see transaction history
    elif UserInput in ["transactions","tx"]:
        # check if there is no active user
        if ActiveCustomer == None:
            # if not then show messege
            print("You are not logged in.")
        else:
            Load()
            print(ActiveCustomer.CheckTransactions())
    
    # check is user wants to delete the account
    elif UserInput in ["delete account","d","delete"]:
        # check if there is no active user
        if ActiveCustomer == None:
            # if not then show messege
            print("You are not logged in.")
        else:
            DeleteAccount()
            print("Your account has been deleted.")

    # Otherwise show error messege
    else:
        print("Unable to understand, try again.")