## @package utility
# Package for basic operators
# @file utility.py
# @author Wencan Luo (wencan@cs.pitt.edu)
# @date 11/12/2013

def sub(X,Y):#x - y
	#assert(type(X) == type(Y))
	if type(X) == type([]):
		r = []
		for x in X:
			if x not in Y:
				r.append(x)
		return r
	
	if type(X) == type({}):
		r = {}
		for k,v in X.items():
			if k not in Y:
				r[k] = v
			else:
				if Y[k] != v:
					r[k] = v
		return r
	
	return X-Y

if (__name__ == '__main__'):
	print sub([1,2,3], [1,4])
	print sub({1:1, 2:2}, {1:1,3:3})