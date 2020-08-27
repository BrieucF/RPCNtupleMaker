import ROOT
import json

#roll_blacklist = ["637637229", "637571693", "637637069", "637567341", "637567133", "637567729", "637632669"]
roll_blacklist = []

ROOT.gROOT.SetBatch(ROOT.kTRUE)

file_list = ["../test/RPCTree_minBias_2018D_oneFile.root"]
#file_list = ["../test/RPCTree_singleMu_oneFile.root"]

rpc_tree = ROOT.TChain("rpcNtupleMaker/RPCTree")

for file_path in file_list:
    rpc_tree.Add(file_path)

nDigiForOverflow = 91
dict_roll_numberOfDigiOverflowOccurence = {}
how_many_event_with_digiOverflow = 0

th1_n_digi_per_roll = ROOT.TH1I("th1_n_digi_per_roll_per_evt", "th1_n_digi_per_roll_per_evt", 25, 0, 25)
th1_n_digi_per_roll_largeRangeX = ROOT.TH1I("th1_n_digi_per_roll_per_evt_largeRangeX", "th1_n_digi_per_roll_per_evt_largeRangeX", 150, 0, 150)

for event in rpc_tree:
    dict_roll_numberOfDigi = {}
    dict_roll_digistrip_BX = {}
    for digi_idx in range(event.digi_nDigi): #First loop to check if the strip was fired over consecutive BX's
        if str(event.digi_rawId[digi_idx]) in :ict_roll_digistrip_BX:
            if event.digi_strip[digi_idx] in dict_roll_digistrip_BX[str(event.digi_rawId[digi_idx])]:
                dict_roll_digistrip_BX[str(event.digi_rawId[digi_idx])][event.digi_strip[digi_idx]].append(event.digi_bx[digi_idx])
            else:
                dict_roll_digistrip_BX[str(event.digi_rawId[digi_idx])][event.digi_strip[digi_idx]] = [event.digi_bx[digi_idx]]
            #if event.digi_strip[digi_idx] in dict_roll_digistrip_BX[str(event.digi_rawId[digi_idx])]:
            #    dict_roll_digistrip_BX[str(event.digi_rawId[digi_idx])].append(event.digi_bx[digi_idx])
            #else:
            #    dict_roll_digistrip_BX[str(event.digi_rawId[digi_idx])][event.digi_strip[digi_idx]] = [event.digi_bx[digi_idx]]
        else:
            dict_roll_digistrip_BX[str(event.digi_rawId[digi_idx])] = {event.digi_strip[digi_idx] : [event.digi_bx[digi_idx]]}
#        if str(event.digi_rawId[digi_idx]) in roll_blacklist:
#            continue
    for digi_idx in range(event.digi_nDigi):
        if event.digi_bx[digi_idx] != 0:
            continue
        if -2 in dict_roll_digistrip_BX[str(event.digi_rawId[digi_idx])][event.digi_strip[digi_idx]]: 
            continue
        if -1 in dict_roll_digistrip_BX[str(event.digi_rawId[digi_idx])][event.digi_strip[digi_idx]]:
            continue
        if str(event.digi_rawId[digi_idx]) in dict_roll_numberOfDigi:
            dict_roll_numberOfDigi[str(event.digi_rawId[digi_idx])] += 1
        else:
            dict_roll_numberOfDigi[str(event.digi_rawId[digi_idx])] = 1

    hasOverflow = False
    for roll in dict_roll_numberOfDigi.keys():
        th1_n_digi_per_roll.Fill(dict_roll_numberOfDigi[roll])
        th1_n_digi_per_roll_largeRangeX.Fill(dict_roll_numberOfDigi[roll])
        if dict_roll_numberOfDigi[roll] >= nDigiForOverflow: # and roll == '637567869':
            print event.event_eventNumber 
            hasOverflow = True
            if roll in dict_roll_numberOfDigiOverflowOccurence:
                dict_roll_numberOfDigiOverflowOccurence[roll] += 1
            else:
                dict_roll_numberOfDigiOverflowOccurence[roll] = 1
    if hasOverflow:
        how_many_event_with_digiOverflow += 1


th1_n_digi_per_roll.SetBinContent(th1_n_digi_per_roll.GetNbinsX(), th1_n_digi_per_roll.GetBinContent(th1_n_digi_per_roll.GetNbinsX()) + th1_n_digi_per_roll.GetBinContent(th1_n_digi_per_roll.GetNbinsX() + 1));
canvas_n_digi_per_roll = ROOT.TCanvas("canvas_n_digi_per_roll", "canvas_n_digi_per_roll")
th1_n_digi_per_roll.Draw()
canvas_n_digi_per_roll.Print("n_digi_per_roll_per_evt.png")

th1_n_digi_per_roll_largeRangeX.SetBinContent(th1_n_digi_per_roll_largeRangeX.GetNbinsX(), th1_n_digi_per_roll_largeRangeX.GetBinContent(th1_n_digi_per_roll_largeRangeX.GetNbinsX()) + th1_n_digi_per_roll_largeRangeX.GetBinContent(th1_n_digi_per_roll_largeRangeX.GetNbinsX() + 1));
canvas_n_digi_per_roll_largeRangeX = ROOT.TCanvas("canvas_n_digi_per_roll_largeRangeX", "canvas_n_digi_per_roll_largeRangeX")
th1_n_digi_per_roll_largeRangeX.Draw()
canvas_n_digi_per_roll_largeRangeX.Print("n_digi_per_roll_per_evt_largeRangeX.png")

json_roll_numberOfDigiOverflowOccurence = json.dumps(dict_roll_numberOfDigiOverflowOccurence)
f = open("roll_numberOfDigiOverflowOccurence.json", 'w')
f.write(json_roll_numberOfDigiOverflowOccurence)
f.close()
print how_many_event_with_digiOverflow, " event with overflow out of ", rpc_tree.GetEntries(), " which is ", 100*how_many_event_with_digiOverflow/float(rpc_tree.GetEntries()), " %"

