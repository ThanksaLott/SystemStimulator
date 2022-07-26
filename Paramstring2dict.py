# -*- coding: utf-8 -*-
"""
Created on Thu May 12 14:55:28 2022

@author: lott
GS d- s:+ a-- C++ t 5 X R tv b+ D+ G e+++ h r++ 
"""

def dictbuilder(splitparams):
    dicto = {}
    for line in splitparams:
        keyval = line.split("=")
        key = keyval[0][1:]
        val = keyval[1]
        dicto[key] = val
    return dicto

def printdict(dictt):
    stringo = ""
    for key in dictt.keys():
        stringo+=('"' + key + '" : ')
        stringo += (str(dictt[key]) + ",\n")
    return stringo

parametersstring = " gammaDNF=2.957, Rt=1, PDNFt = 1, alph1=0.0017, alph2=0.3, alph3=1.0, kR=0.8, k1=0.01, k2_1=0.5, bDNF=36.0558, kon=0.003, koff=0.01668"
split = parametersstring.split(",")

a = dictbuilder(split)
b = printdict(a)
print(b)