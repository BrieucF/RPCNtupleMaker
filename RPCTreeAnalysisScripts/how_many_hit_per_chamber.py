import ROOT
import json

#roll_blacklist = ["637637229", "637571693", "637637069", "637567341", "637567133", "637567729", "637632669"]
roll_blacklist = []

ROOT.gROOT.SetBatch(ROOT.kTRUE)

file_list = ["../test/RPCTree_minBias_2018D_oneFile.root"]

rpc_tree = ROOT.TChain("rpcNtupleMaker/RPCTree")

for file_path in file_list:
    rpc_tree.Add(file_path)

nDigiForOverflow = 15
dict_roll_numberOfDigiOverflowOccurence = {}
how_many_event_with_digiOverflow = 0

th1_average_n_digi_per_roll = ROOT.TH1F("th1_average_n_digi_per_roll", "th1_average_n_digi_per_roll", 100, 0, 0.015)
th1_n_digi_per_roll = ROOT.TH1I("th1_n_digi_per_roll", "th1_n_digi_per_roll", 100, 0, 600)

#nevents = rpc_tree.GetEntries()
event_used = 0
event_max = -1
dict_roll_numberOfDigi = {}
print "Start looping on events..."
for event in rpc_tree:
    if event_used == event_max: break 
    for digi_idx in range(event.digi_nDigi):
        if event.digi_bx[digi_idx] != 0:
            continue
        if str(event.digi_rawId[digi_idx]) in roll_blacklist:
            continue
        if str(event.digi_rawId[digi_idx]) in dict_roll_numberOfDigi:
            dict_roll_numberOfDigi[str(event.digi_rawId[digi_idx])] += 1
        else:
            dict_roll_numberOfDigi[str(event.digi_rawId[digi_idx])] = 1
    event_used += 1
print "End looping on events..."

for roll in dict_roll_numberOfDigi.keys():
    th1_average_n_digi_per_roll.Fill(dict_roll_numberOfDigi[roll]/float(event_used))
    th1_n_digi_per_roll.Fill(dict_roll_numberOfDigi[roll])

#Show overflow
th1_average_n_digi_per_roll.SetBinContent(th1_average_n_digi_per_roll.GetNbinsX(), th1_average_n_digi_per_roll.GetBinContent(th1_average_n_digi_per_roll.GetNbinsX()) + th1_average_n_digi_per_roll.GetBinContent(th1_average_n_digi_per_roll.GetNbinsX() + 1));
th1_n_digi_per_roll.SetBinContent(th1_n_digi_per_roll.GetNbinsX(), th1_n_digi_per_roll.GetBinContent(th1_n_digi_per_roll.GetNbinsX()) + th1_n_digi_per_roll.GetBinContent(th1_n_digi_per_roll.GetNbinsX() + 1));


canvas_average_n_digi_per_roll = ROOT.TCanvas("canvas_average_n_digi_per_roll", "canvas_average_n_digi_per_roll")
th1_average_n_digi_per_roll.Draw()
canvas_average_n_digi_per_roll.Print("average_n_digi_per_roll_bx0.png")
canvas_average_n_digi_per_roll.SetLogy()
canvas_average_n_digi_per_roll.Print("average_n_digi_per_roll_bx0_log.png")

canvas_n_digi_per_roll = ROOT.TCanvas("canvas_n_digi_per_roll", "canvas_n_digi_per_roll")
th1_n_digi_per_roll.Draw()
canvas_n_digi_per_roll.Print("n_digi_per_roll_bx0.png")

json_roll_numberOfDigiOverflowOccurence = json.dumps(dict_roll_numberOfDigiOverflowOccurence)
f = open("roll_numberOfDigiOverflowOccurence.json", 'w')
f.write(json_roll_numberOfDigiOverflowOccurence)
f.close()
print how_many_event_with_digiOverflow, " event with overflow out of ", rpc_tree.GetEntries(), " which is ", 100*how_many_event_with_digiOverflow/float(rpc_tree.GetEntries()), " %"

