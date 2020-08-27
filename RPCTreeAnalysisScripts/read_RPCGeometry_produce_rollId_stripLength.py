import os
import json

rpc_geometry_file = "/afs/cern.ch/user/b/brfranco/RPCGeometry.txt" 
rpc_geometry = open(rpc_geometry_file, 'r')
roll_id_stripLength = {}
nstrip_list = []
dict_strip_num_nroll = {}
whole_file = rpc_geometry.read()
print len(whole_file.split("All Info "))
counter = 0
for line in whole_file.split("All Info "):
    if line.find(" number =") != -1:
        counter += 1
        roll_id = line[0:9]
        place_nstrip = line.find('length =')
        if place_nstrip == -1: 
            print "No pattern found..."
            break
        nstrip = line[place_nstrip+8:place_nstrip+12]
        nstrip = nstrip.split('.')[0]
        if roll_id in roll_id_stripLength.keys():
            print roll_id, " already in dict with entry ", roll_id_stripLength[roll_id]
        roll_id_stripLength[roll_id] = nstrip
        nstrip_list.append(nstrip)
        if nstrip in dict_strip_num_nroll.keys():
            dict_strip_num_nroll[nstrip] += 1
        else:
            dict_strip_num_nroll[nstrip] = 1
print dict_strip_num_nroll
print "Different strip numbers: ", set(nstrip_list)
print "Number of roll in json: ", len(roll_id_stripLength.keys())
print counter
with open('rollId_stripLength.json', 'w') as json_file:
      json.dump(roll_id_stripLength, json_file)
