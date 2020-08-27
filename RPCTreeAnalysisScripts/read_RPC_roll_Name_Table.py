import json
import csv

roumyana_table = csv.reader(open('/afs/cern.ch/user/b/brfranco/all_present_RPC_updated-Table_1.csv'), delimiter=',')

rawId_name_map = {}

for raw in roumyana_table:
    rawId_name_map[raw[1]] = raw[0]

threshold = 1
with open('roll_numberOfDigiOverflowOccurence.json') as jsonfile:
    data = json.load(jsonfile)
    for entry in data.keys():
        if data[entry] >= threshold:
            print entry, " : ", data[entry], " (%s) "%rawId_name_map[entry]

