import FWCore.ParameterSet.Config as cms
process = cms.Process("RPCNtupleMaker")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
#process.GlobalTag.globaltag = cms.string("103X_dataRun2_Prompt_v3")
process.GlobalTag.globaltag = cms.string("101X_dataRun2_Prompt_v11")

process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(
    #'/store/data/Run2018D/MinimumBias/RAW/v1/000/324/344/00000/6CBFA5AD-021A-2949-BE27-AA623BE85EAB.root'
    '/store/data/Run2018D/MinimumBias/RAW/v1/000/322/016/00000/CC2F11D7-23AE-E811-98DA-FA163E2890BA.root'
    #'file:/afs/cern.ch/user/b/brfranco/work/public/RPC/digi_merger/CMSSW_10_2_5/src/EventFilter/RPCRawToDigi/test/testRPCDigiMerger.root',
    #'file:/eos/cms/store/data/Run2018D/SingleMuon/RAW-RECO/ZMu-PromptReco-v2/000/321/457/00000/0C03F56B-BEA5-E811-AE45-FA163E96C3EF.root',
    #'/store/data/Run2018D/MinimumBias/RAW/v1/000/324/344/00000/6CBFA5AD-021A-2949-BE27-AA623BE85EAB.root',
    )
    )
process.TFileService = cms.Service('TFileService',
                fileName = cms.string('RPCTree_MinBias324344_digiMerger_withRecHit.root')
                )

### RPC RawToDigi - from TwinMux
process.load("EventFilter.RPCRawToDigi.RPCTwinMuxRawToDigi_cff")

### RPC RawToDigi - from CPPF
process.load("EventFilter.RPCRawToDigi.RPCCPPFRawToDigi_cff")
# process.load("EventFilter.RPCRawToDigi.RPCCPPFRawToDigi_sqlite_cff") #to load CPPF link maps from the local DB

### RPC RawToDigi - from OMTF
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.omtfStage2Digis = cms.EDProducer("OmtfUnpacker",
          inputLabel = cms.InputTag('rawDataCollector'),
          )

process.load("EventFilter.RPCRawToDigi.RPCDigiMerger_cff")

process.load("RecoLocalMuon.RPCRecHit.rpcRecHits_cfi")
process.rpcRecHits.rpcDigiLabel = cms.InputTag('rpcDigiMerger')

process.load('RPCAnalysis.RPCNtupleMaker.RPCNtupleMaker_cfi')
process.rpcNtupleMaker.rpcDigiLabel = cms.untracked.InputTag('rpcDigiMerger')
process.rpcNtupleMaker.storeRpcRecHits = cms.untracked.bool(True)

process.p = cms.Path(((process.rpcTwinMuxRawToDigi + process.rpcCPPFRawToDigi + process.omtfStage2Digis) * process.rpcDigiMerger) * process.rpcRecHits * process.rpcNtupleMaker)

