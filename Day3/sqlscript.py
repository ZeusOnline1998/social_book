import csv

with open('mock_data.csv', "r") as f:
    reader = csv.reader(f)
    for data in reader:
        print(data)
