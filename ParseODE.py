# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 16:53:03 2022

@author: lott
GS d- s:+ a-- C++ t 5 X R tv b+ D+ G e+++ h r++ 
"""

# def readOdeParameters(path):
import os

if __name__ == "__main__":
    
    
    path = 'D:/SystemStimulator/models/AFD.ode'
    
    file = open(path, "r")
    flist = file.readlines()
    file.close()
    del file
    
    initdict = {}
    paramdict = {}
    equations = {}
    
    for line in flist:
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
        # Get the Equations ...
        if line.endswith("\n"): # remove "\n"
            line = line[:len(line)-1]
        line = line.replace(" ", "")
        if any(symb in line for symb in ["+", "*", "/"]):
            if line.startswith("#"): continue
            for param in paramdict.keys():
                start = 0
                print("param = " + str(param))

                while start < len(line):
                    # print("search start = " + str(start))
                    pos = line.find(param, start)
                    if pos == -1: break
                    start = pos
                    print("pos = " + str(pos))
                    front, back = False, False
                    if any(symb in  line[pos-1]  for symb in ["+", "-", "*", "/", "("]):
                        front = True
                    try:
                        if any(symb in  line[pos+len(param)]  for symb in ["+", "-", "*", "/", ")"]):
                            back = True
                    except IndexError:
                        back = True
                    print("front = " + str(front))
                    print("back = " + str(back))
                    if front and back:
                        line = line.replace(param, str(paramdict[param]))
                        
                    # print(line2)
                    start += len(param)
            print(line)
            equations.append(line)
    
    diffeqs = []
    auxeqs = {}
    for eq in equations:
        if eq.find("/dt") > 0:
            diffeqs.append(eq)
        else:
            auxvar, auxeq = eq.split("=")
            auxeqs[auxvar] = str(auxeq)
            
    if len(auxeqs) > 0:
        for i in range(len(diffeqs)):
            eq = diffeqs[i]
            if not any(aux in eq for aux in auxeqs.keys()): continue
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
                        eq = eq.replace(aux, auxeqs[aux])
                        diffeqs[i] = eq
                    start += (len(auxeqs[aux]) - len(aux))
        
    
    
    # if any(symb in line for symb in ["+", "*", "/"]):
    #     if line.startswith("#"): continue
    #     print(line)
        
    #     if any(symb in line for symb in paramdict.keys()): 
    #         for key in paramdict.keys():
    #             line = line.replace(key, str(paramdict[key]))
    #         print(line)
    
#%% Testing ground
if not __name__ == "__main__":
    line = "dmCa/dt = (mCainf(V)-mCa)/taumCa"
    line = line.replace(" ", "")
    
    start = 0
    param = "taumCa"
    # param = "mCa"
    while start < len(line):
        # print("search start = " + str(start))
        pos = line.find(param, start)
        start = pos
        # print("pos = " + str(pos))
        front, back = False, False
        if any(symb in  line[pos-1]  for symb in ["+", "-", "*", "/", "("]):
            front = True
        try:
            if any(symb in  line[pos+len(param)]  for symb in ["+", "-", "*", "/", ")"]):
                back = True
        except IndexError:
            back = True
        # print("front = " + str(front))
        # print("back = " + str(back))
        if front == True and back == True:
            line2 = line.replace(line[pos:pos+len(param)], str(paramdict[param]))
            
        print(line2)
        start += len(param)

    
