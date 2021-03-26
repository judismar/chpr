import random

class HashFunction:
	def __init__(self, m, p):
		self.m = m
		self.p = p
		self.a = random.randint(1, p-1)
		self.b = random.randint(1, p-1)
		self.c = random.randint(0, p-1)

	def __call__(self, x):
		return ((self.a*x**2 + self.b*x + self.c) % self.p) % self.m
