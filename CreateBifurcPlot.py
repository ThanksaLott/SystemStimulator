# -*- coding: utf-8 -*-
"""
Created on Tue May 17 15:40:32 2022

@author: lott
GS d- s:+ a-- C++ t 5 X R tv b+ D+ G e+++ h r++ 
"""

file = 'C:/xppall/AFD_Points.dat'
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
a = pd.read_csv(file, delimiter = " ")


stab = np.where(a.iloc[:,3] == 1)[0]
instab = np.where(a.iloc[:,3] > 1)[0]
plt.figure()
plt.plot(a.iloc[:instab[0],0], a.iloc[:instab[0],1], "k")
plt.plot(a.iloc[instab[0]:1088,0], a.iloc[instab[0]:1088,1], "r--")
plt.plot(a.iloc[1088:1484,0], a.iloc[1088:1484,1], "k")
plt.plot(a.iloc[1484:instab[-1],0], a.iloc[1484:instab[-1],1], "r--")
plt.plot(a.iloc[instab[-1]:,0], a.iloc[instab[-1]:,1], "k")
# plt.vlines(a.iloc[instab[-1],0], -40, 20, "magenta") # for RIM
#plt.vlines(a.iloc[1088,0], -90, 20, "magenta")
plt.vlines(a.iloc[instab[-1],0], -90, 20, "magenta")
plt.xlim(0,30)
plt.ylim(-90,20)
plt.xlabel("Iapp")
plt.ylabel("V")
plt.title("Bifurcation diagram of AFD model")