# -*- coding: utf-8 -*-
"""
Created on Thu May 19 14:14:50 2022

@author: lott
GS d- s:+ a-- C++ t 5 X R tv b+ D+ G e+++ h r++ 
"""

import numpy as np
class model():
    def __init__(self):
        
        self.params = {
            "g_Ca":0.1,
            "g_Kir":1.92,
            "g_K":12.62,
            "g_L":0.1,
            "E_Ca":144.38,
            "E_K":-83.7,
            "E_L":-63.27,
            "VmCa":-16.34,
            "VhCa":0,
            "VhKir":-67.44,
            "VmK":-3.31,
            "VhK":-65.4,
            "k_mCa":1.84,
            "k_hCa":0,
            "k_hKir":-11.46,
            "k_mK":7.26,
            "k_hK":-29.5,
            "tau_mCa":6.64,
            "tau_hCa":0,
            "tau_mK":0.082,
            "tau_hK":3.63,
            "m0_Ca":0.002,
            "h0_Ca":0,
            "m0_K":0.001,
            "h0_K":0.991,
            "C":0.049
            }
        self.initdefault = [-82.432, 0, 0, 0.640] 
        self.criticality = 10.04
        self.climbingpulse = [5,30,10,10,10]
        self.initdim = 4
        self.ylabels = ["V", "m_Ca", "m_K", "h_K", "Iapp"]


    def h_Kirinf(self, V):
        return 1/(1+np.exp((self.params["VhKir"]-V)/self.params["k_hKir"]))
    def m_Cainf(self, V):
        return 1/(1+np.exp((self.params["VmCa"]-V)/self.params["k_mCa"]))
    def m_Kinf(self, V):
        return 1/(1+np.exp((self.params["VmK"]-V)/self.params["k_mK"]))
    def h_Kinf(self, V):
        return 1/(1+np.exp((self.params["VhK"]-V)/self.params["k_hK"]))
    def equations(self, t, y):
        V, m_Ca, m_K, h_K, I = y
        
        dV = (-self.params["g_Ca"]*m_Ca*(V-self.params["E_Ca"]) 
              - self.params["g_Kir"]*self.h_Kirinf(V) * (V-self.params["E_K"]) 
              - self.params["g_K"]*m_K*h_K*(V-self.params["E_K"])
              -self.params["g_L"]*(V-self.params["E_L"]) + I)/self.params["C"]
        dm_Ca = (self.m_Cainf(V)-m_Ca)/self.params["tau_mCa"]
        dm_K = (self.m_Kinf(V)-m_K)/self.params["tau_mK"]
        dh_K = (self.h_Kinf(V)-h_K)/self.params["tau_hK"]
        dI = 0
        dydt = np.array((dV, dm_Ca, dm_K, dh_K, dI))
        return dydt
    
    def nullclines(self, y):
        """Computes nullclines, solved by m_Ca by setting V in a range"""
        V, m_Ca, m_K, h_K, I = y
        
        Vrange = np.linspace(-90,90, 500)
        NulcV = ((- self.params["g_Kir"]*self.h_Kirinf(Vrange) * (Vrange-self.params["E_K"]) 
                 - self.params["g_K"]*m_K*h_K*(Vrange-self.params["E_K"])
                 -self.params["g_L"]*(Vrange-self.params["E_L"]) + I)
                 /(self.params["g_Ca"]*(Vrange-self.params["E_Ca"])))
        
        Nulcm_Ca = self.m_Cainf(Vrange)
        # Nulcm_K = self.m_Kinf(Vrange)
        # nulch_K = self.h_Kinf(Vrange)
        return Vrange, NulcV, Nulcm_Ca#, Nulcm_K, nulch_K
    
    def NullclineVm_Ca(self, y):
        V, m_Ca, m_K, h_K, I = y
        
        Vrange = np.linspace(-90,90, 500)
        NulcV = ((- self.params["g_Kir"]*self.h_Kirinf(Vrange) * (Vrange-self.params["E_K"]) 
                 - self.params["g_K"]*m_K*h_K*(Vrange-self.params["E_K"])
                 -self.params["g_L"]*(Vrange-self.params["E_L"]) + I)
                 /(self.params["g_Ca"]*(Vrange-self.params["E_Ca"])))
        
        Nulcm_Ca = self.m_Cainf(Vrange)
        return Vrange, NulcV, Nulcm_Ca#, Nulcm_K, nulch_K
    
    def NullclineVm_K(self, y):
        V, m_Ca, m_K, h_K, I = y
        
        Vrange = np.linspace(-90,90, 500)
        NulcV = ((-self.params["g_Ca"]*m_Ca*(Vrange-self.params["E_Ca"]) 
                  - self.params["g_Kir"]*self.h_Kirinf(Vrange) * (Vrange-self.params["E_K"]) 
                  -self.params["g_L"]*(Vrange-self.params["E_L"]) + I) 
                 / (self.params["g_K"]*h_K*(Vrange-self.params["E_K"]) ))
        
        Nulcm_K = self.m_Kinf(Vrange)
        return Vrange, NulcV, Nulcm_K

    def NullclineVh_K(self, y):
        V, m_Ca, m_K, h_K, I = y
        
        Vrange = np.linspace(-90,90, 500)
        NulcV = ((-self.params["g_Ca"]*m_Ca*(Vrange-self.params["E_Ca"]) 
                  - self.params["g_Kir"]*self.h_Kirinf(Vrange) * (Vrange-self.params["E_K"]) 
                  -self.params["g_L"]*(Vrange-self.params["E_L"]) + I) 
                 / (self.params["g_K"]*m_K*(Vrange-self.params["E_K"]) ))
        
        Nulch_K = self.h_Kinf(Vrange)
        return Vrange, NulcV, Nulch_K