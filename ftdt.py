

def ftdt(L, C, RL, i0, v0, dz, dt, vph, R=0, G=0):
	v = v0
	i = i0

	kmax = len(i)

	d = dt / dz
	re = d / L
	rh = d / C

	while True:
		iprox = [0] + [i[k] - re*(v[k]-v[k-1]) for k in range(1,kmax)]

		# if RL == float("inf"):
		# 	iprox[0] = 0
		# elif RL == 0:
		# 	iprox[0] = iprox[1]

		vprox = [0] + [v[k] - rh * (iprox[k + 1] - iprox[k]) for k in range(1, kmax - 1)] + [0]
		
		#condições de contorno para V
		vprox[0] = v[1] + ((vph*dt - dz)/(vph*dt + dz))*(vprox[1] - v[0])
		vprox[-1] = v[-2] + ((vph*dt - dz)/(vph*dt + dz))*(vprox[-2] - v[0])

		#TODO: resolver para carga RL resistiva
		
		yield iprox, vprox

		v = vprox
		i = iprox

gen = (ftdt(1,1,0,[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,6],0.1,0.1,10))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
