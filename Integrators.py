# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 14:59:00 2022

@author: lott
GS d- s:+ a-- C++ t 5 X R tv b+ D+ G e+++ h r++ 
"""

import pandas as pd
import numpy as np

class SingleStepIntegrator():
    # 1 Insert values in eqs
    # 2 evaluate eqs
    # 3 Save results as new values
    # Repeat
    
    # Create a dictionary that holds the values
    def __init__(self, initdict, diffeqdict, StimulusParameter, StimulusInstr, n_TPs, dt = 0.01):
        self.initdict = initdict
        self.diffeqdict = diffeqdict
        self.StimulusParameter = StimulusParameter
        self.StimulusInstr = StimulusInstr
        self.n_TPs = n_TPs
        self.dt = dt
        
        self.UnpackStimulus()
        self.GenerateStimulus()
        self.GenerateValDict()
        self.EvenBetterReplace()
        self.RunSimulation()
        
    def UnpackStimulus(self):
        """
        Writes the individual items in stimulus instruction list as individual 
        variables, so the code is more readable.
        """
        self.Stimulus_base = self.StimulusInstr[0]
        self.Stimulus_strength = self.StimulusInstr[1]
        self.Stimulus_start = self.StimulusInstr[2]
        self.Stimulus_length = self.StimulusInstr[3]
        self.Stimulus_interpulse = self.StimulusInstr[4]
        self.Stimulus_repeats = self.StimulusInstr[5]
             
    def GenerateStimulus(self):
        """Generates the amount of EGF present at each timepoint.
        
        #Pulse_strength:float, Pulse_start:int, Pulse_length:int, 
            Interpulse:int, Repeats:int = 1
        Parameters:
            Pulse_strength:float - Amount of EGF
            Pulse_start:int - Timepoint at which pulse (train) starts
            Pulse_length:int - Duration of the pulse
            Interpulse:int - Time between pulses
            Repeats:int - Amount of repetition, must be >=1 for pulses.
        
        Returns:
            Stimulus:np.array - Amount of EGF at each TP."""
            
        Stimulus = self.Stimulus_base * np.ones(self.n_TPs+1)
        start=self.Stimulus_start
        for i in range(self.Stimulus_repeats):
            stop = start + self.Stimulus_length
            Stimulus[start:stop] = self.Stimulus_strength
            start+=(self.Stimulus_interpulse + self.Stimulus_length)
        self.Stimulus = {self.StimulusParameter: Stimulus}
        return {self.StimulusParameter: Stimulus}
    
    def GenerateValDict(self, tstart = 0):
        """
        Generates a dictionary to hold the values gained in the simulation.

        Parameters
        ----------
        tstart : float, optional
            Parameter in case simulation starts later. The default is 0.

        Returns
        -------
        valdict : dict
            Dictionary of time, tp, stimulus parameter and all values.

        """
        valdict = {"tp": [0],
               "t" : [tstart],
               self.StimulusParameter: [0]}
        for key in self.initdict.keys():
            valdict[key] = [self.initdict[key]]
        self.valdict = valdict
        return valdict
    
    def InsertVals(self):
        """
        Puts current values into the differential equations

        Returns
        -------
        subseqs : dict
            Substituted equations, where values are placed.

        """
        subseqs = {}
        for eqkey in self.diffeqdict.keys():
            eq = self.diffeqdict[eqkey]
            for valkey in self.valdict.keys():
                eq = eq.replace(valkey, str(self.valdict[valkey][-1]))
            subseqs[eqkey] = eq
        return subseqs

    # def BetterReplace(self):
    #     """
    #     Inserts values into equation.
    #     This function is deprecated, please use EvenBetterReplace for running
    #     the simulation as it is way more efficient.

    #     Returns
    #     -------
    #     subseqs : dict
    #         Dictionary of value name and equation, where values are placed.

    #     """
    #     subseqs = {}
    #     for eqkey in self.diffeqdict.keys():
    #         eq = self.diffeqdict[eqkey]
    #         for valkey in self.valdict.keys():
    #             value = self.valdict[valkey][-1]
    #             start = 0
    #             while start < len(eq):
    #                 pos = eq.find(valkey, start)
    #                 if pos < 0: break
    #                 start = pos
    #                 front, back = False, False
    #                 if any(symb in  eq[pos-1]  for symb in ["+", "-", "*", "/", "("]):
    #                     front = True
    #                 try:
    #                     if any(symb in  eq[pos+len(str(valkey))]  for symb in ["+", "-", "*", "/", ")"]):
    #                         back = True
    #                 except IndexError:
    #                     back = True
    #                 if front and back:
    #                     eq = self.ReplaceAtPos(eq, pos, valkey, str(value))
    #                     start+=len(str(value))
    #                 else: start += 1
    #         subseqs[eqkey] = eq
    #     return subseqs

    def ReplaceAtPos(self, string:str, pos:int, remove:str, insert:str):
        """
        Replaces characters at a defined position of a string
    
        Parameters
        ----------
        string : str
            Original string where things need to be replaced.
        pos : int
            Position where things will be inserted.
        remove : str-transformable
            What will be replaced
        insert : str-transformable
            What will be inserted.
    
        Returns
        -------
        str
            The original string with replacements.
    
        """
        if not string[pos:pos+len(str(remove))] == remove:
            raise ValueError("The given phrase to replace '" + str(remove) 
                             + "' was not found at position '" + str(pos) 
                             + "'. Instead '" + string[pos:pos+len(str(remove))] 
                             + "' was found.")
            
        return string[:pos] + str(insert) + string[pos+len(str(remove)):]

    # def EvaluateEQs(self):
    #     # subseqs = self.InsertVals()
    #     subseqs = self.BetterReplace()
    #     for key in subseqs.keys():
    #         self.valdict[key].append(self.valdict[key][-1]+self.dt*eval(subseqs[key]))
    #     self.valdict["tp"].append(self.valdict["tp"][-1] + 1)
    #     self.valdict["t"].append(self.valdict["t"][-1] + self.dt)
    #     # self.valdict = valdict
    #     # return valdict

    def EvenBetterReplace(self):
        subseqs = {}
        for eqkey in self.diffeqdict.keys():
            eq = self.diffeqdict[eqkey]
            for valkey in self.valdict.keys():
                value = "self.valdict['"+ valkey +"'][-1]"
                start = 0
                while start < len(eq):
                    pos = eq.find(valkey, start)
                    if pos < 0: break
                    start = pos
                    front, back = False, False
                    if any(symb in  eq[pos-1]  for symb in ["+", "-", "*", "/", "("]):
                        front = True
                    try:
                        if any(symb in  eq[pos+len(str(valkey))]  for symb in ["+", "-", "*", "/", ")"]):
                            back = True
                    except IndexError:
                        back = True
                    if front and back:
                        eq = self.ReplaceAtPos(eq, pos, valkey, str(value))
                        start+=len(str(value))
                    else: start += 1
            subseqs[eqkey] = eq
        self.subseqs = subseqs
        return subseqs

    def BetterEvaluateEQs(self):
        """
        Loops over the equations and solves them for the next time step.
        Results are saved in self.valdict.

        Returns
        -------
        None.

        """
        for key in self.subseqs.keys():
            self.valdict[key].append(self.valdict[key][-1]+self.dt*eval(self.subseqs[key]))
        self.valdict["tp"].append(self.valdict["tp"][-1] + 1)
        self.valdict["t"].append(self.valdict["t"][-1] + self.dt)
    
    def SingleStep(self):
        """
        Performs a single integration step and prints results.
        Needed that for testing.
        """
        
        for key in self.subseqs.keys():
            print(self.valdict[key][-1]+self.dt*eval(self.subseqs[key]))
    
    def RunSimulation(self):
        """
        Does the ODE solving in a loop until last TP is reached.
        Values are saved in the self.valdict dictionary.
        """
        while self.valdict["tp"][-1] < self.n_TPs:
            self.valdict[self.StimulusParameter][-1] = self.Stimulus[self.StimulusParameter][self.valdict["tp"][-1]]
            # self.EvaluateEQs()
            self.BetterEvaluateEQs()
            
    def PrintLast(self):
        """
        Prints the the values at the last timepoint. 
        Good for getting new initial values, e.g being closer to steady state.

        Returns
        -------
        string: str
            String of values at the last timepoint. Is also printed out.

        """
        string = "init "
        count = 0
        for key in self.valdict.keys():
            if key in ["tp", "t", self.StimulusParameter]: continue
            if not count == 0:
                string += ","
            string += (key + "=" + str(round(self.valdict[key][-1],3)))
            count += 1
        print(string)
        return string
            # print(key + " " +str(round(self.valdict[key][-1],3)))


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    diffeqdict = {'V': '(-0.1*mCa*(V-144.38)-1.92*1/(1+np.exp((-67.44-V)/-11.46))*(V--83.7)-12.62*mK*hK*(V--83.7)-0.1*(V--63.27)+Iapp)/0.049',
                  'mCa': '(1/(1+np.exp((-16.34-V)/1.84))-mCa)/6.64',
                  'mK': '(1/(1+np.exp((-3.31-V)/7.26))-mK)/0.082',
                  'hK': '(1/(1+np.exp((-65.4-V)/-29.5))-hK)/3.63'}

    initdict = {'V': -36.377, 'mCa': 0.36992, 'mK': 0.0, 'hK': 0.96281}
    
    StimulusInstr = [0,0,20,1000,200,3] #[98.01,110.5,20,1000,200,3]
    StimulusParameter = "Iapp"
    n_TPs = 10
    
    sim = SingleStepIntegrator(initdict, diffeqdict, StimulusParameter, StimulusInstr, n_TPs, dt = 0.01)
    plt.plot(sim.valdict["t"], sim.valdict["V"])
    