# Occupancy

Use    
`python measureOccupancy.py --inputfile=path/to/file --collBunch=1 --instLumi=1`    
or   
`python measureOccupancy.py --config=configs/testconfig.cfg`    
to run the code.

## Requirements
The following python modules are necessary:
* __ROOT__ (pyROOT)
* __pandas__ (dependencies (?): numpy, scipy, matplotlib)

_Note:_ If run on the T3@PSI using some versions of CMSSW (e.g. 8_0_26) results in crash because matplotlib can not be correctly improrted.

## Config description
The configs used for config mode need to contain a __General__ section and one or more __Run__ sections:

    [General]
    title=string
    description=string
    foldername=string

* __title__ will be displayed as `<h1>` in the top of the output HTML file
* __description__  will be displayed as subtitle in the output HTML file
* __foldername__ is used as name of the folder containing the output files. If not present it will be created        

```
[RunName]
collidingBunches=float/int
lumi=float
file=string
comment=string
dataset=string
```
* __RunName__ is a unique name used the index the runs and is displayed as name in the output tables
* __collidingBunches__ and __lumi__ are used for calculations and can be obtained form WBM. __lumi__ is the average inst. luminosity in the considered LS range in e30 cm^-2 s^-1.
* __comment__ and __dataset__ are displayed in the output HTML files

If a config option is desired to be empty (for example if the section is a placeholder with empty file option), also remove the __=__ sign.
