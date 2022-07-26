# -*- coding: utf-8 -*-
"""
Created on Mon May 16 16:39:31 2022

@author: lott
GS d- s:+ a-- C++ t 5 X R tv b+ D+ G e+++ h r++ 
"""
# Climbing activity achieved with:
# init = [-16.54556821, 0.53893609, 0.72679945, 0.2646773]
# PulseInstr = [5,30,10,10,5]
# BaseStim = 4.41

import numpy as np
class model():
    def __init__(self):
        
        self.params = {
            "g_Ca":0.24,
            "g_Kir":0.332,
            "g_K":0.127,
            "g_L":0.28,
            "E_Ca":105.3,
            "E_K":-100,
            "E_L":-81.3,
            "VmCa":-21.04,
            "VhCa":0,
            "VhKir":-89.99,
            "VmK":-17.7,
            "VhK":-21.28,
            "k_mCa":28.8,
            "k_hCa":0,
            "k_hKir":-1.2,
            "k_mK":1.18,
            "k_hK":-4.64,
            "tau_mCa":0.16,
            "tau_hCa":0,
            "tau_mK":0.2,
            "tau_hK":5.08,
            "m0_Ca":0.349,
            "h0_Ca":0,
            "m0_K":0.79,
            "h0_K":0.13,
            "C":0.02
            }
        self.initdefault = [-16.55203883,   0.53887935,   0.72568689,   0.26523059]    
        self.criticality = 4.41
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
    
        
    