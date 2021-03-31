import math
import random
import sys
import time
from cuckoo_hashing_perfect_rehash import CuckooHashingPerfectRehash

#Average number of insertions a perfect rehash is required after one was performed.

random.seed()
N = 200

def sim(outputfile, rehashAll):
	n = 500
	output = "x = 500:500:25000\ny = ["
	U = list(range(1, 10**7))
	for _ in range(50):
		S = random.sample(U, n)
		chpr = CuckooHashingPerfectRehash(n, 0.5, 3*math.log(n, 2), 10**7)
		for key in S:
			chpr.insert(key, True) #Here, we want all functions to change if a rehash is necessary, before the experiment begins.
		l = []
		for __ in range(N):
			chpr.numRehashes = 0
			cont = 0
			while chpr.numRehashes < 2:
				if chpr.numRehashes >= 1:
					cont += 1
				chpr.removeRandom()
				newInsertion = False
				while not newInsertion:
					x = random.randint(1, 10**7)
					newInsertion = chpr.insert(x, rehashAll)
			l.append(cont)
		output += str(mean(l)) + " "
		print(n)
		n += 500
		f = open(outputfile, "w")
		f.write(output)
		f.close()
	output += "]\nplot(x, y)"
	f = open(outputfile, "w")
	f.write(output)
	f.close()

def mean(numlist):
	sumvar = 0
	for num in numlist:
		sumvar += num
	return float(sumvar)/float(len(numlist))

sim("/home/judismar/Área de Trabalho/out", False)
sim("/home/judismar/Área de Trabalho/out-2", True)
