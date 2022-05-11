# -*- coding: utf-8 -*-
"""
Created on Wed May 11 11:21:38 2022

@author: lott
GS d- s:+ a-- C++ t 5 X R tv b+ D+ G e+++ h r++ 
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from numba import jit
import sdeint
import os
import subprocess
import sys
import scipy.integrate

#TODO: proper way of getting variable names to use in plotting labels
class Stimulator():
    
    def __init__(self, model, BaseStim, PulseInstr, init, n_T=300, delT=0.01):
        self.equations = model.equations
        self.nullclines = model.nullclines
        
        self.n_T = n_T
        self.delT=delT
        
        self.BaseStim = BaseStim
        self.PulseInstr = PulseInstr
        self.UnpackPulseInstructions()
        self.GenerateStimulus()
        
        if init in ["find", "Find", "SS", "steadystate"]:
            self.init = self.FindSteadyState()
        else: 
            init = np.array(init)
            self.init = np.append(init, BaseStim)
        
        #self.CheckImported()
        self.RunSimulation()
    
    def CheckImported(self):
        """"Used to make sure that the correct thing was imported"""
        print("Yes, the stimulator was imported.")
    
    def UnpackPulseInstructions(self):
        """Unpacks how to create pulses from Instructions.
        
        These instructions are either list or array of len 5. First position
        describes the strength, second the start point, third the length,
        fourth the interpulse duration and fifth the amount of repeats"""
        self.Pulse_strength = self.PulseInstr[0]
        self.Pulse_start = int(self.PulseInstr[1])
        self.Pulse_length = int(self.PulseInstr[2])
        self.Interpulse = int(self.PulseInstr[3])
        try:
            self.Repeats = self.PulseInstr[4]
        except IndexError:
            self.Repeats = 1
        
    def GenerateStimulus(self):
        """Generates the amount of stimulus present at each timepoint.
        
        #Pulse_strength:float, Pulse_start:int, Pulse_length:int, 
            Interpulse:int, Repeats:int = 1
        Parameters:
            Pulse_strength:float - Amount of stimulus
            BaseStim:float - Amount of stimulus in absense of pulse
            Pulse_start:int - Timepoint at which pulse (train) starts
            Pulse_length:int - Duration of the pulse
            Interpulse:int - Time between pulses
            Repeats:int - Amount of repetition, must be >=1 for pulses.
        
        Returns:
            Stimulus:np.array - Amount of stimulus at each TP."""
        Stimulus = self.BaseStim * np.ones(self.n_T)
        start=self.Pulse_start
        for i in range(self.Repeats):
            stop = start + self.Pulse_length
            Stimulus[start:stop] = self.Pulse_strength
            start+=(self.Interpulse + self.Pulse_length)
        self.Stimulus = Stimulus
        return Stimulus
    
    def RunSimulation(self):
        X_init = self.init #np.array([-44.3195622 , 0.53396948, self.BaseStim])
        ys = []
        ts = []

        for tp in range(0, self.n_T):
            if tp == 0:
                solve = scipy.integrate.RK45(self.equations, tp, X_init, tp+1, max_step = self.delT)
            else:
                X_init = np.array([solve.y[0], solve.y[1], self.Stimulus[tp]])
                solve = scipy.integrate.RK45(self.equations, tp, X_init, tp+1, max_step = self.delT)
            while solve.status == 'running':
                solve.step()
                ys.append(solve.y)
                ts.append(solve.t)
                # print("y = " + b.ystr(b.y))
                # print("t = " + str(b.t))
        self.ys = np.array(ys)
        self.stims = self.ys[:,self.ys.shape[1]-1]
        self.ts = np.array(ts)
        self.n_TPs = len(ts)
        
    def Nullclines(self, Stim):
        """Computes nullclines, as specified in model class"""
        NulcX, NulcY, XRange = self.model.nullclines(Stim)
        return NulcX, NulcY

    def TimeSeries(self, whichy = 0, start = 0, end = -1, path:str = None, 
                   fname:str = None, title = None, ymax = None, ymin = None):
        #TODO: Better description of what whichy does, maybe better name
        """Plots a TimeSeries.
        
        Parameters:
            whichy : int default 0
                Determines which component of the ys is used
            start : int default 0
                Timepoint where the timeseries starts
            stop : int default -1
                Timepoint where the timeseries ends
            path : str or path-like default None
                Path in which the plot will be saved.
            fname : str default None
                Filename for the plot. Needs to include a datatype fileending"""
            
        if end != -1 and start > end:
            raise Warning((" in drawing TimeSeries! Starting point after "
                           + "endpoint. Will try to switch around."))
            inb = end
            end = start
            start = inb
            del inb
        
        if end == -1:
            end = len(self.ts)
        elif end > max(self.ts):
            raise Warning((" in drawing TimeSeries! Simulation ended"
                           + " before the timepoint given is reached. Now "
                           + "depicting the whole simulation."))
            end = len(self.ts)
        else:
            end = np.where(np.array(self.ts) == end)[0][0]
        if start == 0:
            start == 0
        elif start < min(self.ts):
            raise Warning(("Warning in drawing TimeSeries! Starting timepoint"
                           + " below first tp in Simulation. will use the very"
                           + " first point instead."))
            start = 0
        else:
            start = np.where(np.array(self.ts) == start)[0][0]
        
        fig, ax = plt.subplots()
        plt.plot(self.ts, self.ys[:,whichy]) #, label = "V")
        
        pstart = self.Pulse_start
        for i in range(self.Repeats):
            pstop = pstart + self.Pulse_length
            ax.axvspan(pstart,pstop, alpha=0.3, color = "k", linewidth = 0)
            pstart+=(self.Interpulse + self.Pulse_length)

        plt.title("Stim = " + str(max(self.Stimulus)))
        plt.xlim(self.ts[start], self.ts[end-1])
        
        if ymax == None:
            ymax = np.nanmax(self.ys[start:end, whichy])
            ymax += ymax*0.05
        if ymin == None:
            ymin = np.nanmin(self.ys[start:end, whichy])
            ymin += ymin*0.05
        plt.ylim(ymin,ymax)
        plt.xlabel("time")
        #plt.ylabel("V")
        # plt.legend()
        if not path == None:
            if not os.path.isdir(path): os.mkdir(path)
            plt.savefig(os.path.join(path,fname))
            return
        plt.show()
        return
    

    
    def PhaseSpace(self, whichx = 0, whichy = 1, start = 0, 
                   end = -1, linescatter = "scatter"):
        #TODO: Write docstring
        if end != -1 and start > end:
            raise Warning ((" in drawing PhaseSpace! Starting point after"
                            + " endpoint. Will try to switch around."))
            inb = end
            end = start
            start = inb
            del inb
        
        if end == -1:
            end = len(self.ts)
        elif end > max(self.ts):
            raise Warning ((" in drawing PhaseSpace! Simulation ended"
                            + " before the timepoint given is reached.Now"
                            + " depicting the whole simulation."))
            end = len(self.ts)
        else:
            end = np.where(np.array(self.ts) == end)[0][0]
        if start == 0:
            start == 0
        elif start < min(self.ts):
            raise Warning ((" in drawing PhaseSpace! Starting timepoint below"
                            + " first tp in Simulation."
                            + " Will use the very first point instead."))
            start = 0
        else:
            start = np.where(np.array(self.ts) == start)[0][0]
        
        plt.figure()
        if linescatter == "line":
            plt.plot(self.ys[start:end, whichx], self.ys[start:end, whichy])
        if linescatter == "scatter":
            cmap = cm.spring(np.abs(self.stims[start:end]-self.BaseStim))
            plt.scatter(self.ys[start:end, whichx], self.ys[start:end, whichy], 
                        s = 0.5, alpha = 0.8, color = cmap)
        plt.xlabel("V")
        plt.ylabel("n")
        plt.xlim(-60,-10)
        plt.show()
        
    def MaxDuringPulses(self, whichy = 0):
        """Creates and returns a DataFrame containing the maximal Values of 
        a parameter recorded at each stimulus. This is counted from
        stimulus start till end of the Interpulse.
        
        Parameters:
            whichy : int default 0
                Determines which component of the ys is used"""
        cols = ["V"]
        rows = []
        for i in range(self.Repeats):
            rows.append("Pulse_" + str(i))
        df = pd.DataFrame(np.zeros((self.Repeats, 1)), index = rows, columns = cols)
        for i in range(self.Repeats):
            start = np.where(self.ts == self.Pulse_start + i*(self.Pulse_length+self.Interpulse))[0][0]
            end = np.where(self.ts ==self.Pulse_start + (i+1)*(self.Pulse_length+self.Interpulse))[0][0]
            maxY = self.ys[start:end,whichy].max()
            
            df.loc["Pulse_" + str(i), "V"] = maxY
        return df