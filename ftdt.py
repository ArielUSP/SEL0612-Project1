

def ftdt(R, G, L, C, RL, v0, i0, dz, dt, nmax):
	v = v0
	i = i0

	kmax = len(i)

	c1 = 2 * dt / (dt * dz * R + 2 * dz * L)
	c2 = (2 * L - dt * R) / (2 * L + dt * R)
	c3 = -(2 * dt) / (dt * dz * G + 2 * dz * C)
	c4 = (2 * C - dt * G) / (2 * C + dt * G)
	
	n = 0

	while n < nmax:
		n = n+1
		iprox = [c1 * (v[k + 1] - v[k - 1]) + c2 * i[k] for k in range(1, kmax - 1)]

		if RL == float("inf"):
			iprox = [0] + iprox
		elif RL == 0:
			iprox = [iprox[0]] + iprox

		vprox = [c3 * (iprox[k + 1] - iprox[k]) + c4 * v[k + 1] for k in range(0, kmax)]

		#TODO: resolver para carga RL resistiva
		
		yield i, v

gen = (ftdt(0,1,1,0,0,[0,0,0,0,12],[0,0,0,0,0],0.1,0.1,10))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
