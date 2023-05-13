

# Import necessary libraries
import pandas as pd
import pdfplumber
import re
import unicodedata
from collections import namedtuple
from tkinter import *
import matplotlib.pyplot as plt


# Extract information needed from payslip
def PayslipInfo():
    """
    Use pdfplumber to extract information from a PDF file.
    """
    payslip_file = input("Select your payslip file: (end with .pdf)")

    with pdfplumber.open(os.path.join(payslip_file)) as pdf: # use content manager
        extractText = pdf.pages[0].extract_text()
        extractText2 = unicodedata.normalize("NFKD", extractText) # return normal form for some Unicode String
        extractText_final = extractText2.replace("\xad", "")
        return extractText_final


def get_required_info(extractText_final):
    """
    Use regex to match the pattern 
    Input: string
    """
    # Match with Regex patterns
    employ_re = re.compile(r"(SO\S\d+)(.*)(Perspectum*)")
    PayDate_re = re.compile(r"(Date: )(\d{2}/\d{2}/\d{4})")
    Salary_re = re.compile(r"(Salary)(\s)(\d+.\d+)")
    Tax_re = re.compile(r"(Tax)(\s)(\d+.\d+)")
    NI_re = re.compile(r"(National Insurance)(\s)(\d+\d+)")
    ErsNICTP_re = re.compile(r"(Ers NIC TP:)(\d+.\d+)")    
    ErsNICYTD_re = re.compile(r"(Ers NIC YTD:)(\s)(\d+.\d+)")
    ErsPensionTP_re = re.compile(r"(Ers Pension TP:)(\s)(\d+.\d+)")
    ErsPensionYTD_re = re.compile(r"(Ers Pension YTD:)(\s)(\d+.\d+)")
    
    # Search based on complied patterns
    Employee_ID = employ_re.search(extractText_final).group(1)
    Employee_Name = employ_re.search(extractText_final).group(2)
    Company_Name = employ_re.search(extractText_final).group(3)
    Pay_Date = PayDate_re.search(extractText_final).group(2)
    Salary = Salary_re.search(extractText_final).group(3)
    Tax = Tax_re.search(extractText_final).group(3)
    National_Insurance = NI_re.search(extractText_final).group(3)
    Ers_NIC_TP = ErsNICTP_re.search(extractText_final).group(2)
    Ers_NIC_YTD = ErsNICYTD_re.search(extractText_final).group(3)
    Ers_Pension_TP = ErsPensionTP_re.search(extractText_final).group(3)
    Ers_Pension_YTD = ErsPensionYTD_re.search(extractText_final).group(3)

    # Use namedtuple to collection information
    Line = namedtuple("Employment", "Employee_ID,Employee_Name, Company_Name, Pay_Date, Salary,Tax, National_Insurance, Ers_NIC_TP, Ers_NIC_YTD,Ers_Pension_TP, Ers_Pension_YTD")

    #  Create a place holder called compensation and store the results
    compensation = []
    compensation.append(Line(Employee_ID, Employee_Name, Company_Name, Pay_Date, Salary, Tax, National_Insurance, Ers_NIC_TP, Ers_NIC_YTD,Ers_Pension_TP, Ers_Pension_YTD))

    return compensation

def get_payslip_dataframe(compensation):
    """
    Use pandas to organise dataframe
    """
    payslip_df = pd.DataFrame(compensation)

    # change the datatype to numeric from column 4 onwards(ie from Salary to Ers_Pension_YTD)
    for col in payslip_df.columns[4:]:  
        payslip_df[col] = pd.to_numeric(payslip_df[col], errors="ignore")     

    # Add Month to the dataframe
    Month = []
    Month.append(payslip_df['Pay_Date'][0].split('/')[1])
    payslip_df['Month'] = Month

    return payslip_df


# SpendingTrack function
def SpendOrg():
    """
    Use pandas to read in expense file with csv format.
    Reformat the data frame and add the Month information which will be used to merge with payslip data frame.
    """
    expense_file = input('Enter your Expense:')
    f1 = pd.read_csv(expense_file)
    f2 = f1.rename(columns = {'amount out ': 'Out', 'amount in': 'In'})
    f3 = abs(f2.groupby('Category').sum())
    expense_df = f3.iloc[0:, 0:1].transpose()
    expense_df['Month'] = f2.Date[0].split('/')[1]
    return expense_df



# Concatenate data frames
def MergeSheet(payslip_df, expense_df):
    """
    Use pandas to merge two data frames together base on common key
    Input: the payslip data frame and the expense data frame
    Return: the budget data frame (budget = payslip + expense)
    """
    budget_df = payslip_df.merge(expense_df, on = 'Month', how = 'outer') 
    return budget_df


# Write budget data frame into csv file
def AddToMerge(budget_df):
    existing_budget_file = input('Please select existing budget file: (end with .csv)')
    try:
        # if there has been an existing budget file
        existing_budget_df = pd.read_csv(os.path.join(existing_budget_file))
        update_budget_df = pd.concat([existing_budget_df, budget_df], axis = 0)
        update_budget_df.to_csv('Master Budget.csv', index = False)
    except:
        # if not, create a budget file with the budget data frame
        update_budget_df = budget_df
        update_budget_df.to_csv('Master Budget.csv', index = False)
    
    print('The master budget file has been updated')