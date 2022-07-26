# -*- coding: utf-8 -*-
"""
Created on Wed May 18 14:36:49 2022

@author: lott
GS d- s:+ a-- C++ t 5 X R tv b+ D+ G e+++ h r++ 
"""

import numpy as np
class model():
    def __init__(self):
        
        self.params = {
            "At":1,
            "Bt":1,
            "Ct":1,
            "Aneg":0.5,
            "kStim":1,
            "kCA":1,
            "kCStim":1,
            "kAB":1,
            "kBC":1,
            }
        self.initdefault = [0.0, 0.0, 0.0]
        self.initdim = 3
        self.ylabels = ["A", "B", "C", "Stim"]

    
    def equations(self, t, y):
        A, B, C, Stim = y

        dA = ((self.params["kStim"]-self.params["kStim"]*self.params["kCStim"]*C)*Stim-A*self.params["Aneg"])  *(self.params["At"]-A)
        dB = (self.params["kAB"]*A) *(self.params["Bt"]-B)
        dC = (self.params["kBC"]*B) *(self.params["Ct"]-C)
        dStim = 0
        dydt = np.array((dA, dB, dC, dStim))
        return dydt
    
    def nullclines(self):
        pass