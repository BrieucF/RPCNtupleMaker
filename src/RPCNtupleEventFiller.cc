#include "RPCAnalysis/RPCNtupleMaker/interface/RPCNtupleEventFiller.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"

#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"

RPCNtupleEventFiller::RPCNtupleEventFiller(edm::ConsumesCollector && collector,
                     const std::shared_ptr<RPCNtupleConfig> config, 
                     std::shared_ptr<TTree> tree, const std::string & label) : 
  RPCNtupleBaseFiller(config, tree, label)
{

}

RPCNtupleEventFiller::~RPCNtupleEventFiller() 
{ 

};

void RPCNtupleEventFiller::initialize()
{
  
  m_tree->Branch((m_label + "_runNumber").c_str(), &m_runNumber, (m_label + "_runNumber/I").c_str());
  m_tree->Branch((m_label + "_lumiBlock").c_str(), &m_lumiBlock, (m_label + "_lumiBlock/I").c_str());
  m_tree->Branch((m_label + "_eventNumber").c_str(), &m_eventNumber, (m_label + "_eventNumber/L").c_str());
  
  m_tree->Branch((m_label + "_timeStamp").c_str(), &m_timeStamp, (m_label + "_timeStamp/l").c_str());

  m_tree->Branch((m_label + "_bunchCrossing").c_str(), &m_bunchCrossing, (m_label + "_bunchCrossing/I").c_str());
  m_tree->Branch((m_label + "_orbitNumber").c_str(), &m_orbitNumber, (m_label + "_orbitNumber/L").c_str());
  
}

void RPCNtupleEventFiller::clear()
{

  m_runNumber   = RPCNtupleBaseFiller::DEFAULT_INT_VAL_POS;
  m_lumiBlock   = RPCNtupleBaseFiller::DEFAULT_INT_VAL_POS;
  m_eventNumber = RPCNtupleBaseFiller::DEFAULT_INT_VAL_POS;

  m_timeStamp   = 0;
  
  m_bunchCrossing = RPCNtupleBaseFiller::DEFAULT_INT_VAL_POS;
  m_orbitNumber   = RPCNtupleBaseFiller::DEFAULT_INT_VAL_POS;
  
}

void RPCNtupleEventFiller::fill(const edm::Event & ev)
{

  clear();

  m_runNumber   = ev.run();
  m_lumiBlock   = ev.getLuminosityBlock().luminosityBlock();
  m_eventNumber = ev.eventAuxiliary().event();

  m_timeStamp = ev.eventAuxiliary().time().value();


  m_bunchCrossing = ev.eventAuxiliary().bunchCrossing();;

  m_orbitNumber   = ev.eventAuxiliary().orbitNumber();
  
  return;

}
