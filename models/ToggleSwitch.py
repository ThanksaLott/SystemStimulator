# -*- coding: utf-8 -*-
"""
Created on Thu May 12 16:12:05 2022

@author: lott
GS d- s:+ a-- C++ t 5 X R tv b+ D+ G e+++ h r++ 
"""

import numpy as np
class model():
    def __init__(self):
        
        self.params = {
            "gammaDNF" : 2.957,
            "Rt" : 1,
            "PDNFt" :  1,
            "alph1" : 0.0017,
            "alph2" : 0.3,
            "alph3" : 1.0,
            "kR" : 0.8,
            "k1" : 0.01,
            "k2_1" : 0.5,
            "bDNF" : 36.0558,
            "kon" : 0.003,
            "koff" : 0.01668
            }
        
        self.initdim = 3
    
    def equations(self, t, y):
        Ra, PDNFa, LRa, LT = y
        
        dRa = (self.params["kR"]*((self.params["Rt"] - Ra - LRa)*(self.params["alph1"]*(self.params["Rt"] - Ra - LRa) + self.params["alph2"]*Ra + self.params["alph3"]*LRa) - self.params["gammaDNF"]*PDNFa*Ra) - self.params["kon"]*Ra*LT + 1/2*self.params["koff"]*LRa)
        dPDNFa = (self.params["k1"]*((self.params["PDNFt"] - PDNFa) - self.params["k2_1"]*PDNFa -self.params["bDNF"]*PDNFa*(Ra + LRa)) + self.params["kon"]*Ra*LT - 1/2*self.params["koff"]*LRa)
        dLRa = self.params["kon"]*(Ra + (self.params["Rt"] - Ra - LRa))*LT - self.params["koff"]*LRa
        dLT = 0
        dydt = np.array((dRa, dPDNFa, dLRa, dLT))
        return dydt
    
    def nullclines(self, y):
        """Computes nullclines, solved by n by setting V in a range"""
        Ra, PDNFa, LRa, LT = y
        
        RaRange = np.linspace(0.0005,1,500)
        NulcRa = ((self.params["kR"]*((self.params["Rt"] - self.RaRange - LRa)*(self.params["alph1"]*(self.params["Rt"] - self.RaRange - LRa) + self.params["alph2"]*self.RaRange + self.params["alph3"]*LRa)) - self.params["kon"]*self.RaRange*LT + 1/2*self.params["koff"]*LRa) / (self.params["kR"]*self.params["gammaDNF"]*self.RaRange))
        NulcPDNFa = ((self.params["k1"]*self.params["PDNFt"]  + self.params["kon"]*self.RaRange*LT - 1/2*self.params["koff"]*LRa) / (self.params["k1"] *(1 + self.params["k2_1"] + self.params["bDNF"]*(self.RaRange + LRa))))
        return NulcRa, NulcPDNFa, RaRange
    