import pandas as pd
import csv


with open("U.S. Presidents Birth and Death Information - Sheet1.csv", 'r+') as f:
    rawCSV = f.readlines()
    rawCSV[0] = rawCSV[0].strip() + ",year_of_birth,lived_years,lived_months,lived_days\n"
    f.seek(0)
    f.writelines(rawCSV)
