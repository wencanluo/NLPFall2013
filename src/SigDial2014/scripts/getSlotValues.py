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
from SlotTracker import *

def getQuestionType():
	tests = ["dstc2_train", "dstc2_dev"]
	
	for test in tests:
		dict = {}
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		goal_index = head.index('recovery_goals')
		
		out_index = head.index('output acts')
		asr_index = head.index('top asr')
		in_trans_index = head.index('input trans')
		
		for i,row in enumerate(body):
			out_act = row[out_index][1:-1]
			acts = "_".join(sorted(set( list(getAct(out_act, "out_", True)))))
			asr = row[asr_index][1:-1]			
			trans = row[in_trans_index][1:-1]
			goals = row[goal_index][1:-1]
			goaldict = getGoalsDict(goals)
			
def getUnigramDict(file):
	head, body = fio.readMatrix(file, True)
	#index = head.index('goal_label')
	asr_index = head.index('top asr')
	
	dict = {}
	
	for row in body:
		asr = row[asr_index][1:-1]
		
		ws = asr.split()
		for w in ws:
			if w not in dict:
				dict[w] = 0
			dict[w] = dict[w] + 1
	
	fio.PrintDict(dict, True)
	
	return dict

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

def checkRequested():
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

def getARCombinationCount():
	tests = ["dstc2_train", "dstc2_dev"]
	
	for test in tests:
		dict = defaultdict(float)
		
		print test
		filename = "res/"+test+"_summary.txt"
		
		head, body = fio.readMatrix(filename, True)
		
		sr_id_index = head.index('sr_id')
		dm_id_index = head.index('dm_id')
		turn_index= head.index('turn_index')
		
		for i,row in enumerate(body):
			sr_id = 'SR'+row[sr_id_index]
			dm_id = 'DM'+row[dm_id_index]
			
			turn_id = row[turn_index]
				
			if turn_id == '0':	
				dict[sr_id+'.'+dm_id] = dict[sr_id+'.'+dm_id] + 1

		print dict['SR0.DM0'], "\t", dict['SR0.DM1']
		print dict['SR1.DM0'], "\t", dict['SR1.DM1']

def getPrior():
	#tests = ["dstc2_train", "dstc2_dev"]
	tests = ["dstc2_train"]
	
	goal_names = ['area', 'food', 'name', 'pricerange']
	
	dict = {}
	
	for goal in goal_names:
		for test in tests:
			filename = "res/"+test+"_summary.txt"
			
			head, body = fio.readMatrix(filename, True)
			
			out_index = head.index('output acts')
			goal_index = head.index('recovery_goals')
			
			for i,row in enumerate(body):
				goals = row[goal_index][1:-1]
				goaldict = SlotTracker.getGoalsDict(goals)
				
				label = ""
				if goal in goaldict:
					if goal == 'name' or goal == 'food':
						if goaldict[goal]=='dontcare':
							label = 'dontcare'
						else:
							label = 'Yes'
					else:
						label = goaldict[goal]
				else:
					label = 'No'
				
				if goal not in dict:
					dict[goal]=defaultdict(float)
					
				dict[goal][label] = dict[goal][label] + 1.0
	
	#normalized
	for goal in dict:
		x_items = dict[goal].items()
		total_p = sum([p for k,p in x_items])

		for k in dict[goal]:
			dict[goal][k] = dict[goal][k]/total_p
		
	return dict
					
if (__name__ == '__main__'):
	
	SavedStdOut = sys.stdout
	sys.stdout = open('res/slotdistribution.txt', 'w')
	
	getPrior()
	
	#getUnigramDict("res/dstc2_train_summary.txt")
	#getQuestionType()
	#getSlotValuesDistribution()
	#checkSlotOntology()
	#checkRequested()
	#getARCombinationCount()
	
	sys.stdout = SavedStdOut
	
	print "Done"
	