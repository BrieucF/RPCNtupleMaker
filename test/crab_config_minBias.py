from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config

config = config()

config.section_("General")
config.General.requestName   = 'rpcNtupleMaker_onRAWRECO_MinBias_noJSON_automatic_newTry_v2_correct'
config.General.transferLogs = True
config.General.transferOutputs = True

config.section_("JobType")
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName    = 'test_rpcNtupleMaker_digiMerger.py'
config.JobType.outputFiles = ['RPCTree_MinBias324344_digiMerger_withRecHit.root']
#config.JobType.maxMemoryMB = 2000 # Default is 2000
#config.JobType.maxJobRuntimeMin = 200 # Default is 1315
config.JobType.allowUndistributedCMSSW = True      #use this only in case the cmssw release is not supported on all cms site and if you are sure what re you doing

config.section_("Data")
#config.Data.inputDBS = 'phys03'
#config.Data.inputDataset = '/SingleMu/dpg_rpc-digi_iRPConeRollSingleMu100-9a2330f7564cd87f532e8859b7fb3c65/USER'
config.Data.inputDataset = '/MinimumBias/Run2018D-v1/RAW'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 1
NJOBS = 153  # This is not a configuration parameter, but an auxiliary variable that we use in the next line.
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS

config.Data.outLFNDirBase = '/store/group/dpg_rpc/comm_rpc/Trigger/rpcNtuples/'
#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON_MuonPhys.txt'
#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'
config.Data.publication = False
config.Data.publishWithGroupName = True
config.Data.outputDatasetTag = 'MinimumBiasRun2018D-v1RAW-withRecHit-correct'        #change a bit this name, in order data to be not published with the name of the current test simulation
config.section_("Site")
config.Site.storageSite = 'T2_CH_CERN'
