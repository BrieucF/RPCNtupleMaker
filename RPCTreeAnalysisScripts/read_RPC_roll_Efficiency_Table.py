import json
import csv

roumyana_table = csv.reader(open('/afs/cern.ch/user/b/brfranco/all_present_RPC_updated-Table_1.csv'), delimiter=',')

rollname_simEff_map = {}

for raw in roumyana_table:
    rollname_simEff_map[raw[0]] = raw[2]

efficiencies_sum = 0
n_roll = 0
string_match = 'RB1'

for rollname in rollname_simEff_map.keys():
    if string_match in rollname:
        n_roll +=1
        efficiencies_sum += float(rollname_simEff_map[rollname])
print  "Average efficiency for roll with pattern ", string_match, " is ", efficiencies_sum/float(n_roll)


