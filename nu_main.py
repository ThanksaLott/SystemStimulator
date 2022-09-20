# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 14:59:03 2022

@author: lott
GS d- s:+ a-- C++ t 5 X R tv b+ D+ G e+++ h r++ 
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from ParseODE import ParseODE
from Integrators import SingleStepIntegrator

model2load =  "xpp-two_compartment_mod" # Name of the .ode file
model2load = "TwoCompartment"
init = "default" # initial conditions, "default" for inits specified in .ode

StimulusInstr = [0,0.2,1000,6000,6000,1] # Stimulus train
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

def TimeSeries(Variable):
    """
    Plots a time series of the given Variable(s) and the stimulus parameter.

    Parameters
    ----------
    Variable : str or list
        Determines which variable(s) to plot. Use a list of str for multiple.

    Returns
    -------
    None.

    """
    plt.figure()
    plt.plot(Sim.valdict["t"][:], Sim.Stimulus[StimulusParameter], "k", label = StimulusParameter)
    if type(Variable) == list:
        for var in Variable:
            plt.plot(Sim.valdict["t"], Sim.valdict[var], label = var)
    elif type(Variable) == str:
        plt.plot(Sim.valdict["t"], Sim.valdict[Variable], label = Variable)
    plt.legend()


def PhaseSpace2D(Xvariable, Yvariable, start = 0, end = -1, interval = 50):
    """
    Generates a plot of a 2D PhaseSpace trajectory.

    Parameters
    ----------
    Xvariable : str
        Variable to be put on the x-axis.
    Yvariable : str
        Variable to be put on the y-axis.
    start : int, optional
        Starting TP of the trajectory. The default is 0.
    end : int, optional
        end TP of the trajectory. The default is -1.
    interval : int, optional
        interval (in TPs) of dots along trajectory. The default is 50.

    Returns
    -------
    None.
    """
    if end == -1:
        end = Sim.n_TPs
    cmap = cm.hot(np.abs(Sim.Stimulus[StimulusParameter][::interval]))
    
    plt.figure()
    plt.plot(Sim.valdict[Xvariable],Sim.valdict[Yvariable], "k", lw = 1)
    plt.scatter(Sim.valdict[Xvariable][::interval],
                Sim.valdict[Yvariable][::interval], 
                color = cmap, s = 8, alpha = 0.8)
    plt.xlabel(Xvariable)
    plt.ylabel(Yvariable)
    plt.show()
    



#%% Plotting for non-EGFR 2 compartment

# TimeSeries("RPMa")

# TimeSeries("PDNFa")

# TimeSeries("LRPM")

# import numpy as np
# plt.plot(Sim.valdict["t"], np.array(Sim.valdict["RPMa"])+np.array(Sim.valdict["LRPM"]))
# plt.plot(Sim.valdict["t"][1:], Sim.Stimulus[StimulusParameter], "k", label = StimulusParameter)

#%% Plotting for EGFR 2 compartment
# TimeSeries("EGFRp_pm")
# TimeSeries("EGFR_cyt")
# PhaseSpace2D('EGFRp_pm', 'PTPRGa_pm')

# EGFRtotal_pm = np.array(Sim.valdict["EGFRp_pm"])+np.array(Sim.valdict["EGFR_pm"])+np.array(Sim.valdict["EEGFRp_pm"])
# EGFRtotal = EGFRtotal_pm + np.array(Sim.valdict["EGFR_cyt"])+np.array(Sim.valdict["EGFRp_cyt"])
# plt.plot(Sim.valdict["t"]/60, EGFRtotal)
# plt.plot(EGFRtotal_pm)
#%% Plotting for the Two Compartment model

TimeSeries("RPMa")
Rtotalpm = np.array(Sim.valdict["RPMa"]) + np.array(Sim.valdict["RPMi"]) + np.array(Sim.valdict["LRPM"])
Rtotal = Rtotalpm + np.array(Sim.valdict["REa"]) + np.array(Sim.valdict["REi"]) + np.array(Sim.valdict["LREi"])
plt.plot(Rtotal)
plt.plot(Rtotalpm)

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