# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 14:59:03 2022

@author: lott
GS d- s:+ a-- C++ t 5 X R tv b+ D+ G e+++ h r++ 
"""

import os
from ParseODE import ParseODE
from Integrators import SingleStepIntegrator

model2load =  "xpp-two_compartment_mod" # Name of the .ode file
init = "default" # initial conditions, "default" for inits specified in .ode

StimulusInstr = [0,0.2,1000,6000,6000,14] # Stimulus train
# Follows the scheme of [basal, strength, start, length, interpulse, repeats]

StimulusParameter = "EGF" # Name of the parameter for stimulus
n_TPs = 200000 # Amount of timepoints on which simulation is performed

cwd = os.getcwd()
modellist = [fn[:-4] for fn in os.listdir(os.path.join(cwd, "models"))
             if fn.endswith(".ode")]

if not model2load in modellist:
    raise LookupError("The model (" +str(model2load) 
                      + (") you tried to import is not included in the "
                         + "modellist. Make sure you did not misstype."
                         + "The full list of models available is: \n")
                      + str(modellist)
                      )

path = os.path.join(os.path.join(cwd, "models"), model2load+".ode")


Parsed = ParseODE(path, StimulusParameter, check=False)
Sim = SingleStepIntegrator(Parsed.initdict, Parsed.diffeqdict, StimulusParameter, StimulusInstr, n_TPs, dt = 0.01)

import matplotlib.pyplot as plt
def TimeSeries(Variable):
    plt.figure()
    plt.plot(Sim.valdict["t"][1:], Sim.Stimulus[StimulusParameter], "k", label = StimulusParameter)
    if type(Variable) == list:
        for var in Variable:
            plt.plot(Sim.valdict["t"], Sim.valdict[var], label = var)
    elif type(Variable) == str:
        plt.plot(Sim.valdict["t"], Sim.valdict[Variable], label = Variable)
    plt.legend()

#%% Plotting for non-EGFR 2 compartment

# TimeSeries("RPMa")

# TimeSeries("PDNFa")

# TimeSeries("LRPM")

# import numpy as np
# plt.plot(Sim.valdict["t"], np.array(Sim.valdict["RPMa"])+np.array(Sim.valdict["LRPM"]))
# plt.plot(Sim.valdict["t"][1:], Sim.Stimulus[StimulusParameter], "k", label = StimulusParameter)

#%% Plotting for EGFR 2 compartment
TimeSeries("EGFRp_pm")
TimeSeries("EGFR_cyt")

import numpy as np
EGFRtotal_pm = np.array(Sim.valdict["EGFRp_pm"])+np.array(Sim.valdict["EGFR_pm"])+np.array(Sim.valdict["EEGFRp_pm"])
EGFRtotal = EGFRtotal_pm + np.array(Sim.valdict["EGFR_cyt"])+np.array(Sim.valdict["EGFRp_cyt"])
plt.plot(EGFRtotal)
plt.plot(EGFRtotal_pm)
#%% Plotting for the Two Compartment model

# plt.figure()
# plt.plot(Sim.valdict["t"], Sim.valdict["RPMa"])
# plt.plot(Sim.valdict["t"], Sim.valdict["RPMi"])
# plt.plot(Sim.valdict["t"], Sim.valdict["PDNFa"])
# plt.plot(Sim.valdict["t"], Sim.valdict["LRPM"])
# plt.plot(Sim.valdict["t"], Sim.valdict["REa"])
# plt.plot(Sim.valdict["t"], Sim.valdict["REi"])
# plt.plot(Sim.valdict["t"], Sim.valdict["LREi"])
# plt.plot(Sim.valdict["t"][1:], Sim.Stimulus["LT"], "k")
# # plt.ylim(-0.05,1)
# plt.show()


    #plt.ylim(-0.05,1.1)

# TimeSeries(["RPMa","RPMi","PDNFa","LRPM","REa","REi","LREi"])

# t = 5
# plt.figure()
# plt.plot(Sim.valdict["t"][:t], Sim.valdict["RPMa"][:t])
# plt.plot(Sim.valdict["t"][:t], Sim.valdict["RPMi"][:t])
# plt.plot(Sim.valdict["t"][:t], Sim.valdict["PDNFa"][:t])
# plt.plot(Sim.valdict["t"][:t], Sim.valdict["LRPM"][:t])
# plt.plot(Sim.valdict["t"][:t], Sim.valdict["REa"][:t])
# plt.plot(Sim.valdict["t"][:t], Sim.valdict["REi"][:t])
# plt.plot(Sim.valdict["t"][:t], Sim.valdict["LREi"][:t])
# plt.plot(Sim.valdict["t"][:t], Sim.Stimulus["LT"][:t], "k")
# plt.ylim(-0.05,0.6)
# plt.show()

#%% Useful for finding steady states etc.
## Returns last value for each equation
Sim.PrintLast()