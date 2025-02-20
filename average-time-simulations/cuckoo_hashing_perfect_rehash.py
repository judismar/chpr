import math
import random
from universal_hash_family import HashFunction
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
		self.numRehashes = 0
		self.numberKeys = [0]*self.d #Number of keys in each table.
		for i in range(self.d):
			self.h[i] = HashFunction(self.m, 10000019)
			self.hPerfect[i] = HashFunction(self.m, 10000019) #Arbitrary function: this list be useful only when a perfect hash function is built.
			self.T[i] = [None]*self.m
		self.emptySlotedTables = list(range(self.d)) #Keeps the index of subtables with empty slots to perform perfect rehash on.	

	def lookup(self, x):
		for i in range(self.d):
			if self.T[i][self.h[i](x)] == x or self.T[i][self.hPerfect[i](x)] == x:
				return True
		return False

	def insert(self, x, rehashAll = False):
		if self.lookup(x):
			return False
		moves = 0
		while moves < self.maxmoves:
			k = random.choice(list(range(self.d)))
			aux = self.T[k][self.h[k](x)]
			self.T[k][self.h[k](x)] = x
			x = aux
			if x == None: #Sucessful.
				self.numberKeys[k] += 1
				if self.numberKeys[k] == self.m:
					self.emptySlotedTables.remove(k)
				return True
			moves += 1
		self.perfectRehash(x, rehashAll)
		return True

	def removeRandom(self):
		k = random.randint(0, self.d-1)
		l = random.randint(0, self.m-1)
		while self.T[k][l] == None:
			k = random.randint(0, self.d-1)
			l = random.randint(0, self.m-1)
		self.T[k][l] = None
		self.numberKeys[k] -= 1
		if self.numberKeys[k] == self.m - 1:
			self.emptySlotedTables.append(k)

	def perfectRehash(self, key, rehashAll):
		self.numRehashes += 1
		if not rehashAll: #Perfect rehash on a single table
			k = random.choice(self.emptySlotedTables)
			self.h[k] = HashFunction(self.m, 10000019) #Change the k-th function to generate new underlying augmenting paths.
			aux = [key]
			for x in self.T[k]:
				if x != None:
					aux.append(x)
			h = ModifiedPerfectHashFunction(2, 10000019)
			sucessful = h.mapping(10*len(aux)^2, aux, self.m - len(aux)) #10x^2 iterations, x = len(aux); x is at most m.
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
		else: #Rehash all tables, used in experiments
			keyStored = False
			for k in range(self.d):
				self.h[k] = HashFunction(self.m, 10000019) #Change all functions to generate new underlying augmenting paths.
				if self.numberKeys[k] > 0 or not keyStored:
					aux = []
					if not keyStored and self.numberKeys[k] < self.m:
						self.numberKeys[k] += 1
						if self.numberKeys[k] == self.m:
							self.emptySlotedTables.remove(k)
						aux.append(key)
						keyStored = True
					for x in self.T[k]:
						if x != None:
							aux.append(x)
					h = ModifiedPerfectHashFunction(2, 10000019)
					sucessful = h.mapping(10*len(aux)^2, aux, self.m - len(aux)) #10x^2 iterations, x = len(aux); x is at most m.
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

	def printf(self):
		for i in range(self.d):
			print(i, self.T[i])
