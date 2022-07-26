# -*- coding: utf-8 -*-
"""
Created on Mon May 16 13:36:17 2022

@author: lott
GS d- s:+ a-- C++ t 5 X R tv b+ D+ G e+++ h r++ 
"""

import numpy as np
class model():
    def __init__(self):
        
        self.params = {
            "Rt" : 1,
            "k_in":6,
            "k_out":0.03,
            "k_open":0.1,
            "k_close":0.1,
            "k_shutclose": 0.4,
            "k_shutopen": 0.2,
            "ContractThresh":6
            }
        self.initdefault = [0,0,1,0]
        self.initdim = 3
    
    def Ro2Rc1(self):
        pass
    
    def Rc12Rc2(self):
        pass
    
    
    def equations(self, t, y):
        Ca, Ro, Rc1, Rc2, Stim = y
        
        # dRa = self.params["k_on"]*Ri - self.params["k_off"]*Ra*(np.exp(Ca-self.params["ContractThresh"]))
        # dRi = self.params["k_off"]*Ra*(np.exp(Ca-self.params["ContractThresh"]))- self.params["k_on"]*Ri
        
        dCa = self.params["k_in"]*Ro - Ca*self.params["k_out"]
        dRo = self.params["k_open"]*Stim*Rc1 - self.params["k_close"]*Ro
        dRc1 = (self.params["k_close"]*Ro + Rc2*self.params["k_shutopen"] 
                - self.params["k_open"]*Stim*Rc1 
                - np.exp(Ca-self.params["ContractThresh"])*Rc1*self.params["k_shutclose"])
        dRc2 = np.exp(Ca-self.params["ContractThresh"])*Rc1*self.params["k_shutclose"] - Rc2*self.params["k_shutopen"]
        

        dStim = 0
        dydt = np.array((dCa, dRo, dRc1, dRc2, dStim))
        return dydt
    
    def nullclines(self, y):
        """Computes nullclines, solved by n by setting V in a range"""
        Ra, PDNFa, LRa, LT = y
        
        RaRange = np.linspace(0.0005,1,500)
        NulcRa = ((self.params["kR"]*((self.params["Rt"] - self.RaRange - LRa)*(self.params["alph1"]*(self.params["Rt"] - self.RaRange - LRa) + self.params["alph2"]*self.RaRange + self.params["alph3"]*LRa)) - self.params["kon"]*self.RaRange*LT + 1/2*self.params["koff"]*LRa) / (self.params["kR"]*self.params["gammaDNF"]*self.RaRange))
        NulcPDNFa = ((self.params["k1"]*self.params["PDNFt"]  + self.params["kon"]*self.RaRange*LT - 1/2*self.params["koff"]*LRa) / (self.params["k1"] *(1 + self.params["k2_1"] + self.params["bDNF"]*(self.RaRange + LRa))))
        return NulcRa, NulcPDNFa, RaRange
    