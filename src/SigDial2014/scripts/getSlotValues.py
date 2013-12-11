'''
Created on Sep 30, 2013

@author: wencan
'''
import fio
import sys, json
import getWekaArff
import getSummary
import SlotTracker
from collections import defaultdict
import getWekaGoalsArff

def getSlotDict(file):
	head, body = fio.readMatrix(file, True)
	#index = head.index('goal_label')
	index = head.index('goal_label')
	
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
	tests = ["dstc2_train", "dstc2_dev"]
	
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

def checkSlotOntology():
	ontology = json.load(open('config/ontology_dstc2.json'))
	tests = ["dstc2_train", "dstc2_dev"]
	
	ontology = ontology['informable']
	
	dicts = []
	for test in tests:
		filename = "res/"+test+"_summary.txt"
		dict = getSlotDict(filename)
		
		dicts.append(dict) 
	
	for dict in dicts:
		for key, d in dict.items():
			if key in ontology:
				for k in d:
					if k not in ontology[key]:
						print key, k			

def checkRuquested():
	tests = ["dstc2_train", "dstc2_dev"]
	
	goal_names = ['area', 'food', 'name', 'pricerange']
	
	dict = defaultdict(float)
	
	for goal in goal_names:
		print goal
		for test in tests:
			print test
			filename = "res/"+test+"_summary.txt"
			
			head, body = fio.readMatrix(filename, True)
			
			out_index = head.index('output acts')
			goal_index = head.index('recovery_goals')
			
			for i,row in enumerate(body):
				out_act = row[out_index][1:-1]
				
				goals = row[goal_index][1:-1]
				goaldict = SlotTracker.getGoalsDict(goals)
				
				isRequestedGoal = getWekaGoalsArff.IsRequestedSlotGoals(out_act, goal_names)
				
				if goal in isRequestedGoal:
					if goal in goals:
						dict['Yes.Yes'] = dict['Yes.Yes'] + 1
					else:
						dict['Yes.No'] = dict['Yes.No'] + 1
				else:
					if goal in goals:
						dict['No.Yes'] = dict['No.Yes'] + 1
					else:
						dict['No.No'] = dict['No.No'] + 1
		
			
			print dict['Yes.Yes'], "\t", dict['Yes.No']
			print dict['No.Yes'], "\t", dict['No.No']
		
					
if (__name__ == '__main__'):
	
	SavedStdOut = sys.stdout
	sys.stdout = open('log.txt', 'w')
	
	#getSlotValuesDistribution()
	#checkSlotOntology()
	checkRuquested()
	
	sys.stdout = SavedStdOut
	
	print "Done"
	