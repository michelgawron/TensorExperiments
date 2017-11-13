"""
Testing behaviour of csv reading
"""
import csv

with open("lists/body/list_tokenized_docs.csv", "r") as fp:
    reader = csv.reader(fp)
    list_csv = [row for row in reader]
    print(len(list_csv))
    print(list_csv)
    fp.close()