"""
Main module for binging together all the steps needed for the occupancy measurement

K. Schweiger, 2017
"""

import logging

import modules.classes as classes
import modules.output
import modules.pandasOutput
def getValuesPerLayer(n, nModules, collBunches, isCluster = False,
                      RevFrequ = 11245, ActiveModArea = 10.45, PixperMod = 66560 ):
    """
    Function for calculating mean values per Layer:
    * hit pixel/cluster per module
    * hit pixel/cluster per area [cm^-2]
    * hit pixel/cluster par area rate [cm^-2 s^-1]
    * occupancy

    Set isCluster to True if used for cluster because occupancy can ne be measured.

    returns dict with keys: PixpMod, PixpArea, PixpAreaSec, Occ
    """

    perMod = n / float(nModules)
    perArea, perAreaSec = calculateCommonValues(perMod, collBunches, RevFrequ, ActiveModArea, PixperMod)

    occupancy = None
    if not isCluster:
        occupancy =  perMod / PixperMod

    return {"perMod" : perMod, "perArea" : perArea, "perAreaSec" : perAreaSec, "Occ" : occupancy}

def getValuesPerDet(nperDet, collBunches, isCluster = False,
                    RevFrequ = 11245, ActiveModArea = 10.45, PixperMod = 66560):
    """
    Function for calculating mean values per Det/Module:
    * hit pixel/cluster per area [cm^-2]
    * hit pixel/cluster par area rate [cm^-2 s^-1]
    * occupancy

    Set isCluster to True if used for cluster because occupancy can ne be measured.

    returns dict with keys: PixpMod, PixpArea, PixpAreaSec, Occ
    """

    perArea, perAreaSec = calculateCommonValues(nperDet, collBunches, RevFrequ, ActiveModArea, PixperMod)

    occupancy = None
    if not isCluster:
        occupancy =  nperDet / PixperMod

    return {"perMod" : nperDet, "perArea" : perArea, "perAreaSec" : perAreaSec, "Occ" : occupancy}

def calculateCommonValues(nPerModule, collBunches, RevFrequ, ActiveModArea, PixperMod):
    perArea = nPerModule / float(ActiveModArea)
    perAreaSec = perArea * collBunches * RevFrequ

    return perArea, perAreaSec

def occupancyFromConfig(config):
    from ConfigParser import SafeConfigParser

    logging.info("Processing config {0}".format(config))

    cfg = SafeConfigParser()
    cfg.read( config )

    runstoProcess = cfg.sections()
    logging.debug("Sections in config: {0}".format(runstoProcess))
    Resultcontainers = {}
    for run in runstoProcess:
        logging.info("Processing section {1} from config {0}".format(config, run))
        inputfile = cfg.get(run, "file")
        collBunches = cfg.getfloat(run, "collidingBunches")
        comment = cfg.get(run, "comment")
        Resultcontainers[run] = classes.container(run, inputfile, collBunches, comment)
        #TODO: look for / and if there is one in outputname make subfolder and save .dat files there
        modules.output.makeTabel(Resultcontainers[run], outputname = "out"+run.replace(" ",""))
        print Resultcontainers
    #modules.pandasOutput.getDataFrames(Resultcontainers, runstoProcess)
    #modules.pandasOutput.makeFullDetectorTables(Resultcontainers, runstoProcess, "testing")
    modules.pandasOutput.makeHTMLfile(Resultcontainers, runstoProcess, "testing")
        #modules.output.makeRunComparisonTable(Resultcontainers)

def occupancyFromFile(inputfile, collBunchesforRun):
    """
    Calculate occupency and related values from a preprocesst file containing
    the nescessary histograms

    TODO: Link DPGPixel Github
    """
    filename = inputfile.split("/")[-1].split(".")[0]
    logging.info("Processing file: {0}".format(filename))
    logging.debug("File location: {0}".format(inputfile))
    Resultcontainer = classes.container(filename, inputfile, collBunchesforRun)
    Resultcontainer.printValues()
    #print modules.output.formatContainerFullPixelDetector(Resultcontainer)
    modules.output.makeTabel(Resultcontainer)
