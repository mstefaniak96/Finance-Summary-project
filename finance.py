import gspread
import csv
import time

MONTH = 'july'

file = f'PKO_{MONTH}.csv'

def pko_finance(file):
    transactions = []
    all_categories = []
    # fetching transaction data 
    with open(file, encoding="utf8", errors='ignore', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for i in csv_reader:
            if i[3] == 'Kwota':
                pass
            else:
                date = i[0]
                name = i[2]
                amount = float(i[3])
                all_categories.append(i[2])
                transaction = ((date,name,amount))
                transactions.append(transaction)
 
    sa = gspread.service_account()
    sh = sa.open('My Finance')

    wsheet = sh.worksheet(f'{MONTH}') 
    wsheet.batch_clear(['A6:C1000'])

    # inserting transactions with use of sleep due to API limitations
    for i in transactions:
        wsheet.insert_rows([i],6)
        time.sleep(1.5)



def finance_summary(file):
    expenses = []
    income = []
    # fetching data to create a list for expenses and incomes
    with open(file, encoding="utf8", errors='ignore', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for i in csv_reader:
            if i[3] == 'Kwota':
                pass
            else:
                amount = float(i[3])
                if amount > 0:
                    income.append(amount)
                elif amount < 0:
                    expenses.append(amount)
                
    sa = gspread.service_account()
    sh = sa.open('My Finance')

    wsheet = sh.worksheet(f'{MONTH}') 
    
    # Creating sums of data to update spreadsheet cells
    
    sum_of_expenses = sum(expenses)
    sum_of_income = sum(income)
    total = sum_of_income+sum_of_expenses
    
    wsheet.batch_clear(['A2:C2'])
    wsheet.update_cell(2,1,sum_of_expenses)
    wsheet.update_cell(2,2,sum_of_income)
    wsheet.update_cell(2,3,total)
        
    
def finance_breakdown(file):
    transactions = []
    all_categories = []   
    # opening the file and creating transaction data
    with open(file, encoding="utf8", errors='ignore', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for i in csv_reader:
            if i[3] == 'Kwota':
                pass
            else:
                name = i[2]
                amount = float(i[3])
                all_categories.append(i[2])
                transaction = ((name,amount))
                transactions.append(transaction)  


    categories = []
    new_dict = {}
    
    # removing duplicates from all_categories
    [categories.append(i) for i in all_categories if i not in categories]
    
    #creating dictionary 
    for i in categories:
        new_dict[i] = []
        
    # adding all transactions sum for each category
    for i in transactions:
        if i[0] in new_dict.keys():
            new_dict[i[0]].append(i[1])
            
    # creating the sums for categories
    for i in new_dict:
        new_dict.update({i:sum(new_dict[i])})
        
    sa = gspread.service_account()
    sh = sa.open('My Finance')

    wsheet = sh.worksheet(f'{MONTH}') 
    
    wsheet.batch_clear(['E1:Z2'])
    # updating cells with categories and values
    for idx,v in enumerate(new_dict.items()):
        my_values = list(v)
        wsheet.update_cell(1,idx+5,my_values[0])
        wsheet.update_cell(2,idx+5,my_values[1])

pko_finance(file)
finance_breakdown(file)
finance_summary(file)
