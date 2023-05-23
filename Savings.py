def savings_account():
    # message is printed for users
    print('''Instant Savings: Access your money whenever you need it, without having to give notice.
          Ideal for if you need to dip into your savings.
          _________________________________________________________________________________________
          Fixed Bonds: If you already have savings that you don’t mind locking away for a couple of years. 
          Fixed Bonds are a great way of making more of your money in the long term.
          And the longer you decide to leave them, the more rewarding your interest rate will be.''')

    # user chooses account type
    account_type = input("Please enter 'a' for Instant Access Savings or 'b' for Fixed Bonds:   ")

    if account_type == "a":
        savings_amount = int(input("Please enter the amount you want to deposit:  "))
        years = int(input("Please enter the amount of years you want to invest for: "))

        # calculations for when account type Instant Access Saving is chosen
        NatWest = savings_amount * 1.0225 ** years - savings_amount
        NatWest = round(NatWest, 2)
        Aviva = savings_amount * 1.02 ** years - savings_amount
        Aviva = round(Aviva, 2)
        Lloyds = savings_amount * 1.0247 ** years - savings_amount
        Lloyds = round(Lloyds, 2)

        print(f"If you choose NatWest you'll earn £{NatWest} in interest after {years}")
        print(f"If you choose Aviva you'll earn £{Aviva} in interest after {years}")
        print(f"If you choose Lloyds you'll earn £{Lloyds} in interest after {years}")

        print("Thank you for using the calculator today!")

    elif account_type == 'b':
        bond_amount = int(input("Please enter the amount you want to deposit:   "))
        num_years = int(input("Please enter the amount of years you want to invest for:   "))

        # calculations for when account type Fixed Bonds is chosen based on the number of years
        if 1 <= num_years < 3:
            NatWest_bond = bond_amount * 1.04 ** num_years - bond_amount
            NatWest_bond = round(NatWest_bond, 2)
            Aviva_bond = bond_amount * 1.042 ** num_years - bond_amount
            Aviva_bond = round(Aviva_bond, 2)
            Lloyds_bond = bond_amount * 1.0425 ** num_years - bond_amount
            Lloyds_bond = round(Lloyds_bond, 2)

            print(f"If you choose NatWest you'll earn £{NatWest_bond} in interest after {num_years}")
            print(f"If you choose Aviva you'll earn £{Aviva_bond} in interest after {num_years}")
            print(f"If you choose Lloyds you'll earn £{Lloyds_bond} in interest after {num_years}")

            print("Thank you for using the calculator today!")

        elif num_years >= 3:
            NatWest_bond = bond_amount * 1.05 ** num_years - bond_amount
            NatWest_bond = round(NatWest_bond, 2)
            Aviva_bond = bond_amount * 1.052 ** num_years - bond_amount
            Aviva_bond = round(Aviva_bond, 2)
            Lloyds_bond = bond_amount * 1.0525 ** num_years - bond_amount
            Lloyds_bond = round(Lloyds_bond, 2)

            print(f"If you choose NatWest you'll earn £{NatWest_bond} in interest after {num_years}")
            print(f"If you choose Aviva you'll earn £{Aviva_bond} in interest after {num_years}")
            print(f"If you choose Lloyds you'll earn £{Lloyds_bond} in interest after {num_years}")

            print("Thank you for using the calculator today!")

    else:
        print("Please enter correct value")
    return


# ============== This menu is presented to the users =====================#
def menu():
    print("Choose either 'Savings Account' or 'Stocks Portfolio' from the menu to proceed.")
    print("-------------------------------------------------------------------------------------------")
    print("Savings Account - to calculate the amount of interest you'll earn at the end of a couple of years")
    print("Investment - to calculate the amount of interest you'll earn on your investment")
    print("1. Savings Account")
    print("2. Stocks Portfolio")
    print("0. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        savings_account()
    elif choice == "2":
        stocks_portfolio()
    elif choice == "0":
        print("Goodbye!")
    else:
        print("Invalid choice. Please enter 0, 1 or 2")


menu()
