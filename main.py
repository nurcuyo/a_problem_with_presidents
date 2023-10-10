import pandas as pd
import csv
import dateutil.parser as dp
import dateutil.relativedelta as dr
from datetime import datetime as dt
from tabulate import tabulate
import matplotlib.pyplot as plt

# Copy data to new file with updated header and calculated data for new columns

with open("U.S. Presidents Birth and Death Information - Sheet1.csv", 'r') as f1:
    with open("BDI_Copy.csv", 'w+', newline='') as f2:
        reader = csv.reader(f1)
        writer = csv.writer(f2)
        header = next(reader)
        writer.writerow(header + ["year_of_birth","lived_years","lived_months","lived_days"])  # add new headers
        for line in reader:
            towrite = line
            yob = line[1][-5:]
            if yob != '':  # catches ref lines at the end without needing "try/except" blocks
                start_date = dp.parse(line[1])
                end_date = dt.now() if line[3] == '' else dp.parse(line[3]) # if alive, cmp birth to now, else to death
                diff = dr.relativedelta(end_date, start_date)  # gives diff in y, m, d, etc.
                towrite = (line + [yob, diff.years, diff.months+diff.years*12, (str(end_date-start_date)[:5])])
            writer.writerow(towrite)

# Display tables for Oldest and Youngest Presidents (pandas)

df = pd.read_csv('BDI_Copy.csv', engine='python', skipfooter=2)  # engine suppresses warning, skip footer omits ref
df = df.fillna('-')

# Since 'lived_years' represents a floored value for age in years, I added a more accurate column here to break ties

true_years = []
for index, row in df.iterrows():
    true_years += ["{:.2f}".format((row['lived_days'])/365.25)]
    print(true_years)
df['true_lived_years'] = true_years

topTen = df.nlargest(10, 'lived_days')[['PRESIDENT', 'year_of_birth', 'lived_years', 'true_lived_years', 'lived_months', 'lived_days']]
print(tabulate(topTen, headers='keys', showindex=False, tablefmt="rounded_grid"))
print('\n')
bottomTen = df.nsmallest(10, 'lived_days')[['PRESIDENT', 'year_of_birth', 'lived_years', 'true_lived_years', 'lived_months', 'lived_days']]
print(tabulate(bottomTen, headers='keys', showindex=False, tablefmt="rounded_grid"))

# Calculating statistics for lived_days

sr = df['lived_days']
# print(sr)

mean = sr.mean()
median = sr.median()
mode = sr.mode()
mx = sr.max()
mn = sr.min()
stdev = sr.std()
wavg = 0

print('\n')
print("Mean:", mean)
print("Median:", median)
# print("Mode:", mode)  # no values repeat so there is no mode
print("Max:", mx)
print("Min:", mn)
print("Standard Deviation:", stdev)

# Plotting (pandas and matplotlib)

topTen.plot.scatter(label='Oldest Presidents\' Lived Years vs Birth Year', x='year_of_birth', y='true_lived_years', c='Black')
plt.gca().invert_yaxis()
bottomTen.plot.scatter(label='Youngest Presidents\' Lived Years vs Birth Year', x='year_of_birth', y='true_lived_years', c='Red')
plt.show()

