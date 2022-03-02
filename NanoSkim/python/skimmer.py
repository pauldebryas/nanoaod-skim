import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object

class Skimmer(Module):
    def __init__(self, is_data=False):
        pass

    # def beginJob(self):
    #     Module.beginJob(self, histFile, histDirName)

    # def endJob(self):
    #     Module.endJob(self)

    # def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    #     pass

    # def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    #     pass

    @staticmethod
    def selectMuon(muon):
        '''Select muon passing analysis criteria
        '''
        return muon.pt > 24. and abs(muon.eta) < 2.4 and muon.mediumId and muon.pfRelIso03_all < 0.5

    @staticmethod
    def selectTau(tau):
        '''Select muon passing analysis criteria, without isolation
        '''
        return tau.pt > 20. and abs(tau.eta) < 2.3 and tau.idDeepTau2017v2p1VSmu > 0.5 and tau.idDeepTau2017v2p1VSe > 0.5 and tau.idDeepTau2017v2p1VSjet > 0.5

    @staticmethod
    def selectElectron(ele):
        '''Select muon passing analysis criteria, without isolation
        '''
        return ele.pt > 20. and abs(ele.eta) < 2.5 and ele.mvaFall17V2Iso_WP90 > 0.5


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        muons = Collection(event, 'Muon')
        muons = [muon for muon in muons if self.selectMuon(muon)]
        muons.sort(key=lambda x: x.pt, reverse=True)

        # At least one muon
        if not muons:
            return False

        electrons = Collection(event, 'Electron')
        electrons = [electron for electron in electrons if self.selectElectron(electron)]
        electrons = [electron for electron in electrons if not any(deltaR(electron, muon) < 0.5 for muon in muons)]
        electrons.sort(key=lambda x: x.pt, reverse=True)

        taus = Collection(event, 'Tau')
        taus = [tau for tau in taus if self.selectTau(tau)]
        taus = [tau for tau in taus if not any(deltaR(tau, muon) < 0.5 for muon in muons)]
        taus = [tau for tau in taus if not any(deltaR(tau, electron) < 0.5 for electron in electrons)]

        return len(muons) + len(taus) + len(electrons) >= 3

        return True

