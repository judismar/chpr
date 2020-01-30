import math
import random
from bad_hash_function import HashFunction
from monte_carlo_perfect_hashing import ModifiedPerfectHashFunction
from deterministic_perfect_hashing import DeterministicPerfectHashFunction

class CuckooHashingPerfectRehash:
	def __init__(self, n, epsilon, maxmoves, u):
		self.d = int(math.log(math.log(n, 2), 2)) + 3 #The number of tables.
		self.m = int((1 + epsilon)*n/self.d) + 1 #The size of each table.
		self.maxmoves = maxmoves
		self.u = u
		self.T = [None]*self.d
		self.h = [None]*self.d
		self.hPerfect = [None]*self.d
		self.numberKeys = [0]*self.d #Number of keys in each table.
		for i in range(self.d):
			self.h[i] = HashFunction(self.m, 10000019)
			self.hPerfect[i] = HashFunction(self.m, 10000019) #Arbitrary function.
			self.T[i] = [None]*self.m
		self.emptySlotedTables = list(range(self.d)) #Keeps the index of subtables with empty slots to perform perfect rehash on.	

	def lookup(self, x):
		for i in range(self.d):
			if self.T[i][self.h[i](x)] == x or self.T[i][self.hPerfect[i](x)] == x:
				return True
		return False

	def insert(self, x):
		if self.lookup(x):
			return
		moves = 0
		while moves < self.maxmoves:
			k = 0
			aux = self.T[k][self.h[k](x)]
			self.T[k][self.h[k](x)] = x
			x = aux
			if x == None: #Sucessful.
				self.numberKeys[k] += 1
				if self.numberKeys[k] == self.m:
					self.emptySlotedTables.remove(k)
				return
			moves += 1
		self.perfectRehash(x)

	def perfectRehash(self, key):
		k = 0
		self.h[k] = HashFunction(self.m, 10000019) #Change the k-th function to generate new underlying augmenting paths.
		aux = [key]
		for x in self.T[k]:
			if x != None:
				aux.append(x)
		h = ModifiedPerfectHashFunction(2, 10000019)
		sucessful = h.mapping(10*len(aux)^2, aux, self.m - len(aux)) #10x^3 iterations, x = len(aux); x is at most m.
		if sucessful:
			self.T[k] = [None]*self.m
			self.hPerfect[k] = h
		else:
			h = DeterministicPerfectHashFunction(aux, self.u)
			if h.q >= self.m:
				self.T[k] = [None]*h.q
			else:
				self.T[k] = [None]*self.m
			self.hPerfect[k] = h
		for x in aux:
			self.T[k][self.hPerfect[k](x)] = x
		self.numberKeys[k] += 1
		if self.numberKeys[k] == self.m:
			self.emptySlotedTables.remove(k)
