import csv
import json

json_file = 'vancouver_west.json'
out_csv = 'vancouver_west.csv'

with open(json_file) as infile:
    data = json.load(infile)

with open(out_csv, 'wb') as outfile:
    csv_out = csv.writer(outfile)
    for id_, row in data.iteritems():
        csv_out.writerow([id_] + row)
