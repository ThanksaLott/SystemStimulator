# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:56:22 2022

@author: lott
GS d- s:+ a-- C++ t 5 X R tv b+ D+ G e+++ h r++ 
"""

# if __name__ == "__main__":
#     pass

import os

model2load =  "ToggleSwitch" #"I_Nap-I_K"
init = [0,0,0] #[0.0, 0.1, 0.5, 0.0, 0.0, 0.1] #[-44.3195622 , 0.53396948]
PulseInstr = [0,0,0,0,0] #[1,50,5,10,3]# [120,15,5,10,3]
BaseStim = 0

cwd = os.getcwd()
modellist = [fn[:-3] for fn in os.listdir(os.path.join(cwd, "models"))
             if fn.endswith(".py")]

if not model2load in modellist:
    raise LookupError("The model (" +str(model2load) 
                      + (") you tried to import is not included in the "
                         + "modellist. Make sure you did not misstype."
                         + "The full list of models available is: \n")
                      + str(modellist)
                      )

import importlib
mod = importlib.import_module("models."+model2load)
model = mod.model()
print(model.params)

from Stimulator import Stimulator
simu = Stimulator(model, BaseStim, PulseInstr, init, n_T = 1500)
simu.TimeSeries()


# EGFRp, RGa, RJa, EGFEGFRp, EGFEGFR, N2a, EGF = y