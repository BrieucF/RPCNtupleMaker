#ifndef RPCNtupleConfig_h
#define RPCNtupleConfig_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Framework/interface/ESHandle.h"

//#include "Geometry/CommonDetUnit/interface/GlobalTrackingGeometry.h"
#include "Geometry/RPCGeometry/interface/RPCGeometry.h"
#include "Geometry/Records/interface/MuonGeometryRecord.h"

//#include "DTDPGAnalysis/RPCNtuples/src/DTTrigGeomUtils.h"

#include <map>
#include <string>
#include <memory>

namespace edm
{
  class ParameterSet;
  class EventSetup;
}

class RPCNtupleConfig
{

 public :

  /// Constructor
  RPCNtupleConfig(const edm::ParameterSet & config);

  /// Update EventSetup information
  void getES(const edm::EventSetup & environment);

  /// Map containing different input tags
  std::map<std::string, edm::InputTag> m_inputTags;

  // Options from cfg
  bool m_storeRpcDigis, m_storeRpcRecHits;


  /// Handle to the DT geometry
  edm::ESHandle<RPCGeometry> m_rpcGeometry;

};

#endif

