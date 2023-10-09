import pandas as pd
import csv
import dateutil.parser as dp
import dateutil.relativedelta as dr
from datetime import datetime as dt

# Copy data to new file with updated header and calculated data for new columns

with open("U.S. Presidents Birth and Death Information - Sheet1.csv", 'r') as f1:
    with open("BDI_Copy.csv", 'w+', newline='') as f2:
        reader = csv.reader(f1)
        writer = csv.writer(f2)
        header = next(reader)
        writer.writerow(header + ["year_of_birth","lived_years","lived_months","lived_days"])
        for line in reader:
            towrite = line
            yob = line[1][-5:]
            if yob != '':
                start_date = dp.parse(line[1])
                end_date = dt.now() if line[3] == '' else dp.parse(line[3])
                diff = dr.relativedelta(end_date, start_date)
                print(diff)
                towrite = (line + [yob, diff.years, diff.months+diff.years*12, int(str(end_date-start_date)[:5])])

            writer.writerow(towrite)
