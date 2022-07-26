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
        self.modylabels = model.ylabels
        
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
            #print(tp)
            if tp == 0:
                solve = scipy.integrate.RK45(self.equations, tp, X_init, tp+1, max_step = self.delT)
            else:
                X_init = solve.y #np.array([solve.y[0], solve.y[1], self.Stimulus[tp]])
                X_init[-1] = self.Stimulus[tp]
                solve = scipy.integrate.RK45(self.equations, tp, X_init, tp+1, max_step = self.delT)
            while solve.status == 'running':
                solve.step()
                ys.append(solve.y)
                ts.append(solve.t)
        self.ys = np.array(ys)
        self.stims = self.ys[:,self.ys.shape[1]-1]
        self.ts = np.array(ts)
        self.n_TPs = len(ts)
        
    def NullclinesStim(self, y):
        """Computes nullclines dependent on a stimulus"""
        XRange, NulcX, NulcY = self.nullclines(y)
        return XRange, NulcX, NulcY
    
    def NullclinesTP(self, tp):
        """Computes nullclines dependent on a stimulus"""
        y = self.ys[tp,:]
        XRange, NulcX, NulcY = self.nullclines(y)
        return XRange, NulcX, NulcY

    def TimeSeries(self, whichy = 0, start = 0, end = -1, path:str = None, 
                   fname:str = None, title = None, ymax = None, ymin = None):
        #TODO: Better description of what whichy does, maybe better name
        """Plots a TimeSeries.
        
        Parameters:
            whichy : int or list default 0
                Determines which component of the ys is used
            start : int default 0
                Timepoint where the timeseries starts
            stop : int default -1
                Timepoint where the timeseries ends
            path : str or path-like default None
                Path in which the plot will be saved.
            fname : str default None
                Filename for the plot. Needs to include a datatype fileending"""
            
        start, end = self.CheckStartEndTimes(start, end)
        
        fig, ax = plt.subplots()
        if type(whichy) == int:
            plt.plot(self.ts, self.ys[:,whichy]) #, label = "V")
            plt.ylabel(self.modylabels[whichy])
        elif type(whichy) == list:
            for i in whichy:
                plt.plot(self.ts, self.ys[:,i], label = self.modylabels[i])
                plt.legend()
        
        pstart = self.Pulse_start
        for i in range(self.Repeats):
            pstop = pstart + self.Pulse_length
            ax.axvspan(pstart,pstop, alpha=0.3, color = "k", linewidth = 0)
            pstart+=(self.Interpulse + self.Pulse_length)

        plt.title("Stim = " + str(max(self.Stimulus)))
        plt.xlim(self.ts[start], self.ts[end-1])
        
        if ymax == None:
            ymax = np.nanmax(self.ys[start:end, whichy])
            if ymax >0: ymax += ymax*0.05
            else: ymax -= ymax*0.05
        if ymin == None:
            ymin = np.nanmin(self.ys[start:end, whichy])
            if ymin >0: ymin -= ymin*0.05
            else: ymin += ymin*0.05
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
                   end = -1, linescatter = "scatter", nullclines = None):
        #TODO: Write docstring+
        start, end = self.CheckStartEndTimes(start, end)
        
        plt.figure()
        if linescatter == "line":
            plt.plot(self.ys[start:end, whichx], self.ys[start:end, whichy])
        if linescatter == "scatter":
            cmap = cm.spring(np.abs(self.stims[start:end]-self.BaseStim))
            plt.scatter(self.ys[start:end, whichx], self.ys[start:end, whichy], 
                        s = 0.5, alpha = 0.8, color = cmap)
        plt.xlabel(self.modylabels[whichx])
        plt.ylabel(self.modylabels[whichy])
        if nullclines:
            x, y1, y2 = self.nullclines
        # plt.xlim(-60,-10)
        plt.show()
        
    def PhaseSpaceAnim(self, path, fname, TSy = 0, PSx = 0, PSy = 1, start = 0, 
                   end = -1, frame_num = 100, removepng = False):
        #TODO: Write docstring
        """Generates an animation of the phase space and the time series.
        
        Parameters:
            TSy : int or list default 0
                Determines which component(s) of the ys is used to plot the timeseries
            PSx : int default 0
                Determines which component is used on the x-axis of the phase-
                space plot
            PSy : int default 0
                Determines which component is used on the y-axis of the phase-
                space plot
            start : int default 0
                Timepoint where the timeseries starts
            stop : int default -1
                Timepoint where the timeseries ends
            frame_num: int default 100
                Determines how many frames are generated for the animation
            path : str or path-like default None
                Path in which the plot will be saved.
            fname : str default None
                Filename for the plot. Needs to include a datatype fileending"""
        start, end = self.CheckStartEndTimes(start, end)

        print("Generating the Animation...")
        xRange, NulcX, NulcY = self.NullclinesTP(0)
        minimy = min([np.nanmin(NulcX), np.nanmin(NulcY)])
        maximy = max([np.nanmax(NulcX), np.nanmax(NulcY)])
        frame = 0
        for tp in np.linspace(start+1,end-1, frame_num):
            tp = int(tp)
            
            sys.stdout.write('\r')
            sys.stdout.write("[%-20s] %d%%, tp = %s, n_tp = %s" % 
                              ('='*int(20*(tp+1)/self.n_TPs), 
                              100*(tp+1)/self.n_TPs, str(tp), str(self.n_TPs)))
            sys.stdout.flush()
            xRange, NulcX, NulcY = self.NullclinesTP(tp)
            
        
            cmap = cm.jet(np.abs(self.ys[0:tp:50,-1]))
            
            # if self.TimeEvolution.loc[tp,"LT"] > 0:
            #     trajcolor = "red"
            # else: trajcolor = "black"
            
            plt.figure(figsize = (8,5))
            plot1 = plt.subplot2grid((2,6), (0, 0), colspan = 2)
            plot2 = plt.subplot2grid((2,6), (1, 0), colspan = 2)
            plot3 = plt.subplot2grid((2,6), (0, 2), rowspan = 2, colspan = 4)
        
            # plot1.plot(TwoDBifurc.iloc[:,0], TwoDBifurc.iloc[:,1], color = "green")
            # plot1.scatter(self.gammaDNF, self.TimeEvolution.loc[tp,"LRa"], color = cmap[-1])
            # plot1.set_xlabel("gammaDNF")
            # plot1.set_ylabel("LRa")
            
            if type(TSy) == int:
                plot2.plot(self.ys[:,TSy], color = "blue")
            elif type(TSy) == list:
                for i in TSy:
                    plot2.plot(self.ys[:,i], color = "blue", label = self.modylabels[i])
                plot2.legend()
            plot2.vlines(tp, np.nanmin(self.ys[:,TSy]), np.nanmax(self.ys[:,TSy]), color = "k")
            plot2.set_xlabel("Time")
            plot2.set_ylabel("Response")
            plot2.set_ylim(np.nanmin(self.ys[:,TSy]), np.nanmax(self.ys[:,TSy]))
            
            plot3.scatter(self.ys[start:tp:50,PSx], self.ys[start:tp:50,PSy], color = cmap, s = 0.5, alpha = 0.8)
            plot3.plot(xRange, NulcX, lw = 1, color = "g")
            plot3.plot(xRange, NulcY, lw = 1, color = "m")
            plot3.scatter(self.ys[tp,PSx], self.ys[tp,PSy], color = cmap[-1])
            plot3.set_xlabel(self.modylabels[PSx])
            plot3.set_ylabel(self.modylabels[PSy])
            # plot3.set_xlim(0.01, 0.7)
            plot3.set_ylim(minimy, maximy)
            
            plt.tight_layout()
            plt.savefig(os.path.join(path, "tempfileani2%05d.png" % frame))
            frame +=1
            plt.close()
            
        os.chdir(path)
        subprocess.call([
            'ffmpeg', '-framerate', '8', '-i', 'tempfileani2%05d.png', '-r', '30', '-pix_fmt', 'yuv420p',
            fname + '.mp4'
        ])
        
        if removepng:
            for file_name in os.listdir(path):
                if file_name.startswith("tempfileani2") and file_name.endswith(".png"):
                    os.remove(file_name)
        
        
        
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
    
    def CheckStartEndTimes(self, start, end):
        """Makes sure that starting and ending times are proper."""
        
        if end != -1 and start > end:
            raise Warning ((" in drawing PhaseSpaceAnim! Starting point after"
                            + " endpoint. Will try to switch around."))
            inb = end
            end = start
            start = inb
            del inb
        
        if end == -1:
            end = len(self.ts)
        elif end > max(self.ts):
            raise Warning ((" in drawing PhaseSpaceAnim! Simulation ended"
                            + " before the timepoint given is reached.Now"
                            + " depicting the whole simulation."))
            end = len(self.ts)
        else:
            end = np.where(np.array(self.ts) == end)[0][0]
        if start == 0:
            start == 0
        elif start < min(self.ts):
            raise Warning ((" in drawing PhaseSpaceAnim! Starting timepoint below"
                            + " first tp in Simulation."
                            + " Will use the very first point instead."))
            start = 0
        else:
            start = np.where(np.array(self.ts) == start)[0][0] 
        return start, end