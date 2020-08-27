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
    'file:/afs/cern.ch/work/c/cpena/public/NikTrigger/step2_file1_to_5.root',
    'file:/afs/cern.ch/work/c/cpena/public/NikTrigger/step2_file6_to_10.root',
    'file:/afs/cern.ch/work/c/cpena/public/NikTrigger/step2_file11_to_15.root',
    'file:/afs/cern.ch/work/c/cpena/public/NikTrigger/step2_file16_to_20.root'
    #'file:/eos/cms/store/data/Run2018D/SingleMuon/RAW-RECO/ZMu-PromptReco-v2/000/321/457/00000/0C03F56B-BEA5-E811-AE45-FA163E96C3EF.root',
    #'/store/data/Run2018D/MinimumBias/RAW/v1/000/324/344/00000/6CBFA5AD-021A-2949-BE27-AA623BE85EAB.root',
    )
    )
process.TFileService = cms.Service('TFileService',
                fileName = cms.string('RPCTree_displacedJet.root')
                )

process.load('RPCAnalysis.RPCNtupleMaker.RPCNtupleMaker_cfi')
process.rpcNtupleMaker.rpcDigiLabel = cms.untracked.InputTag('simMuonRPCDigis')
process.rpcNtupleMaker.storeRpcRecHits = cms.untracked.bool(False)

process.p = cms.Path(process.rpcNtupleMaker)

