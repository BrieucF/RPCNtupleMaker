import ROOT
import json
import os
import math

#roll_blacklist = ["637637229", "637571693", "637637069", "637567341", "637567133", "637567729", "637632669"]
#roll_blacklist = ["637571693", "637637229"]
roll_blacklist = []

#thresholds = range(5, 90)
#thresholds = range(3, 30)
thresholds = [4, 5, 7, 10, 30, 50]

ROOT.gROOT.SetBatch(ROOT.kTRUE)

#file_list = ["../test/RPCTree_minBias_2018D_oneFile.root"]
#file_list = ["../test/RPCTree_MinBias324344_digiMerger.root"]
file_list = ["/eos/cms/store/group/dpg_rpc/comm_rpc/Trigger/rpcNtuples/MinimumBias/MinimumBiasRun2018D-v1RAW-withRecHit-correct/200703_112929/0000/RPCTree_MinBias324344_digiMerger_withRecHit_2.root"]
#file_list = ["../test/RPCTree_displacedJet.root"]
#file_list = ["../test/RPCTree_singleMu_oneFile.root"]

#output_dir = 'displacedJet_bx0_noMultiplehit_noHitBefore'
#output_dir = 'displacedJet_bx0_3_30_noMultiplehit__noHitBefore'
output_dir = 'MinBiasWithRecHit_digiMerger_3_30_bx0_stripPercentage'
#output_dir = 'displacedJet_bx0_noMultiplehit_noHitBefore_stripPercentage'

rollId_nstrip = {}
with open('rollId_nstrip.json') as json_file:
    rollId_nstrip = json.load(json_file)

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

rpc_tree = ROOT.TChain("rpcNtupleMaker/RPCTree")
for file_path in file_list:
    rpc_tree.Add(file_path)
n_evt = rpc_tree.GetEntries()
print n_evt

th1_avNrollWithOverflow_vs_threshold = ROOT.TH1F('th1_avNrollWithOverflow_vs_threshold', 'th1_avNrollWithOverflow_vs_threshold', 30, 0, 30)
th1_avNrollWithOverflow_vs_threshold.GetXaxis().SetTitle("Threshold on #Digi")
th1_avNrollWithOverflow_vs_threshold.GetYaxis().SetTitle("<#Roll with more Digi than threshold>")
th1_avNrollWithOverflowForEvtWithOverFlow_vs_threshold = ROOT.TH1F('th1_avNrollWithOverflowForEvtWithOverFlow_vs_threshold', 'th1_avNrollWithOverflowForEvtWithOverFlow_vs_threshold', 30, 0, 30)
th1_avNrollWithOverflowForEvtWithOverFlow_vs_threshold.GetXaxis().SetTitle("Threshold on #Digi")
th1_avNrollWithOverflowForEvtWithOverFlow_vs_threshold.GetYaxis().SetTitle("<#Roll with more Digi than threshold> only for evt with overflow")
th1_evPercentageWithOverflow_vs_threshold = ROOT.TH1F('th1_evPercentageWithOverflow_vs_threshold', 'th1_evPercentageWithOverflow_vs_threshold', 30, 0, 30)
th1_evPercentageWithOverflow_vs_threshold.GetXaxis().SetTitle("Threshold on #Digi")
th1_evPercentageWithOverflow_vs_threshold.GetYaxis().SetTitle("Percentage of evt with roll exceeding #Digi threshold")

