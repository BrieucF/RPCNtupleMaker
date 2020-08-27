import ROOT
import json

chamber_blacklist = ["637637229", "637571693", "637637069", "637567341", "637567133", "637567729", "637632669"]

ROOT.gROOT.SetBatch(ROOT.kTRUE)

file_list = ["../test/RPCTree_minBias_2018D_oneFile.root"]

rpc_tree = ROOT.TChain("rpcNtupleMaker/RPCTree")

for file_path in file_list:
    rpc_tree.Add(file_path)

nDigiForOverflow = 15
dict_roll_numberOfDigiOverflowOccurence = {}
how_many_event_with_digiOverflow = 0

th1_n_digi_per_chamber = ROOT.TH1I("th1_n_digi_per_chamber", "th1_n_digi_per_chamber", 25, 0, 25)

for event in rpc_tree:
    dict_roll_numberOfDigi = {}
    for digi_idx in range(event.digi_nDigi):
        if str(event.digi_rawId[digi_idx]) in chamber_blacklist:
            continue
        if str(event.digi_rawId[digi_idx]) in dict_roll_numberOfDigi:
            dict_roll_numberOfDigi[str(event.digi_rawId[digi_idx])] += 1
        else:
            dict_roll_numberOfDigi[str(event.digi_rawId[digi_idx])] = 1

    hasOverflow = False
    for roll in dict_roll_numberOfDigi.keys():
        th1_n_digi_per_chamber.Fill(dict_roll_numberOfDigi[roll])
        if dict_roll_numberOfDigi[roll] >= nDigiForOverflow:
            hasOverflow = True
            if roll in dict_roll_numberOfDigiOverflowOccurence:
                dict_roll_numberOfDigiOverflowOccurence[roll] += 1
            else:
                dict_roll_numberOfDigiOverflowOccurence[roll] = 1
    if hasOverflow:
        how_many_event_with_digiOverflow += 1


th1_n_digi_per_chamber.SetBinContent(th1_n_digi_per_chamber.GetNbinsX(), th1_n_digi_per_chamber.GetBinContent(th1_n_digi_per_chamber.GetNbinsX()) + th1_n_digi_per_chamber.GetBinContent(th1_n_digi_per_chamber.GetNbinsX() + 1));
canvas_n_digi_per_chamber = ROOT.TCanvas("canvas_n_digi_per_chamber", "canvas_n_digi_per_chamber")
th1_n_digi_per_chamber.Draw()
canvas_n_digi_per_chamber.Print("n_digi_per_chamber.png")

json_roll_numberOfDigiOverflowOccurence = json.dumps(dict_roll_numberOfDigiOverflowOccurence)
f = open("roll_numberOfDigiOverflowOccurence.json", 'w')
f.write(json_roll_numberOfDigiOverflowOccurence)
f.close()
print how_many_event_with_digiOverflow, " event with overflow out of ", rpc_tree.GetEntries(), " which is ", 100*how_many_event_with_digiOverflow/float(rpc_tree.GetEntries()), " %"

