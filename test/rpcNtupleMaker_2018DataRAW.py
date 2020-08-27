import FWCore.ParameterSet.Config as cms
process = cms.Process("RPCNtupleMaker")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = cms.string("103X_dataRun2_Prompt_v3")

process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(
    #'file:/eos/cms/store/data/Run2018D/SingleMuon/RAW-RECO/ZMu-PromptReco-v2/000/321/457/00000/0C03F56B-BEA5-E811-AE45-FA163E96C3EF.root',
    '/store/data/Run2018D/MinimumBias/RAW/v1/000/324/344/00000/6CBFA5AD-021A-2949-BE27-AA623BE85EAB.root',
    )
    )
process.TFileService = cms.Service('TFileService',
                fileName = cms.string('RPCTree_minBias_2018D_oneFile.root')
                )

process.load("EventFilter.RPCRawToDigi.rpcUnpacker_cfi")
import EventFilter.RPCRawToDigi.rpcUnpacker_cfi
muonRPCDigis = EventFilter.RPCRawToDigi.rpcUnpacker_cfi.rpcunpacker.clone()
muonRPCDigis.InputLabel = 'rawDataCollector'
process.rpcunpacker.InputLabel = 'rawDataCollector'

process.load('RPCAnalysis.RPCNtupleMaker.RPCNtupleMaker_cfi')
process.rpcNtupleMaker.rpcDigiLabel = cms.untracked.InputTag('rpcunpacker')
process.rpcNtupleMaker.storeRpcRecHits = cms.untracked.bool(False)

process.p = cms.Path(process.rpcunpacker + process.rpcNtupleMaker)

