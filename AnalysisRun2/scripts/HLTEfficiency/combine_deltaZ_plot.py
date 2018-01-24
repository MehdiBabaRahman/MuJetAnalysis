import sys
from ROOT import *
from argparse import ArgumentParser

from hepPlotter import HepPlotter
import hepPlotterTools as hpt
#import hepPlotterLabels as hpl

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Helpers import *

mass_strings = {
    "0p25": "0.25", 
    "0p275" : "0.275", "0p3": "0.3", "0p4" : "0.4", "0p7" : "0.7", 
    "1" : "1.0", "1p5" : "1.5", "2" : "2.0", "5" : "5.0", "8p5" : "8.5"
}

mass_indices = {
    "0p25": 0, "0p3": 1, "0p4" : 2, "0p7" : 3, "1" : 4, "1p5" : 5, "2" : 6, "5" : 7, "8p5" : 8
}

cT_strings = {
  "0" : 0.0, "0p05" :  0.05, "0p1" :  0.10, "0p2" :  0.20, "0p5" :  0.50, "1" :  1.00, 
  "200" :  2.00, "300" :  3.00, "500" :  5.00, "1000" :  10.0, "2000" :  20.0, "8500" :  85.0
}

cT_strings2 = {
  "0" : "0", "0p05" : "0.05", "0p1" : "0.1", "0p2" : "0.2", "0p5" : "0.50", "1" : "1", 
  "2" : "2", "3" : "3", "5" : "5", "10" : "10", "20" : "20", "50" : "50", "100" : "100"
}

cT_indices = {
  "0" : 0, "0p05" : 1, "0p1" : 2, "0p2" : 3, "0p5" : 4, "1" : 5, 
  "2" : 6 ,  "3" : 7, "5" : 8, "10" : 9, "20" : 10, "50" : 11, "100" : 12
};

mass_colors = {
  "0250", kRed, "0275", kOrange, "0300", kSpring, "0400", kGreen+2, "0700", kAzure+9, 
  "1000", kBlue, "1500", kViolet+6, "2000", kMagenta, "8500", kBlack
}


def makePlot(effTuple, format='pdf'):

    ## setup histogram
    hist = HepPlotter("histogram",1)
    hist.x_relative_size = 10
    hist.y_relative_size = 7
    hist.drawEffDist = False    # draw the physics distribution for efficiency (jet_pt for jet trigger)
    #hist.rebin       = 1
    hist.x_label     = effTuple[1]
    hist.y_label     = "Entries"
    hist.format      = format      # file format for saving image
    hist.saveDir     = 'deltaZ_plots_2016DarkSUSY_20180124/'
    hist.saveAs      = "deltaZ_2016MonteCarlo_" + effTuple[2] # save figure with name
    hist.CMSlabel       = 'outer'  # 'top left', 'top right'; hack code for something else
    hist.CMSlabelStatus = 'Simulation Preliminary'  # ('Simulation')+'Internal' || 'Preliminary' 
    hist.initialize()
    hist.plotLUMI = False
    hist.lumi = '2017 C, XX'
    hist.drawStatUncertainty = True    
    hist.Add(effTuple[0], draw='step', color='blue', 
             linecolor='blue', linestyle='solid',label='')

    n1, ma, ctau  = decodeDarkSUSYFileName(effTuple[2])
    #print n1, ma, ctau

    hist.extra_text.Add(r"\textbf{Dark SUSY}", coords=[0.1,0.4])
    hist.extra_text.Add(r"$m_{N1} = %s~\mathrm{GeV}$"%n1, coords=[0.1,0.35])
    hist.extra_text.Add(r"$m_{\gamma D} = %s~\mathrm{GeV}$"%(mass_strings[ma]), coords=[0.1,0.3])
    #hist.extra_text.Add(r"$c_{\tau} = %s~\mathrm{mm}$"%cT_strings2[ctau], coords=[0.1,0.25])
    plot = hist.execute()
    hist.savefig()


## make plots
deltaZ_2016MonteCarlo = {}

DarkSUSY_mH_125_mN1_10_mGammaD_0p25 = [
    'DarkSUSY_mH_125_mN1_10_mGammaD_0p25_cT_0_13TeV_deltaZ_DiMuonC_DiMuonF',
    'DarkSUSY_mH_125_mN1_10_mGammaD_0p25_cT_0p05_13TeV_deltaZ_DiMuonC_DiMuonF',
    'DarkSUSY_mH_125_mN1_10_mGammaD_0p25_cT_0p1_13TeV_deltaZ_DiMuonC_DiMuonF',
    'DarkSUSY_mH_125_mN1_10_mGammaD_0p25_cT_0p5_13TeV_deltaZ_DiMuonC_DiMuonF',
    'DarkSUSY_mH_125_mN1_10_mGammaD_0p25_cT_1_13TeV_deltaZ_DiMuonC_DiMuonF',
    'DarkSUSY_mH_125_mN1_10_mGammaD_0p25_cT_2_13TeV_deltaZ_DiMuonC_DiMuonF',
    'DarkSUSY_mH_125_mN1_10_mGammaD_0p25_cT_5_13TeV_deltaZ_DiMuonC_DiMuonF',
    'DarkSUSY_mH_125_mN1_10_mGammaD_0p25_cT_10_13TeV_deltaZ_DiMuonC_DiMuonF',
    'DarkSUSY_mH_125_mN1_10_mGammaD_0p25_cT_20_13TeV_deltaZ_DiMuonC_DiMuonF',
    'DarkSUSY_mH_125_mN1_10_mGammaD_0p25_cT_50_13TeV_deltaZ_DiMuonC_DiMuonF',
    'DarkSUSY_mH_125_mN1_10_mGammaD_0p25_cT_100_13TeV_deltaZ_DiMuonC_DiMuonF',
]


MyFile = TFile("HLT_deltaZ_DiMuonC_DiMuonF_2016.root");

first = True
for p in DarkSUSY_mH_125_mN1_10_mGammaD_0p25:
    deltaZ_2016MonteCarlo[p] =  MyFile.Get(p)
    if first:
        deltaZ_2016MonteCarlo["DarkSUSY_mH_125_mN1_10_mGammaD_0p25"] = deltaZ_2016MonteCarlo[p]
        first = False
    else:
        print "adding", p
        deltaZ_2016MonteCarlo["DarkSUSY_mH_125_mN1_10_mGammaD_0p25"].Add(deltaZ_2016MonteCarlo[p])

## need ctau to make the deocde function work!
# even though it is not used to make the plot
makePlot((deltaZ_2016MonteCarlo["DarkSUSY_mH_125_mN1_10_mGammaD_0p25"], 
          r"$\Delta Z(\mu\mu)$", "DarkSUSY_mH_125_mN1_10_mGammaD_0p25_cT_0"), format='pdf')

MyFile.Close()