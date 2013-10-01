'''
Created on Sep 30, 2013

@author: wencan
'''
import fio

def getRankDistribution():
	tests = ['test1', 'test2', 'test3', 'test4', 'train1a', 'train2', 'train3']
	
	dicts = []
	for test in tests:
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		index = head.index('rank')
		
		dict = {}
		
		for row in body:
			rank = row[index]
			if rank not in dict:
				dict[rank] = 0
			dict[rank] = dict[rank] + 1
		
		dicts.append(dict)
		#fio.PrintDict(dict)
		#print
		
	for key in range(-1, 100):
		key = str(key)
		print key, "\t",
		for dict in dicts:
			if key not in dict:
				print 0, "\t", 
			else:
				print dict[key], "\t", 
		print	
	
if (__name__ == '__main__'):
	getRankDistribution()