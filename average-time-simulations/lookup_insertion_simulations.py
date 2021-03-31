import math
import random
import sys
import time
from cuckoo_hashing_perfect_rehash import CuckooHashingPerfectRehash

#The average time of a lookup and an insertion are in function of x = log log n, where n is the number of elements in the structure.

random.seed()
N_INSERT = 100
N_LOOKUP = 10000

def exp(strout):
	x = 2
	output = "x = 2:0.2:4.4\nplot(x, ["
	temp = "["
	U = list(range(1, 10000000))
	for _ in range(13):
		insertSample = []
		print(x)
		n = int(2**2**x)
		lookup = True
		for _ in range(N_INSERT):
			S = random.sample(U, n)
			ch = CuckooHashingPerfectRehash(n, 0.2, int(10*math.log(n, 2)), 10000000)
			begin = time.time_ns()
			for key in S:
				ch.insert(key)
			end = time.time_ns()
			insertSample.append(end-begin)
			if lookup:
				lookup = False
				begin = time.time_ns()
				for _ in range(N_LOOKUP):
					ch.lookup(random.choice(U))
				end = time.time_ns()
				temp += str((end-begin)/N_LOOKUP) + " "
		output = output + str(mean(insertSample)/n) + " "
		x += 0.2
		f = open(strout, "w")
		f.write(output + "], x, " + temp + "])")
		f.close()
	temp += "]"
	output += "], x, " + temp + ")"
	f = open(strout, "w")
	f.write(output)
	f.close()

def mean(numlist):
	sumvar = 0
	for num in numlist:
		sumvar += num
	return float(sumvar)/float(len(numlist))

exp("simulation_results/average-insertion-time.txt")
