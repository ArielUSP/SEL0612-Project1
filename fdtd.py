import plotly.express as px
import plotly.graph_objs as go
import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
plt.style.use('seaborn-pastel')

#*-----------------------*
#| Source types:         |
#| 1. 2u(t)              | 
#| 2. u(t)-u(t - l/10uf) |
#*-----------------------*

#*-----------------------*
#| Load types:           |
#| 1. Short Circuit      | 
#| 2. Open Circuit       |
#| 3. Resistive Load     |
#*-----------------------*

SourceType = 1
LoadType = 2

tstart = 4 #start source at
tstop = 10000 #stop source at
kmax = 200 #max spa
Nmax = 2200 #max time interations
pi = math.pi

L = 1.853133862211956e-07 #indutance
C = 7.412535448847824e-11 #capacitance
load_resist = 75 #ohms
v_fase = 1/math.sqrt(L*C) #phase speed
line_size = 20 #meters

delz = line_size/kmax #space-step
delt = (0.5*delz)/v_fase # time-step with stability condition

K1 = (delt/(C*delz))
K2 = (delt/(L*delz))

V = [[0.0 for k in range(kmax+1)] for n in range(Nmax+1)]
I = [[0.0 for k in range(kmax+1)] for n in range(Nmax+1)]

for n in range(1,Nmax):
	#now we iterate over all k values
	for k in range(1, kmax):
		I[n][k+1] = I[n-1][k+1] - K2*(V[n-1][k+1]-V[n-1][k])
		if(k == 2): #source is added here
			if(SourceType == 1):
				I[n][k+1] = I[n][k+1] + (2 if n >= tstart else 0)
			if(SourceType == 2):
				I[n][k+1] = I[n][k+1] + (1 if n >= tstart else 0) - (1 if n >= (tstart + (line_size/(10*v_fase))) else 0)
	if(LoadType == 2): #to implement an open circuit
		I[n][kmax-1] = 0
	for k in range(1,kmax-1):
		V[n][k] = V[n-1][k] - K1*(I[n][k + 1] - I[n][k])
		if(k == 2): #source is added here
			if(SourceType == 1):
				V[n][k] = V[n][k] + load_resist*(2 if n >= tstart else 0)
			if(SourceType == 2):
				V[n][k] = V[n][k] + load_resist*((1 if n >= tstart else 0) - (1 if n >= (tstart + (line_size/(10*v_fase))) else 0))

	#push boundary conditions
	V[n][kmax] = V[n-1][kmax-1] + ((v_fase*delt - delz)/(v_fase*delt + delz)*(V[n][kmax-1]-V[n-1][kmax]))
	V[n][1] = V[n-1][2] + ((v_fase*delt - delz)/(v_fase*delt + delz)*(V[n][2]-V[n-1][1]))
	if(LoadType == 1):
		V[n][kmax-1] = 0
	if(LoadType == 2):
		V[n][kmax-1] = 75*I[n][kmax-1]
	#faz alguma coisa com essa nova geracao

data = [{'z': k, 't': n, 'v': V[n][k], 'i':I[n][k]} for n in range(Nmax) for k in range(kmax)]
fig = px.line(pd.DataFrame(data=data), x='z', y='v', animation_frame='t', range_y=[-4, 4])
fig2 = px.line(pd.DataFrame(data=data), x='z', y='i', animation_frame='t', range_y=[-4, 4])
fig.show()
fig2.show()
