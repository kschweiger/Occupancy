"""
Base module for outputs

K. Schweiger, 2017
"""
import logging
import os
from shutil import copy2
import pandas as pd

from collections import OrderedDict

import modules.htmlOutput
import modules.pandasOutput


def makeFiles(titlestring, generaldescription, containerlist, runlist, foldername, config,
              makeIndex = True, makeTables = True, makePlotOverview = True, plottuples = None,
              exportLaTex = False, exportCSV = False, exportCFG = False):
    logging.info("Starting file export")

    if not os.path.exists(foldername):
        logging.info("Creating folder: {0}".format(foldername))
        os.makedirs(foldername)

    layerNames = ["Layer1", "Layer2", "Layer3", "Layer4"]
    groups = ["Pix/Lay", "Pix/Det", "Clus/Lay", "Clus/Det"]
    ###############################################################
    # Getting dataframes
    fullperRunDF, fullRunCompDF = modules.pandasOutput.makeFullDetectorTables(containerlist, runlist)
    ZperRunDF, ZRunCompDF = modules.pandasOutput.makeZdepDetectorTables(containerlist, runlist)
    InOutperRunDF, InOutRunCompDF = modules.pandasOutput.makeInnerOuterLadderDetectorTables(containerlist, runlist)
    #Getting Tables --> NOTE The (ordered)Dics have keys with layer_group_? etc.
    logging.debug("Getting perRun tables for full detector")
    fullPerRunDFs = makePerRunDFs(fullperRunDF, runlist, groups)
    logging.debug("Getting RunComp tables for full detector")
    fullRunCompDFs = makeRunCompDFs(fullRunCompDF, layerNames, groups)
    logging.debug("Getting perRun tables for z partial detector")
    zPerRunDFs = makePerRunDFs(ZperRunDF, runlist, ["Pix/Lay"], layerNames)
    logging.debug("Getting perRun tables for inner/outer ladder partial detector")
    InOutPerRunDFs = makePerRunDFs(InOutperRunDF, runlist, ["Pix/Lay"], layerNames)
    logging.debug("Getting RunComp tables for inner/outer ladder partial detector")
    InnerRunCompDFs =  makeRunCompDFs(InOutRunCompDF, layerNames, ["Pix/Lay"], ["inner"])
    #print InnerRunCompDFs
    OuterRunCompDFs = makeRunCompDFs(InOutRunCompDF, layerNames, ["Pix/Lay"], ["outer"])
    # Style config
    from ConfigParser import SafeConfigParser
    styleconfig = SafeConfigParser()
    logging.debug("Loading style config")
    styleconfig.read("configs/style.cfg")


    #Copy cfg file to output directory:
    copy2(config, foldername)
    configname = config.split("/")[1]
    ###############################################################

    if makeIndex or makeTables or makePlotOverview:
        modules.htmlOutput.makeFiles(titlestring, generaldescription, containerlist, runlist, foldername,
                                     makeIndex, makeTables, makePlotOverview, plottuples, fullperRunDF, fullRunCompDF,
                                     ZperRunDF, ZRunCompDF, InOutperRunDF, InOutRunCompDF,
                                     cfgname = configname, linkTeX = exportLaTex, linkCSV = exportCSV, linkCFG = exportCFG)

    if exportLaTex or exportCSV:
        defaultprecision = pd.get_option('precision')
        if exportLaTex:
            pd.set_option('precision',styleconfig.getint("Tables","latexprecision"))
            logging.info("LaTex export initialized")
            if not os.path.exists("{0}/{1}".format(foldername, "tex")):
                logging.info("Creating folder: {0}".format("{0}/{1}".format(foldername, "tex")))
                os.makedirs("{0}/{1}".format(foldername, "tex"))
            for key in fullPerRunDFs:
                modules.pandasOutput.writeStringToFile(fullPerRunDFs[key].to_latex(), "{0}/tex/fullPerRun_{1}.txt".format(foldername, key.replace("/","per")))
            for key in fullRunCompDFs:
                modules.pandasOutput.writeStringToFile(fullRunCompDFs[key].to_latex(), "{0}/tex/fullRunComp_{1}.txt".format(foldername, key.replace("/","per")))
            for key in zPerRunDFs:
                modules.pandasOutput.writeStringToFile(zPerRunDFs[key].to_latex(), "{0}/tex/zPerRun_{1}.txt".format(foldername, key.replace("/","per")))
            for key in InOutPerRunDFs:
                modules.pandasOutput.writeStringToFile(InOutPerRunDFs[key].to_latex(), "{0}/tex/InOutPerRun_{1}.txt".format(foldername, key.replace("/","per")))
            for key in InnerRunCompDFs:
                modules.pandasOutput.writeStringToFile(InnerRunCompDFs[key].to_latex(), "{0}/tex/partialRunComp_{1}.txt".format(foldername, key.replace("/","per")))
            for key in OuterRunCompDFs:
                modules.pandasOutput.writeStringToFile(OuterRunCompDFs[key].to_latex(), "{0}/tex/partialRunComp_{1}.txt".format(foldername, key.replace("/","per")))
            pd.set_option('precision',defaultprecision)
        if exportCSV:
            logging.info("CSV export initialized")
            if not os.path.exists("{0}/{1}".format(foldername, "csv")):
                logging.info("Creating folder: {0}".format("{0}/{1}".format(foldername, "csv")))
                os.makedirs("{0}/{1}".format(foldername, "csv"))
            for key in fullPerRunDFs:
                modules.pandasOutput.writeStringToFile(fullPerRunDFs[key].to_csv(sep=";"), "{0}/csv/fullPerRun_{1}.csv".format(foldername, key.replace("/","per")))
            for key in fullRunCompDFs:
                modules.pandasOutput.writeStringToFile(fullRunCompDFs[key].to_csv(sep=";"), "{0}/csv/fullRunComp_{1}.csv".format(foldername, key.replace("/","per")))
            for key in zPerRunDFs:
                modules.pandasOutput.writeStringToFile(zPerRunDFs[key].to_csv(sep=";"), "{0}/csv/zPerRun_{1}.csv".format(foldername, key.replace("/","per")))
            for key in InOutPerRunDFs:
                modules.pandasOutput.writeStringToFile(InOutPerRunDFs[key].to_csv(sep=";"), "{0}/csv/InOutPerRun_{1}.csv".format(foldername, key.replace("/","per")))
            for key in InnerRunCompDFs:
                modules.pandasOutput.writeStringToFile(InnerRunCompDFs[key].to_csv(sep=";"), "{0}/csv/partialRunComp_{1}.csv".format(foldername, key.replace("/","per")))
            for key in OuterRunCompDFs:
                modules.pandasOutput.writeStringToFile(OuterRunCompDFs[key].to_csv(sep=";"), "{0}/csv/partialRunComp_{1}.csv".format(foldername, key.replace("/","per")))
        if exportCFG:
            logging.info("CFG export initialized (SaveConfigParser)")
            if not os.path.exists("{0}/{1}".format(foldername, "cfg")):
                logging.info("Creating folder: {0}".format("{0}/{1}".format(foldername, "cfg")))
                os.makedirs("{0}/{1}".format(foldername, "cfg"))
            for key in fullPerRunDFs:
                converDFtoCFG(fullPerRunDFs[key], "{0}/cfg/fullPerRun_{1}.txt".format(foldername, key.replace("/","per")))
            for key in fullRunCompDFs:
                converDFtoCFG(fullRunCompDFs[key], "{0}/cfg/fullRunComp_{1}.txt".format(foldername, key.replace("/","per")))
            for key in zPerRunDFs:
                converDFtoCFG(zPerRunDFs[key], "{0}/cfg/zPerRun_{1}.txt".format(foldername, key.replace("/","per")))
            for key in InOutPerRunDFs:
                converDFtoCFG(InOutPerRunDFs[key], "{0}/cfg/InOutPerRun_{1}.txt".format(foldername, key.replace("/","per")))
            for key in InnerRunCompDFs:
                converDFtoCFG(InnerRunCompDFs[key], "{0}/cfg/partialRunComp_{1}.txt".format(foldername, key.replace("/","per")))
            for key in OuterRunCompDFs:
                converDFtoCFG(OuterRunCompDFs[key], "{0}/cfg/partialRunComp_{1}.txt".format(foldername, key.replace("/","per")))

def makePerRunDFs(inputdf, runs, groups, layers = None):
    retDFs = OrderedDict([])
    for run in runs:
        for group in groups:
            if layers is None:
                retDFs.update({"{0}_{1}".format(run,group) : inputdf[run][group]})
            else:
                for layer in layers:
                    retDFs.update({"{0}_{1}_{2}".format(run,group,layer) : inputdf[run][group][layer]})
    return retDFs

def makeRunCompDFs(inputdf, layers, groups, ladders = None):
    retDFs = OrderedDict([])
    for layer in layers:
        for group in groups:
            if ladders is None:
                retDFs.update({"{0}_{1}".format(layer,group) : inputdf[layer][group]})
            else:
                for ladder in ladders:
                    retDFs.update({"{0}_{1}_{2}".format(layer, group, ladder) : inputdf[group][ladder][layer]})
    return retDFs

def converDFtoCFG(df, filename):
    from ConfigParser import SafeConfigParser

    cfgout = SafeConfigParser()

    for row in df.iterrows():
        cfgout.add_section(row[0])
        for key in row[1].keys():
            cfgout.set(row[0], key, str(row[1][key]))

    with open(filename, 'wb') as configfile:
        cfgout.write(configfile)
