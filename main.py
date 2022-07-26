# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:56:22 2022

@author: lott
GS d- s:+ a-- C++ t 5 X R tv b+ D+ G e+++ h r++ 
"""

# if __name__ == "__main__":
#     pass

import os

model2load =  "AFD" #"ToggleSwitch" #"I_N ap-I_K"
init = "default" #[-5.17624, 0.633831, 0.999974, 0.0650542]#"default" #[-16.54556821, 0.53893609, 0.72679945, 0.2646773] # #[0,0,1,0] #[0.0, 0.1, 0.5, 0.0, 0.0, 0.1] #[-44.3195622 , 0.53396948]
PulseInstr = [16,30,10,10,3] #[1,50,1,10,20] #[1,50,5,10,3]# [120,15,5,10,3]
BaseStim = "criticality" #4.41
#[-19.60163931, 0.14521655, 0.09586589, 0.17472735] #
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
if init == "default": 
    init = model.initdefault
if BaseStim == "criticality":
    BaseStim = model.criticality
if PulseInstr == "climbing":
    PulseInstr = model.climbingpulse
print(model.params)

from Stimulator import Stimulator
simu = Stimulator(model, BaseStim, PulseInstr, init, n_T = 200)
simu.TimeSeries()
#simu.PhaseSpaceAnim(os.path.join(cwd, "Plots"), fname = "Anim")

import matplotlib.pyplot as plt
import numpy as np
# fromu = 0
# until = 5000
# plt.figure()
# plt.plot(simu.ts[fromu:until], simu.ys[fromu:until,0])
# plt.plot(simu.ts[fromu:until], simu.ys[fromu:until,1])
# plt.plot(simu.ts[fromu:until], simu.ys[fromu:until,2])
# plt.plot(simu.ts[fromu:until], simu.ys[fromu:until,3])
# plt.ylim(-4,4)
# plt.show()

# simu.TimeSeries(whichy = [0,1,2,3])
# simu.PhaseSpace(whichx = 0, whichy = 2)


#%% For RIM

tps = []
Vs = []
Iapps = np.linspace(BaseStim, 7, 20)
i = 0
for Iapp in Iapps:
    print(str(i))
    i += 1
    PulseInstr = [Iapp,0,10,10,1]
    simu = Stimulator(model, BaseStim, PulseInstr, init, n_T = 300)
    simu.TimeSeries()
    epsilon = np.linalg.norm(simu.ys-simu.ys[-1], axis = 1)
    lessthan1 = (2000 +np.where(epsilon[2000:] < 1)[0])[0]
    returntp = simu.ts[lessthan1]
    returnV = simu.ys[np.where(simu.ys[:,4] == Iapp)[0][-1]][0]
    tps.append(returntp)
    Vs.append(returnV)
    print(simu.ts[lessthan1])

#%% For AFD

    
# tps = []
# Vs = []
# Iapps = np.linspace(BaseStim, 20, 20)
# i = 0
# for Iapp in Iapps:
#     print(str(i))
#     i += 1
#     PulseInstr = [Iapp,0,10,10,1]
#     simu = Stimulator(model, BaseStim, PulseInstr, init, n_T = 300)
#     simu.TimeSeries()
#     epsilon = np.linalg.norm(simu.ys-simu.ys[-1], axis = 1)
#     lessthan1 = (2000 +np.where(epsilon[2000:] < 1)[0])[0]
#     returntp = simu.ts[lessthan1]
#     returnV = simu.ys[np.where(simu.ys[:,4] == Iapp)[0][-1]][0]
#     tps.append(returntp)
#     Vs.append(returnV)

#%% For AFD 2nd Bifurc
# init = [-19.60163931, 0.14521655, 0.09586589, 0.17472735]
# BaseStim = 17.40
# tps = []
# Vs = []
# Iapps = np.linspace(BaseStim, 35, 20)
# i = 0
# for Iapp in Iapps:
#     print(str(i))
#     i += 1
#     if i < 6:
#         t = 300
#     else:
#         t = 2000
#     PulseInstr = [Iapp,0,10,10,1]
#     simu = Stimulator(model, BaseStim, PulseInstr, init, n_T = t)
#     simu.TimeSeries()
#     epsilon = np.linalg.norm(simu.ys-simu.ys[-1], axis = 1)
#     lessthan1 = (2000 +np.where(epsilon[2000:] < 1)[0])[0]
#     returntp = simu.ts[lessthan1]
#     returnV = simu.ys[np.where(simu.ys[:,4] == Iapp)[0][-1]][0]
#     tps.append(returntp)
#     Vs.append(returnV)
#     # print(simu.ts[lessthan1])

# plt.figure()
# plt.scatter(Vs, tps)
# plt.xlabel("last V of Stimulus")
# plt.ylabel("Time until basal state is reached")
# plt.show()

# plt.figure()
# plt.scatter(Iapps, tps)
# plt.xlabel("Applied Stimulus")
# plt.ylabel("Time until basal state is reached")
# plt.show()

#%%

# tp = 100
# for tp in np.linspace(0, len(simu.ts), 100):
#     tp = int(tp)
#     print(tp)
#     Vrange, NulcV, Nulcm_Ca = model.NullclineVm_K(simu.ys[tp])
#     Vrange, NulcV, Nulcm_K = model.NullclineVm_K(simu.ys[tp])
#     Vrange, NulcV, Nulch_K = model.NullclineVh_K(simu.ys[tp])
    
#     plt.figure(figsize = (8,8))
#     timeseries = plt.subplot2grid((2,2), (0, 0))
#     NullclineVm_Ca = plt.subplot2grid((2,2), (0, 1))
#     NullclineVm_K = plt.subplot2grid((2,2), (1, 0))
#     NullclineVh_K =  plt.subplot2grid((2,2), (1, 1))
    
#     timeseries.plot(simu.ts, simu.ys[:,0], "k")
#     timeseries.set_xlabel("Time")
#     timeseries.set_ylabel("V")
#     timeseries.vlines(simu.ts[tp], min(simu.ys[:,0]), max(simu.ys[:,0]))
#     # timeseries.plot(simu.ys[:,-1])
    
#     NullclineVm_Ca.plot(NulcV, Vrange)
#     NullclineVm_Ca.plot(Nulcm_Ca, Vrange)
#     NullclineVm_Ca.scatter(simu.ys[tp,1], simu.ys[tp,0], color="red")
#     NullclineVm_Ca.set_xlabel("m_Ca")
#     NullclineVm_Ca.set_ylabel("V")
#     NullclineVm_Ca.set_xlim(-500,500)
    
#     NullclineVm_K.plot(NulcV, Vrange)
#     NullclineVm_K.plot(Nulcm_K, Vrange)
#     NullclineVm_K.scatter(simu.ys[tp,2], simu.ys[tp,0], color="red")
#     NullclineVm_K.set_xlabel("m_K")
#     NullclineVm_K.set_ylabel("V")
#     NullclineVm_K.set_xlim(-1,1)
    
#     NullclineVh_K.plot(NulcV, Vrange)
#     NullclineVh_K.plot(Nulch_K, Vrange)
#     NullclineVh_K.scatter(simu.ys[tp,3], simu.ys[tp,0], color="red")
#     NullclineVh_K.set_xlabel("h_K")
#     NullclineVh_K.set_ylabel("V")
#     NullclineVh_K.set_xlim(-1,1)
    
#     # plt.show()
    
#     plt.tight_layout()
#     plt.show()