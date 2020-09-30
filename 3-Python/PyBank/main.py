import os
import csv 

csvpath = os.path.join("Resources", "budget_data.csv")
# Intialize variable to increment in loop
num_months = 0
# Blank list to capture all changes
net_changes = []
# Min and Max increase/decrease
greatest_increase = [0,0]
greatest_decrease = [0,0]
total_pl = 0
prev_pl = 0
pl = 0
# CSV Path
with open(csvpath) as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    print(csvreader)
    csv_header = next(csvreader)
    print(f'CSV Header: {csv_header}')
# For loop with enumerate to account for total averages changes    
    for i, row in enumerate(csvreader):
        print(row)
        num_months = num_months + 1
        pl = int(row[1])
        current_month = row[0]
        total_pl = total_pl + pl    
        if i == 0:
            prev_pl = pl   
        else:
            change = pl - prev_pl 
            prev_pl = pl
            net_changes.append(change)
            if change > greatest_increase[1]:
                greatest_increase[0] = current_month
                greatest_increase[1] = change
            if change < greatest_decrease[1]:
                greatest_decrease[0] = current_month
                greatest_decrease[1] = change
    net_changes = sum(net_changes) / len(net_changes)
    net_changes = float("{:.2f}".format(net_changes))
# Print statements
summary = (f"""\nFinancial Analysis\n
    ----------------------------\n
    Total Months: {num_months}\n
    Total: ${total_pl}\n
    Average  Change: ${net_changes}\n
    Greatest Increase in Profits: {greatest_increase[0]} (${greatest_increase[1]})\n
    Greatest Decrease in Profits: {greatest_decrease[0]} (${greatest_decrease[1]})\n""")
#Print Summary
print(summary)
# Export
export_name = os.path.join("Analysis", "budget_analysis.txt")
with open(export_name, "a") as txt:
    txt.write(summary)



