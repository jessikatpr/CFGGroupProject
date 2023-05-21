# Import necessary libraries
import os
import pandas as pd
import pdfplumber
import re
import unicodedata
from collections import namedtuple
import matplotlib.pyplot as plt



# SpendingTrack function
def Organise_Expenses():
    """
    Use pandas to read in expense file with csv format.
    Reformat the data frame and add the Month information which will be used to merge with payslip data frame.
    """
    expense_file = input('Enter the expense file name: (ended with .csv) ')
    f1 = pd.read_csv(os.path.join(expense_file))
    f2 = f1.rename(columns = {'Money Out': 'Out', 'Money In': 'In'})
    f3 = abs(f2.groupby('Category')['Out'].sum()) # only take the Money Out column and sum it up, then change to positive value
    f3['Month'] = f2.Date[0].split('/')[1]
    f4 = pd.DataFrame(f3)
    expense_df = f4.transpose()
    print("Status: Expense file has been read")
    return expense_df
    



# Extract information needed from payslip
def get_payslip():
    """
    Use pdfplumber to extract information from a PDF file.
    """
    payslip_file = input("Enter the payslip file name: (end with .pdf) ")

    with pdfplumber.open(os.path.join(payslip_file)) as pdf: # use content manager
        extractText = pdf.pages[0].extract_text()
        extractText2 = unicodedata.normalize("NFKD", extractText) # return normal form for some Unicode String
        extractText_final = extractText2.replace("\xad", "")
        print("Status: Extracted information from the payslip") # TODO: write test that test the length
        return extractText_final
    

def get_required_info(extractText_final):
    """
    Use regex to match the pattern from payslip file
    Input: string from pdfplumber
    """
    
    # Match with Regex patterns
    PayDate_re = re.compile(r"(Date: )(\d{2}/\d{2}/\d{4})")
    Salary_re = re.compile(r"(Salary)(\s)(\d+.\d+)")
    Tax_re = re.compile(r"(Tax)(\s)(\d+.\d+)")
    NI_re = re.compile(r"(National Insurance)(\s)(\d+\d+)")
    ErsNICTP_re = re.compile(r"(Ers NIC TP:)(\d+.\d+)")    
    ErsNICYTD_re = re.compile(r"(Ers NIC YTD:)(\s)(\d+.\d+)")
    ErsPensionTP_re = re.compile(r"(Ers Pension TP:)(\s)(\d+.\d+)")
    ErsPensionYTD_re = re.compile(r"(Ers Pension YTD:)(\s)(\d+.\d+)")
    
    # Search based on complied patterns
    Pay_Date = PayDate_re.search(extractText_final).group(2)
    Salary = Salary_re.search(extractText_final).group(3)
    Tax = Tax_re.search(extractText_final).group(3)
    National_Insurance = NI_re.search(extractText_final).group(3)
    Ers_NIC_TP = ErsNICTP_re.search(extractText_final).group(2)
    Ers_NIC_YTD = ErsNICYTD_re.search(extractText_final).group(3)
    Ers_Pension_TP = ErsPensionTP_re.search(extractText_final).group(3)
    Ers_Pension_YTD = ErsPensionYTD_re.search(extractText_final).group(3)

    # Use namedtuple to collection information
    Line = namedtuple("Compensation_Package", "Pay_Date, Salary,Tax, National_Insurance, Ers_NIC_TP, Ers_NIC_YTD,Ers_Pension_TP, Ers_Pension_YTD")

    #  Create a place holder called compensation and store the results
    compensation = []
    compensation.append(Line(Pay_Date, Salary, Tax, National_Insurance, Ers_NIC_TP, Ers_NIC_YTD,Ers_Pension_TP, Ers_Pension_YTD))

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
    print("Status: Payslip information organised")
    return payslip_df



# Concatenate data frames
def Merge_Pay_Expense(payslip_df, expense_df):
    """
    Use pandas to merge two data frames together base on common key
    Input: the payslip data frame and the expense data frame
    Return: the budget data frame (budget = payslip + expense)
    """
    budget_df = payslip_df.merge(expense_df, on = 'Month', how = 'outer')
    budget_df = budget_df.apply(pd.to_numeric, errors='ignore') 
    print('Status: Payslip and expense information combined')
    return budget_df





# Graph budget summary
def plot_summary(budget_df):
    """
    Use matplotlib to plot summary budget graph
    Input: budget data frame
    Output: Summary graph in png format
    """

    plt.style.use('ggplot')
    plt.rcParams.update({'figure.autolayout': True}) 
    #automatically make room for the element created in matplotlib
    fig, ax = plt.subplots(1,2)

    # Get a data frame that only contains the money out information
    df_out = budget_df.drop(columns=['Pay_Date', 'Month', 'Salary', 'Ers_NIC_YTD' ,'Ers_Pension_YTD'])

    df_out.plot(kind = 'bar', stacked = True, figsize = (10, 6), ax = ax[0])
    budget_df['Salary'].plot(kind = 'bar', color = 'green', alpha = 0.2, ax = ax[0])

    # Add decoration to left plot
    ax[0].set_xticklabels(budget_df['Month'], rotation = 90)
    ax[0].set(xlabel = 'Month', ylabel='GBP', title = 'Budget Summary')
    ax[0].legend(bbox_to_anchor = (1,1), loc = 'upper right')


    # Plot summary table to right plot
    ax[1].axis('off')
    ax[1].axis('tight')

    summary_split = budget_df.drop(columns = ['Pay_Date', 'Month']).to_dict(orient='split')

    summary_table = pd.DataFrame({
        'Item' : summary_split['columns'], 
        'Amount (GBP)': summary_split['data'][0]
        })

    table = ax[1].table(cellText=summary_table.values, colLabels=summary_table.columns, loc='center', colWidths = [0.5, 0.5])
    table.set_fontsize(100)
    table.scale(1,2)

    plt.savefig('Budget Summary Chart.png', bbox_inches="tight", pad_inches=0.3)
    print('Status: Summary generated')




if __name__ == '__main__':
    expense_df = Organise_Expenses()
    extractText_final = get_payslip()
    compensation = get_required_info(extractText_final)
    payslip_df = get_payslip_dataframe(compensation)
    budget_df = Merge_Pay_Expense(payslip_df, expense_df)
    plot_summary(budget_df)