for threshold in thresholds:
    th1_rollWithOverflow_firedStripPercentage = ROOT.TH1F('th1_rollWithOverflow_firedStripPercentage_'+str(threshold), 'th1_rollWithOverflow_firedStripPercentage_'+str(threshold), 100, 0, 100)
    th1_rollWithOverflow_firedStripPercentage.GetXaxis().SetTitle("Fired strip percentage (%)")
    th1_rollWithOverflow_firedStripPercentage.GetYaxis().SetTitle("#roll")

    th1_NrollWithOverflow = ROOT.TH1F('th1_NrollWithOverflow_'+str(threshold), 'th1_NrollWithOverflow_'+str(threshold), 20, 0, 20)
    th1_NrollWithOverflow.GetXaxis().SetTitle("#Roll with more than "+str(threshold)+" fired strip")
    th1_NrollWithOverflow.GetYaxis().SetTitle("Events")

    nDigiForOverflow = threshold
    dict_roll_numberOfDigiOverflowOccurence = {}
    how_many_event_with_digiOverflow = 0
    how_many_roll_with_digiOverflow = 0

    th1_n_digi_per_roll = ROOT.TH1I("th1_n_digi_per_roll_per_evt", "th1_n_digi_per_roll_per_evt", 25, 0, 25)
    th1_n_digi_per_roll_largeRangeX = ROOT.TH1I("th1_n_digi_per_roll_per_evt_largeRangeX", "th1_n_digi_per_roll_per_evt_largeRangeX", 150, 0, 150)


    for event in rpc_tree:
        how_many_roll_with_digiOverflow_perEvt = 0
        dict_roll_numberOfDigi = {}
        dict_roll_digistrip_BX = {}
        for digi_idx in range(event.digi_nDigi): #First loop to check if the strip was fired over consecutive BX's
            if str(event.digi_rawId[digi_idx]) in dict_roll_digistrip_BX:
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
        for digi_idx in range(event.digi_nDigi):
            if event.digi_bx[digi_idx] != 0:
                continue
            if str(event.digi_rawId[digi_idx]) in roll_blacklist:
                #print "Ignoring ", event.digi_rawId[digi_idx]
                continue
            if dict_roll_digistrip_BX[str(event.digi_rawId[digi_idx])][event.digi_strip[digi_idx]].count(0) > 1: #remove cases with multiple hit on 1 strip at bx==0
                continue
            #if -2 in dict_roll_digistrip_BX[str(event.digi_rawId[digi_idx])][event.digi_strip[digi_idx]]: 
            #    continue
            if -1 in dict_roll_digistrip_BX[str(event.digi_rawId[digi_idx])][event.digi_strip[digi_idx]]: #if the strip was fired the BX just before, dont consider it for the counting
                continue
            if str(event.digi_rawId[digi_idx]) in dict_roll_numberOfDigi:
                dict_roll_numberOfDigi[str(event.digi_rawId[digi_idx])] += 1
            else:
                dict_roll_numberOfDigi[str(event.digi_rawId[digi_idx])] = 1

        hasOverflow = False
        for roll in dict_roll_numberOfDigi.keys():
            th1_n_digi_per_roll.Fill(dict_roll_numberOfDigi[roll])
            th1_n_digi_per_roll_largeRangeX.Fill(dict_roll_numberOfDigi[roll])
            if dict_roll_numberOfDigi[roll] >= nDigiForOverflow:
                strip_percentage = dict_roll_numberOfDigi[roll]*100/float(rollId_nstrip[roll]) 
                th1_rollWithOverflow_firedStripPercentage.Fill(strip_percentage)
                how_many_roll_with_digiOverflow += 1
                how_many_roll_with_digiOverflow_perEvt += 1
                hasOverflow = True
                if roll in dict_roll_numberOfDigiOverflowOccurence:
                    dict_roll_numberOfDigiOverflowOccurence[roll] += 1
                else:
                    dict_roll_numberOfDigiOverflowOccurence[roll] = 1
        if hasOverflow:
            th1_NrollWithOverflow.Fill(how_many_roll_with_digiOverflow_perEvt)
            how_many_event_with_digiOverflow += 1
    th1_evPercentageWithOverflow_vs_threshold.SetBinContent(threshold, how_many_event_with_digiOverflow/float(n_evt))
    th1_evPercentageWithOverflow_vs_threshold.SetBinError(threshold, math.sqrt(how_many_event_with_digiOverflow)/float(n_evt))

    if how_many_event_with_digiOverflow != 0:
        th1_avNrollWithOverflowForEvtWithOverFlow_vs_threshold.SetBinContent(threshold, how_many_roll_with_digiOverflow/float(how_many_event_with_digiOverflow)) 
        th1_avNrollWithOverflowForEvtWithOverFlow_vs_threshold.SetBinError(threshold, math.sqrt(how_many_roll_with_digiOverflow)/float(how_many_event_with_digiOverflow)) 

    th1_avNrollWithOverflow_vs_threshold.SetBinContent(threshold, how_many_roll_with_digiOverflow/float(n_evt)) 
    th1_avNrollWithOverflow_vs_threshold.SetBinError(threshold, math.sqrt(how_many_roll_with_digiOverflow)/float(n_evt)) 

    canvas_rollWithOverflow_firedStripPercentage = ROOT.TCanvas('th1_rollWithOverflow_firedStripPercentage_'+str(threshold), 'th1_rollWithOverflow_firedStripPercentage_'+str(threshold))
    th1_rollWithOverflow_firedStripPercentage.Draw()
    canvas_rollWithOverflow_firedStripPercentage.Print(os.path.join(output_dir, "rollWithOverflow_firedStripPercentage_"+str(threshold)+".png"))
    canvas_rollWithOverflow_firedStripPercentage.Print(os.path.join(output_dir, "rollWithOverflow_firedStripPercentage_"+str(threshold)+".root"))

    canvas_NrollWithOverflow = ROOT.TCanvas('th1_NrollWithOverflow_'+str(threshold), 'th1_NrollWithOverflow_'+str(threshold))
    th1_NrollWithOverflow.Draw()
    canvas_NrollWithOverflow.Print(os.path.join(output_dir, "NrollWithOverflow_"+str(threshold)+".png"))
    canvas_NrollWithOverflow.Print(os.path.join(output_dir, "NrollWithOverflow_"+str(threshold)+".root"))

    #th1_n_digi_per_roll.SetBinContent(th1_n_digi_per_roll.GetNbinsX(), th1_n_digi_per_roll.GetBinContent(th1_n_digi_per_roll.GetNbinsX()) + th1_n_digi_per_roll.GetBinContent(th1_n_digi_per_roll.GetNbinsX() + 1));
    #canvas_n_digi_per_roll = ROOT.TCanvas("canvas_n_digi_per_roll", "canvas_n_digi_per_roll")
    #th1_n_digi_per_roll.Draw()
    #canvas_n_digi_per_roll.Print(os.path.join(output_dir, "n_digi_per_roll_per_evt_bx0_noMultipleHit_noHitInBXminus1.png"))

    #th1_n_digi_per_roll_largeRangeX.SetBinContent(th1_n_digi_per_roll_largeRangeX.GetNbinsX(), th1_n_digi_per_roll_largeRangeX.GetBinContent(th1_n_digi_per_roll_largeRangeX.GetNbinsX()) + th1_n_digi_per_roll_largeRangeX.GetBinContent(th1_n_digi_per_roll_largeRangeX.GetNbinsX() + 1));
    #canvas_n_digi_per_roll_largeRangeX = ROOT.TCanvas("canvas_n_digi_per_roll_largeRangeX", "canvas_n_digi_per_roll_largeRangeX")
    #th1_n_digi_per_roll_largeRangeX.Draw()
    #canvas_n_digi_per_roll_largeRangeX.Print(os.path.join(output_dir, "n_digi_per_roll_per_evt_largeRangeX_bx0_noMultipleHit_noHitInBXminus1.png"))
    #canvas_n_digi_per_roll_largeRangeX.SetLogy()
    #canvas_n_digi_per_roll_largeRangeX.Print(os.path.join(output_dir, "n_digi_per_roll_per_evt_largeRangeX_bx0_noMultipleHit_noHitInBXminus1_logy.png"))

    json_roll_numberOfDigiOverflowOccurence = json.dumps(dict_roll_numberOfDigiOverflowOccurence)
    f = open(os.path.join(output_dir, "roll_numberOfDigiOverflowOccurence_threshold_" + str(nDigiForOverflow) + ".json"), 'w')
    f.write(json_roll_numberOfDigiOverflowOccurence)
    f.close()
    print how_many_event_with_digiOverflow, " event with overflow for threshold ", nDigiForOverflow, " out of ", rpc_tree.GetEntries(), " which is ", 100*how_many_event_with_digiOverflow/float(rpc_tree.GetEntries()), " %"

