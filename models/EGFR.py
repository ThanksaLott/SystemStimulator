# -*- coding: utf-8 -*-
"""
Created on Thu May 12 14:53:48 2022

@author: lott
GS d- s:+ a-- C++ t 5 X R tv b+ D+ G e+++ h r++ 
"""
import numpy as np
class model():
    def __init__(self):
        
        self.params = {
            "EGFRt" : 1.205,
            "RGt" : 1,
            "RJt" : 1,
            "N2t" : 1,
            "kd" : 5.56,
            "kon" : 0.001,
            "koff" : 5.56*0.001,
            "alph1" : 0.001,
            "alph2" : 0.3,
            "alph3" : 0.7,
            "Gamma1" : 1.9,
            "Gamma2" : 0.1,
            "GammaRJ" : 0.005,
            "epsilon" : 0.01,
            "k1" : 0.5,
            "k2" : 0.5,
            "k5" : 1.613,
            "b1" : 11,
            "b2" : 1.1
            }
        self.initdefault = [0.0, 0.1, 0.5, 0.0, 0.0, 0.1]
        self.initdim = 6

    
    def equations(self, t, y):
        EGFRp, RGa, RJa, EGFEGFRp, EGFEGFR, N2a, EGF = y
        
        RGi = self.params["RGt"] - RGa
        RJi = self.params["RJt"] - RJa
        N2i = self.params["N2t"] - N2a
        EGFR = self.params["EGFRt"] - (EGFRp + 2*EGFEGFR + 2*EGFEGFRp)
        
        dEGFRp = (EGFR*(self.params["alph1"]*EGFR + self.params["alph2"]*EGFRp 
                        + self.params["alph3"]*EGFEGFRp) 
                  - EGFRp*(self.params["Gamma1"]*RGa 
                           + self.params["GammaRJ"]*RJa 
                           + self.params["Gamma2"]*N2a) 
                  - self.params["kon"]*2*(EGFRp**2)*EGF 
                  + self.params["koff"]*EGFEGFRp)
        dRGa = (self.params["k1"]*RGi - self.params["k2"]*RGa 
                - self.params["b1"]*RGa*(EGFRp + 2*EGFEGFRp))
        dRJa = self.params["k1"]*RJi - self.params["k2"]*RJa 
        dEGFEGFRp = (self.params["k5"]*EGFEGFR - (self.params["GammaRJ"]*RJa
                                                  +self.params["Gamma2"]*N2a)*EGFEGFRp
                          + self.params["kon"]*(EGFRp**2 + EGFR**2)*EGF
                          - self.params["koff"]*EGFEGFRp)
        dEGFEGFR = (-self.params["k5"]*EGFEGFR 
                    + (self.params["GammaRJ"]*RJa 
                       +self.params["Gamma2"]*N2a)*EGFEGFRp 
                    - self.params["koff"]*EGFEGFR)
        dN2a = (self.params["epsilon"]*(self.params["k1"]*N2i 
                                       - self.params["k2"]*N2a 
                                       + self.params["b2"]*(EGFRp + 2*EGFEGFRp)*N2i))

        dEGF = 0
        dydt = np.array((dEGFRp, dRGa, dRJa, dEGFEGFRp, dEGFEGFR, dN2a, dEGF))
        return dydt
    
    def nullclines(self, y):
        """Computes nullclines, solved by n by setting V in a range"""
        EGFRp, RGa, RJa, EGFEGFRp, EGFEGFR, N2a, EGF = y
        del EGFRp
        EGFRpRange = np.linspace(0.002,1,500)
        
        # EGFEGFR = self.TimeEvolution.loc[TP, "EGFEGFR"]
        # EGFEGFRp = self.TimeEvolution.loc[TP, "EGFEGFRp"]
        # EGF = self.TimeEvolution.loc[TP, "EGF_stim"]
        # RJa = self.TimeEvolution.loc[TP, "RJa"]
        # N2a = self.TimeEvolution.loc[TP, "N2a"]
        EGFR = self.params["EGFRt"] - (EGFRpRange + 2*EGFEGFR + 2*EGFEGFRp)
        
        
        EGFRnul = ((EGFR*(self.params["alph1"]*EGFR 
                          + self.params["alph2"]*self.EGFRpRange
                          +self.params["alph3"]*EGFEGFRp)
                    -self.EGFRpRange*(self.params["GammaRJ"]*RJa
                                      +self.params["Gamma2"]*N2a)
                    -2*self.params["kon"]*(self.EGFRpRange**2)*EGF
                    +self.params["koff"]*EGFEGFRp) 
                   / (self.EGFRpRange*self.Gamma1))
        #NulcN = (1/(1+np.exp((V12n-Vrange)/kn)))\
        RGnul = ((self.params["k1"]*self.RGt) 
                 / ((self.params["k1"] + self.params["k2"] 
                     + self.params["b1"]*self.EGFRpRange 
                     + self.params["b1"]*2*EGFEGFRp)))
        return EGFRnul, RGnul, EGFRpRange