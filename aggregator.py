import csv
from collections import Counter
from datetime import datetime


logs_per_month = Counter()

with open("symonds-yat-logs.csv") as f:
    for row in csv.DictReader(f):
        date = row["date"]
        if len(date) == 4:
            # This is a year
            continue
        if not date[0].isdigit():
            # This is a month, so treat it as occuring on first of month
            date = f"1 {date}"
        if not date[-1].isdigit():
            # This log is for this year
            date = f"{date}, 2024"
        date = datetime.strptime(date, "%d %b, %Y")
        logs_per_month[(date.year, date.month)] += 1

with open("symonds-yat-summary.csv", "w") as f:
    writer = csv.writer(f)
    for (year, month), n in sorted(logs_per_month.items()):
        writer.writerow([f"{year}-{month:02}", n])
