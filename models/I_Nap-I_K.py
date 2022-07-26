# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:57:10 2022

@author: lott
GS d- s:+ a-- C++ t 5 X R tv b+ D+ G e+++ h r++ 
"""
import numpy as np
class model():
    def __init__(self):
        
        self.params = {
            "gl": 1,
            "El":-78,
            "gna":2.7,
            "Ena":60,
            "gk":4,
            "Ek":-90,
            "C":1,
            "V12n":-45,
            "kn":5,
            "V12m":-30,
            "km":7
            }
        self.initdefault = [-44.43651909,   0.52814426]    
        self.initdim = 2
        self.ylabels = ["V", "n", "Iapp"]
        self.criticality = 98.01
        self.climbingpulse = [110.5, 10, 2, 4, 2]
        self.initdim = 4
        self.ylabels = ["V", "m_Ca", "m_K", "h_K", "Iapp"]

    
    # BaseStim=98.01, n_T=300, delT=0.01,gl=1, El=-78, 
    #              gna=2.7, Ena=60, gk=4, Ek=-90, C=1, V12n=-45, kn=5, V12m=-30, 
    #              km=7)

    def Ileak(self, V):
        return self.params["gl"]*(V-self.params["El"])
    def Ina(self, V):
        return self.params["gna"]*self.minf(V)*(V-self.params["Ena"])
    def Ik(self, V,n):
        return self.params["gk"]*n*(V-self.params["Ek"])
    def ninf(self, V):
        return 1/(1+np.exp((self.params["V12n"]-V)/self.params["kn"]))
    def minf(self, V):
        return 1/(1+np.exp((self.params["V12m"]-V)/self.params["km"]))
    def tau(self, V):
        return 1

    
    def equations(self, t, y):
        V, n, Iapp = y
        
        dV = (Iapp - self.Ileak(V) - self.Ina(V) - self.Ik(V,n))/self.params["C"]#+np.random.randn()
        dn = (self.ninf(V) - n)/self.tau(V)+0.05*np.random.randn()
        dIapp = 0
        dydt = np.array((dV, dn, dIapp))
        return dydt
    
    def nullclines(self, y):
        """Computes nullclines, solved by n by setting V in a range"""
        V, n, Iapp = y
        
        Vrange = np.linspace(-89,20, 500)
        NulcV = ((Iapp-self.Ileak(Vrange)-self.Ina(Vrange))
                 /(self.params["gk"]*(Vrange-self.Ek)))
        #NulcN = (1/(1+np.exp((V12n-Vrange)/kn)))\
        NulcN = self.ninf(Vrange)
        return NulcV, NulcN, Vrange
    