canvas_evPercentageWithOverflow_vs_threshold = ROOT.TCanvas('evPercentageWithOverflow_vs_threshold', 'evPercentageWithOverflow_vs_threshold')
th1_evPercentageWithOverflow_vs_threshold.Draw()
canvas_evPercentageWithOverflow_vs_threshold.Print(os.path.join(output_dir, "evPercentageWithOverflow_vs_threshold.png"))
canvas_evPercentageWithOverflow_vs_threshold.Print(os.path.join(output_dir, "evPercentageWithOverflow_vs_threshold.root"))

canvas_avNrollWithOverflowForEvtWithOverFlow_vs_threshold = ROOT.TCanvas('avNrollWithOverflowForEvtWithOverFlow_vs_threshold', 'avNrollWithOverflowForEvtWithOverFlow_vs_threshold')
th1_avNrollWithOverflowForEvtWithOverFlow_vs_threshold.Draw()
canvas_avNrollWithOverflowForEvtWithOverFlow_vs_threshold.Print(os.path.join(output_dir, "avNrollWithOverflowForEvtWithOverFlow_vs_threshold.png"))
canvas_avNrollWithOverflowForEvtWithOverFlow_vs_threshold.Print(os.path.join(output_dir, "avNrollWithOverflowForEvtWithOverFlow_vs_threshold.root"))

canvas_avNrollWithOverflow_vs_threshold = ROOT.TCanvas('avNrollWithOverflow_vs_threshold', 'avNrollWithOverflow_vs_threshold')
th1_avNrollWithOverflow_vs_threshold.Draw()
canvas_avNrollWithOverflow_vs_threshold.Print(os.path.join(output_dir, "avNrollWithOverflow_vs_threshold.png"))
canvas_avNrollWithOverflow_vs_threshold.Print(os.path.join(output_dir, "avNrollWithOverflow_vs_threshold.root"))

