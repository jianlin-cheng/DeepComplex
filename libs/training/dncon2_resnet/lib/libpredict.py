#!/usr/bin/python
# Badri Adhikari, 6-15-2017
# Subroutines for prediction

from libcommon import * 

def get_x_from_this_file(feature_file):
	L = 0
	with open(feature_file) as f:
		for line in f:
			if line.startswith('#'):
				continue
			L = line.strip().split()
			L = int(round(math.exp(float(L[0]))))
			break
	x = getX(feature_file, L)
	F = len(x[0, 0, :])
	X = np.zeros((1, L, L, F))
	X[0, :, :, :] = x
	return X

def prediction2rr(P, fileRR):
	print 'Writing RR file ' + fileRR
	L  = int(math.sqrt(len(P)))
	PM = P.reshape(L, L)
	rr = open(fileRR, 'w')
	for i in range(0, L):
		for j in range(i, L):
			if abs(i - j) < 1:
				continue
			rr.write("%i %i 0 8 %.5f\n" %(i+1, j+1, PM[i][j]))
	rr.close()

def make_ensemble_prediction(weight_arch_dict, X):
	N = len(X[:, 0, 0, 0])
	L = len(X[0, :, 0, 0])
	P = np.zeros((N, int(L * L)))
	for weight in weight_arch_dict.keys():
		print ''
		print 'Running prediction using ' + weight + ' and ' + weight_arch_dict[weight]
		P0 = make_prediction(read_model_arch(weight_arch_dict[weight]), weight, X)
		for i in range (0, len(P0[:, 0])):
			P[i] = P[i] + P0[i]
	for i in range (0, len(P[:, 0])):
		P[i] = P[i] / len(weight_arch_dict)
	return P

