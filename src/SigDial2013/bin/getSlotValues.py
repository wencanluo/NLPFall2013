'''
Created on Sep 30, 2013

@author: wencan
'''
import fio
import sys

def getSlotDict(file):
	head, body = fio.readMatrix(file, True)
	index = head.index('CorrectLabel')
	
	dict = {}
	
	for row in body:
		slotvalue = row[index]
		slotvalue = slotvalue[1:-1]
		if slotvalue == '': continue
		
		tokens = slotvalue.split(";")
		for token in tokens:
			sv = token.split("=")
			slot = sv[0]
			value = sv[1]
			
			if slot not in dict:
				dict[slot] = {}
			if value not in dict[slot]:
				dict[slot][value] = 0
			dict[slot][value] = dict[slot][value] + 1
		
	return dict

def getSlotValuesDistribution():
	tests = ['test1', 'test2', 'test3', 'test4', 'train1a', 'train2', 'train3']
	
	dicts = []
	for test in tests:
		filename = "res/"+test+"_summary.txt"
		dict = getSlotDict(filename)
		
		dicts.append(dict)
	
	
	keys = []
	
	for dict in dicts:
		keys = keys + dict.keys()
	
	keys = sorted(set(keys))
	
	for key in keys:
		print key,
		
		values = []
		for dict in dicts:
			if key in dict:
				values = values + dict[key].keys()
		values = sorted(set(values))
		
		for value in values:
			print "\t", value,"\t",
			
			for dict in dicts:
				if key in dict and value in dict[key]:
					print dict[key][value], "\t", 
				else:
					print 0, "\t",
			print
		print
		
if (__name__ == '__main__'):
	
	SavedStdOut = sys.stdout
	sys.stdout = open('log.txt', 'w')
	
	getSlotValuesDistribution()
	
	sys.stdout = SavedStdOut
	
	print "Done"
	