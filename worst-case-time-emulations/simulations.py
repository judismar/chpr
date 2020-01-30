import math
import random
import sys
import time
from cuckoo_hashing_perfect_rehash import CuckooHashingPerfectRehash

random.seed()
N_INSERT = 5
N_LOOKUP = 1000

def exp(strout):
	n = 100
	output = "x = 100:100:25000\nplot(x, ["
	temp = "["
	U = list(range(1, 1000000))
	for _ in range(250):
		insertSample = []
		print(n)
		lookup = True
		for _ in range(N_INSERT):
			ch = CuckooHashingPerfectRehash(n, 0.2, int(10*math.log(n, 2)), 1000000)
			ch.T[0] = random.sample(U, ch.m)
			key = ch.T[0][1]
			ch.T[0][1] = None #A full table with an empty slot.
			begin = time.time_ns()
			ch.insert(key)
			end = time.time_ns()
			insertSample.append(end-begin)
			if lookup:
				lookup = False
				begin = time.time_ns()
				for _ in range(N_LOOKUP):
					ch.lookup(0)
				end = time.time_ns()
				temp += str((end-begin)/N_LOOKUP) + " "
		output = output + str(mean(insertSample)) + " "
		n += 100
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

exp("simulation_results/worst-case-insertion-time.txt")
