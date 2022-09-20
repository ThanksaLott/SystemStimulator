# SystemStimulator

SystemStimulator is a small tool I am writing to aid in working with time varying signals in ordinary differential equation systems. It is able to read xpp-style .ode files into python and evaluate the equations over a given range of timepoints. On top of this, individual parameters can be varied for specific time points (eg. pulses of stimuli). The results of the simulation can then be plot as a time-series or a phase-space trajectory. 

At the current time, the tool is still quite limited to trains of pulses. I will try my best to flush it out in the future.