import FWCore.ParameterSet.Config as cms
process = cms.Process("RPCNtupleMaker")
from Configuration.Eras.Era_Run3_cff import Run3

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.GeometrySimDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRun3RoundOptics25ns13TeVLowSigmaZ_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
#process.GlobalTag.globaltag = cms.string("103X_dataRun2_Prompt_v3")
#process.GlobalTag.globaltag = cms.string("")
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2021_realistic', '')
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2019_design', '')

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
                fileName = cms.string('RPCTree_displacedJet_withRecHits.root')
                )

process.load("Geometry.MuonCommonData.muonIdealGeometryXML_cfi")
process.load("Geometry.RPCGeometry.rpcGeometry_cfi")
process.load("Geometry.MuonNumbering.muonNumberingInitialization_cfi")


process.load("RecoLocalMuon.RPCRecHit.rpcRecHits_cfi")
process.rpcRecHits.rpcDigiLabel = cms.InputTag('simMuonRPCDigis')


process.load('RPCAnalysis.RPCNtupleMaker.RPCNtupleMaker_cfi')
process.rpcNtupleMaker.rpcDigiLabel = cms.untracked.InputTag('simMuonRPCDigis')
process.rpcNtupleMaker.storeRpcRecHits = cms.untracked.bool(True)

process.p = cms.Path(process.rpcRecHits*process.rpcNtupleMaker)

