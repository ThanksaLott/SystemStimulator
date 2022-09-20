# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 16:53:03 2022

@author: lott
GS d- s:+ a-- C++ t 5 X R tv b+ D+ G e+++ h r++ 
"""


import os
import numpy as np

class ParseODE():
    def __init__(self, path, StimulusParameter, check = True):
        self.path = path
        self.StimulusParameter = StimulusParameter
        self.check = check
        self.numpyfunctdict = {
                "exp(" : "np.exp(",
                "cos(" : "np.cos(",
                "arccos(" : "np.arccos(",
                "sin(" : "np.sin(",
                "arcsin(" : "np.arcsin(",
                "tan(" : "np.tan(",
                "arctan(" : "np.arctan(",
                }
        
        # Run the Parsing
        
        file = open(self.path, "r")
        flist = file.readlines()
        file.close()
        del file
        
        initdict = {}
        paramdict = {}
        equations = {}
        
        # Gather given initial values and parameters
        for line in flist:
            if line.startswith("#"): continue
            if line.startswith("@"): continue
            if line.startswith("init"): # Get the inits
                line = line[5:] # remove "init " 
                if line.endswith("\n"): # and remove "\n"
                    line = line[:len(line)-1]
                inits = line.split(",")
                for i in inits:
                    ini, val = i.split("=")
                    ini = ini.strip()
                    val = float(val.strip())
                    
                    initdict[ini] = val
                    
            if line.startswith("param"): # Get the params
                line = line[6:] # remove "param " 
                if line.endswith("\n"): # and remove "\n"
                    line = line[:len(line)-1]
                params = line.split(",")
                for i in params:
                    param, val = i.split("=")
                    param = param.strip()
                    val = float(val.strip())
                    
                    paramdict[param] = val
                    
                
        #  Second loop to make sure I got all the parameters
        equations = []
        for line in flist:
            if line.startswith("#"): continue
            if line.startswith("@"): continue
            if line.startswith("param"): continue
            if line.startswith("init"): continue
            # Get the Equations ...
            if line.endswith("\n"): # remove "\n"
                line = line[:len(line)-1]
            line = line.replace(" ", "")
            if any(symb in line for symb in ["+", "*", "/", "-"]):
                equations.append(line)
        
        diffeqs = []
        auxeqs = {}
        for eq in equations:
            if eq.find("/dt") > 0:
                diffeqs.append(eq)
            else:
                auxvar, auxeq = eq.split("=")
                auxeqs[auxvar] = str(auxeq)
        if check:
            inp = self.VerifyCompilationWithUser(diffeqs, auxeqs, paramdict, initdict)
        else:
            inp = True
        
        if inp:
            self.diffeqs = diffeqs
            self.auxeqs = auxeqs
            self.initdict = initdict
            self.paramdict = paramdict
            self.diffeqdict = self.FinalizeDiffEqs(diffeqs, paramdict, auxeqs)
    
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
    
    def MergeDictionary(a:dict, b:dict):
        c = a.copy()
        c.update(b)
        return c
    
    def ReplaceByDictionary(self, string:str, dictionary:dict):
        """
        Replaces things in a string according to a dictionary.
    
        Parameters
        ----------
        string : str
            A string where things will be substituted.
        dictionary : dict
            Dictionary of what will be substituted with what. Keys -> Values.
    
        Returns
        -------
        string : str
            The modified string.
    
        """
        string = string.replace(" ", "")
        keys = dictionary.keys()
        if not any(thing in string for thing in keys):
            return string
        for thing in keys:
            start = 0
            while start < len(string):
                pos = string.find(thing, start)
                if pos < 0: break
                start = pos
                string = self.ReplaceAtPos(string, pos, thing, dictionary[thing])
                start+=len(dictionary[thing])
        return string
    
    def PutAuxeqsInDiffeqs(self, diffeqs, auxeqs:dict):
        """
        Inserts auxiliary equations into the differential equations
    
        Parameters
        ----------
        diffeqs : list
            List of the differential equations found in the .ode.
        auxeqs : dict
            dictionary of auxiliary equations.
    
        Returns
        -------
        substeqs : list
            List of the differntial equations, where auxiliary equations and proper
            numpy functions are inserted
    
        """
        
        if not len(auxeqs) > 0:
            return diffeqs
        
        substeqs = []
        for eq in diffeqs:
            if not any(aux in eq for aux in auxeqs.keys()): 
                substeqs.append(eq)
                continue
            for aux in auxeqs.keys():
                start = 0
                while start < len(eq):
                    pos = eq.find(aux, start)
                    if pos == -1: break
                    start = pos
                    front, back = False, False
                    if any(symb in  eq[pos-1]  for symb in ["+", "-", "*", "/", "("]):
                        front = True
                    try:
                        if any(symb in  eq[pos+len(aux)]  for symb in ["+", "-", "*", "/", ")"]):
                            back = True
                    except IndexError:
                        back = True
                    if front and back:
                        eq = eq.replace(aux, "(" + auxeqs[aux] + ")") # Make sure there are brackets
                        start += (len(auxeqs[aux]) - len(aux))
                    else:
                        start += 1
            
            substeqs.append(self.ReplaceByDictionary(eq, self.numpyfunctdict))
        return substeqs
            
    
    def PutParamsInDiffeqs(self, diffeqs, paramdict:dict):
        """
        Inserts values of parameters into the differential equations
    
        Parameters
        ----------
        diffeqs : list
            List of the differential equations found in the .ode.
        paramdict : dict
            Dictionary of parameters and their values.
    
        Returns
        -------
        substeqs : list
            List of the differntial equations, where parameters are substituted for
            their values.
            
        """
        
        substeqs = []
        for eq in diffeqs:
            
            for param in paramdict.keys():
                if param == self.StimulusParameter:
                    continue
                start = 0
                while start < len(eq):
                    # print("search start = " + str(start))
                    pos = eq.find(param, start)
                    if pos == -1: break
                    start = pos
                    front, back = False, False
                    if eq[pos-1] in ["+", "-", "*", "/", "(", "="]:
                        front = True
                    try:
                        if eq[pos+len(param)] in ["+", "-", "*", "/", ")"]:
                            back = True
                    except IndexError: # occurs when pos is last char in eq
                        back = True
                    if front and back:
                        eq = self.ReplaceAtPos(eq, pos, param, paramdict[param])
                    start += len(param)
            substeqs.append(eq)
        
        return substeqs
        
    
    def VerifyCompilationWithUser(self, diffeqs, auxeqs, paramdict, initdict):
        print("I found the following differential equations:")
        for eq in diffeqs:
            print(eq)
        print("\nWith these additional equations:")
        for eq in auxeqs:
            print(eq + "=" + auxeqs[eq])
        print("\nAnd this set of parameters:")
        for param in paramdict:
            print(param + "=" + str(paramdict[param]))
        print("\nI also found this set of initial values:")
        for init in initdict:
            print(init + "=" + str(initdict[init]))
        
        while True:
            inp = input("\nDo you want to run with this? (y)es/(n)o: ")
            if inp in ["y", "yes"]:
                inp = True
                break
            elif inp in ["n", "no"]:
                inp = False
                break
            else:
                print("Only yes or no are accepted.")
                continue
        
        return inp
        
    def FinalizeDiffEqs(self, diffeqs, paramdict, auxeqs):
        diffeqs = self.PutAuxeqsInDiffeqs(diffeqs, auxeqs)
        diffeqs = self.PutParamsInDiffeqs(diffeqs, paramdict)
        
        diffeqdict = {}
        for eq in diffeqs:
            what, evalme = eq.split("=")
            diffeqdict[what.split("/dt")[0][1:]] = evalme
        
        return diffeqdict

            
    

#%% main
if __name__ == "__main__":
    
    path = 'D:/SystemStimulator/models/AFD.ode'
    StimulusParameter = "Iapp"
    
    parsed = ParseODE(path, StimulusParameter)


    
#%% Testing ground
# if not __name__ == "__main__":
#     print("fin")

    
