class DeterministicPerfectHashFunction: 
	def __init__(self, keys, u):
		self.q = self.findq(keys, u)

	def __call__(self, x):
		return x % self.q

	def findq(self, keys, u):
		n = len(keys)
		q = n-1
		collided = True
		while collided: #at most n^2 log u loops guarantee
			q += 1
			collided = False
			l = [None]*q
			aux = None
			for x in keys:
				aux = l[x % q]
				if aux != None: #collision
					collided = True
					break
				l[x % q] = x
		return q
