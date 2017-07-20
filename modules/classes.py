"""
Classes for occupancy measurement

K. Schweiger, 2017
"""
import logging
import ROOT

from modules.modulecounter import modulecounter
from modules.tests import isHistoinFile
import modules.measurement


class container:
    """
    Container initialized for a run containing all claculations for the occupancy
    and related values.
    """
    def __init__(self, name, inputfile, collBunches):
        logging.debug("Initializing container for {0} with inputfile {1} and colliding bunches {2}".format(name, inputfile, collBunches))
        self.LayerNames = ["Layer1", "Layer2", "Layer3", "Layer4"]
        self.zpositions = ["-4", "-3", "-2", "-1", "1", "2", "3", "4"]
        self.name = name
        self.file = ROOT.TFile.Open(inputfile)
        self.collBunches = collBunches

        # Varaiable for full layer
        self.nWorkingModules = modulecounter(self.file)
        #Pixels
        self.hitPix = {}
        self.occupancies = {}
        self.hitPixPerModule = {}
        self.hitPixPerArea = {}
        self.hitPixPerAreaSec = {}

        self.Detoccupancies = {}
        self.hitPixPerDet = {}
        self.hitPixPerDetArea = {}
        self.hitPixPerDetAreaSec = {}
        # Clusters
        self.hitClusters = {}
        self.hitClustersPerModule = {}
        self.hitClustersPerArea = {}
        self.hitClustersPerAreaSec = {}

        self.hitClustersPerDet = {}
        self.hitClustersPerDetArea = {}
        self.hitClustersPerDetAreaSec = {}

        # Set general values
        self.getBaseValuesForallLayer()


    def getBaseValuesForallLayer(self):
        """
        Calculate for each layer:
            * Occupancy (Only for pixels)
            * Pixel/Cluster hit per module
            * Pixel/Cluster hit per cm^2
            * Pixel/Cluster hit per cm^2 per sec
        """
        for ilayer, layer in enumerate(self.LayerNames):
            logging.info("Setting base values for {0}".format(layer))
            ############################################################################################
            # Pixels per Layer
            currentmean = getHistoMean(self.file, "d/hpixPerLay"+str(ilayer+1))
            self.hitPix[layer] = currentmean
            values = modules.measurement.getValuesPerLayer(currentmean, self.nWorkingModules[layer], self.collBunches)
            self.occupancies[layer] = values["Occ"]
            self.hitPixPerModule[layer] = values["perMod"]
            self.hitPixPerArea[layer] = values["perArea"]
            self.hitPixPerAreaSec[layer] = values["perAreaSec"]
            # Pixels per Det
            currentmean = getHistoMean(self.file, "d/hpixPerDet"+str(ilayer+1))
            values = modules.measurement.getValuesPerDet(currentmean, self.collBunches)
            self.Detoccupancies[layer] = values["Occ"]
            self.hitPixPerDet[layer] = values["perMod"]
            self.hitPixPerDetArea[layer] = values["perArea"]
            self.hitPixPerDetAreaSec[layer] = values["perAreaSec"]
            ############################################################################################
            # Clusters per Layer
            currentmean = getHistoMean(self.file, "d/hclusPerLay"+str(ilayer+1))
            values = modules.measurement.getValuesPerLayer(currentmean, self.nWorkingModules[layer],self.collBunches, True)
            self.hitClusters[layer] = currentmean
            self.hitClustersPerModule[layer] = values["perMod"]
            self.hitClustersPerArea[layer] = values["perArea"]
            self.hitClustersPerAreaSec[layer] = values["perAreaSec"]
            # CLusters per Det
            currentmean = getHistoMean(self.file, "d/hclusPerDet"+str(ilayer+1))
            values = modules.measurement.getValuesPerDet(currentmean, self.collBunches, True)
            self.hitClustersPerDet[layer] = values["perMod"] #In this case: The mean given to the function
            self.hitClustersPerDetArea[layer] = values["perArea"]
            self.hitClustersPerDetAreaSec[layer] = values["perAreaSec"]

    def getzDependency(self):
        pass

    def printValues(self):
        """
        Print base values for debugging
        """
        for layer in self.LayerNames:
            print "-------- {0} --------".format(layer)
            print "nWorkingModules: {0}".format(self.nWorkingModules[layer])
            print "Pixels per Layer"
            print "  Pixels hit: {0}".format(self.hitPix[layer])
            print "  Occupancy: {0}".format(self.occupancies[layer])
            print "  Pixels hit per Module: {0}".format(self.hitPixPerModule[layer])
            print "  Pixels hit per Area: {0}".format(self.hitPixPerArea[layer])
            print "  Pixels hit per Area per sec: {0}".format(self.hitPixPerAreaSec[layer])
            print "Pixels per Det"
            print "  Occupancy (Det): {0}".format(self.Detoccupancies[layer])
            print "  Pixels hit per Det: {0}".format(self.hitPixPerDet[layer])
            print "  Pixels hit per DetArea: {0}".format(self.hitPixPerDetArea[layer])
            print "  Pixels hit per DetArea per sec: {0}".format(self.hitPixPerDetAreaSec[layer])
            print "Cluster per Layer"
            print "  Clusters hit: {0}".format(self.hitClusters[layer])
            print "  Clusters hit per module: {0}".format(self.hitClustersPerModule[layer])
            print "  Clusters hit per Area: {0}".format(self.hitClustersPerArea[layer])
            print "  Clusters hit per Area per sec: {0}".format(self.hitClustersPerAreaSec[layer])
            print "Clusters per Det"
            print "  Clusters hit per Det: {0}".format(self.hitClustersPerDet[layer])
            print "  Clusters hit per DetArea: {0}".format(self.hitClustersPerDetArea[layer])
            print "  Clusters hit per DetArea per sec: {0}".format(self.hitClustersPerDetAreaSec[layer])

def getHistoMean(inputfile, histoname):
    logging.debug("Getting mean form histogram: {0}".format(histoname))
    if isHistoinFile(inputfile, histoname):
        h = inputfile.Get(histoname)
        mean = h.GetMean()
        logging.debug("Mean of histogram {0} --> {1}".format(histoname, mean))
        if mean == 0:
            logging.waring("Mean of histogram {0} in file {1} is Zero! Please Check.".format(histoname, inputfile))
    else:
        mean = 0
        logging.error("Histogram not in file! Please check.")
    return mean
