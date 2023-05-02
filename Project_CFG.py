import math

# the lines below prints out what the user sees when the program runs
print("Choose either 'Monthly Savings Account' or 'Stocks Portfolio' from the menu to proceed: \n")

print("Monthly Savings - to calculate the amount of interest you'll earn at the end of a couple of years")
print("investment - to calculate the amount of interest you'll earn on your investment")


user_choice = str(input("Please enter your choice:   "
                        "Choose 1 for Monthly Savings:  "))  # user chooses investment or bond


# the code block below is used to calculate the total amount of investment based on user input.
if user_choice == "1":
    Savings_Amount = int(input("Please enter the amount you want to deposit:  "))
    Years = int(input("Please enter the amount of years you want to invest for: "))
    NatWest = Savings_Amount * 0.0525**Years
    Aviva = Savings_Amount * 0.05 ** Years
    Llyods = Savings_Amount * 0.04 ** Years

    print(f"Natwest will be: {NatWest}")
    print(f"Aviva will be: {Aviva}")
    print(f"Lloyds will be: {Llyods}")

else:
    print("Please enter correct value")




