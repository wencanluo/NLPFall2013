'''
Created on Sep 30, 2013

@author: wencan
'''
import fio

def getRankDistribution():
	tests = ["dstc2_train", "dstc2_dev"]
	
	total = []
	dicts = []
	for test in tests:
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		total.append(len(body))
		index = head.index('rank_H3')
		
		dict = {}
		
		for row in body:
			rank = row[index]
			if rank not in dict:
				dict[rank] = 0
			dict[rank] = dict[rank] + 1
		
		dicts.append(dict)
		#fio.PrintDict(dict)
		#print
	
	fio.PrintListwithName(tests, "data")
	fio.PrintListwithName(total, "total")
	
	for key in range(-1, 10):
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