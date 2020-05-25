import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import math
import sys

def fdtd(L, C, RL, kmax, dz, dt, vph, vfonte, rfonte, R=0, G=0, n0=0):

	v = [0 for x in range(0, kmax)]
	i = [0 for x in range(0, kmax)]

	d = dt / dz
	re = d / L
	rh = d / C

	n = n0
	while True:
		iprox = [0] + [i[k] - re * (v[k] - v[k - 1]) for k in range(1, kmax)]

		vprox = [0] + [v[k] - rh * (iprox[k + 1] - iprox[k]) for k in range(1, kmax - 1)] + [0]
		
		#fonte
		iprox[1] = vfonte(n * dt) / rfonte
		vprox[1] = vfonte(n * dt)

		#condições de contorno para V
		vprox[0] = v[1] + ((vph*dt - dz)/(vph*dt + dz))*(vprox[1] - v[0])
		vprox[-1] = v[-2] + ((vph*dt - dz)/(vph*dt + dz))*(vprox[-2] - v[-1])

		if RL == 0:
			vprox[-2] = 0
		elif RL != math.inf:
			vprox[-2] = RL*iprox[-2]

		if RL == math.inf:
			iprox[-2] = 0

		yield iprox, vprox

		v = vprox
		i = iprox
		n = n + 1

if (len(sys.argv) < 3):
	print("Falta parametros")
	exit()

def fonte(t): return 0
if sys.argv[1] == 'pulso':
	fonte = lambda t: 1 if t < 10 / 2.69e8 and t > 0 else 0
elif sys.argv[1] == 'constante':
	fonte = lambda t: 2

RL = float(sys.argv[2])

dt = 1.6e-9
gen = (fdtd(1.853e-7, 7.41e-11, RL, 100, 1, dt, 2.69e8, fonte, 75))

data = [{'z': k, 't': t, 'v': v} for t in range(0,math.ceil(100*10/2.69e8/dt)) for k, v in enumerate(next(gen)[1])]


fig = px.line(pd.DataFrame(data=data), x='z', y='v', animation_frame='t', range_y=[-4,4])

#fig = go.Figure(frames=[go.Frame(data=[go.Line(x=[0,1,2,3,4,5,6,7,8], y=next(gen)[1] )]) for t in range(0,200)])
fig.show()
