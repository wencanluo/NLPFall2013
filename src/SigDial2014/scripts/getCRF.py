'''
Created on Sep 30, 2013

@author: wencan
'''
import fio
from getWekaArff import *
	
def getCRF_Act(featurefile, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+"_name.dict")
	
	for test in tests:
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		turn_index = head.index('turn_index')
		rank_index = head.index('rank')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		goal_index = head.index('recovery_goals')
		goal_names = ['area', 'pricerange']
		
		for goal in goal_names:
			data = []
			
			for row in body:
				rank = int( row[rank_index] )
				label = rank if rank <= 1 else -1
				
				turn_id = row[turn_index]
				out_act = row[out_index][1:-1]
				in_act = row[in_index][1:-1]
				
				acts = set( list(getAct(out_act, "out_", True)) + list(getAct(in_act, "in_", True)))
				goals = row[goal_index][1:-1]
				
				if turn_id == '0':#add a blank line
					row = []
					data.append(row)

				goaldict = getGoalsDict(goals)
				
				row = []
				
				for key in features.keys():
					if key in acts:
						row.append(1)
					else:
						row.append(0)
		
				#row.append(label)
				if goal in goaldict:
					if goal == 'name' or goal == 'food':
						if goaldict[goal]=='dontcare':
							row.append(goal + '.Yes.dontcare')
						else:
							row.append(goal + '.Yes')
					else:
						row.append(goal + '.Yes.'+goaldict[goal])
				else:
					row.append(goal + '.No')
					
				data.append(row)
			
			data = data[1:]
			fio.CRFWriter("res/"+test +"_"+goal +".crf", data)

def getCRF_ActNgram(acts, unigrams, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+acts+"_name.dict")
	unigram = [' ' + word.strip() + ' ' for word in fio.readfile('res/' + unigrams + ".dict")]
	
	goal_names = ['area', 'pricerange']
	
	for test in tests:
		for goal in goal_names:
			data = []

			filename = "res/"+test+"_summary.txt"
			head, body = fio.readMatrix(filename, True)
			
			turn_index = head.index('turn_index')
			rank_index = head.index('rank')
			out_index = head.index('output acts')
			in_index = head.index('top slu')
			asr_index = head.index('top asr')
			goal_index = head.index('recovery_goals')
			
			for row in body:
				rank = int( row[rank_index] )
				label = rank if rank <= 1 else -1
				
				turn_id = row[turn_index]
				out_act = row[out_index][1:-1]
				in_act = row[in_index][1:-1]
				asr = row[asr_index][1:-1]
				
				acts = set( list(getAct(out_act, "out_", True)) + list(getAct(in_act, "in_", True)))
				goals = row[goal_index][1:-1]
				goaldict = getGoalsDict(goals)
				
				if turn_id == '0':#add a blank line
					row = []
					data.append(row)
	
				row = []
				
				for key in features.keys():
					if key in acts:
						row.append(1)
					else:
						row.append(0)
				
				asr = ' ' + asr + ' '
				for word in unigram:
					if asr.find(word) != -1:
						row.append(1)
					else:
						row.append(0)
		
				if goal in goaldict:
					if goal == 'name' or goal == 'food':
						if goaldict[goal]=='dontcare':
							row.append(goal + '.Yes.dontcare')
						else:
							row.append(goal + '.Yes')
					else:
						row.append(goal + '.Yes.'+goaldict[goal])
				else:
					row.append(goal + '.No')
					
				data.append(row)
			
			data = data[1:]
			fio.CRFWriter("res/"+test +"_"+goal +".crf", data)
			print len(row)
			
def getCRF_Label(tests):
	goal_names = ['area', 'pricerange']
	for test in tests:
		for goal in goal_names:
			out = "res/"+test+"_"+goal+".out"
			header, body = fio.CRFReader(out)
			fio.writeMatrix("res/"+test+"_"+goal+"_crf.label", body, header)
	
if (__name__ == '__main__'):
	#getCRF_Act("dstc2_train", ["dstc2_train", "dstc2_dev"])
	#getCRF_ActNgram("dstc2_train", 'unigram', ["dstc2_train", "dstc2_dev"])
	#getWekaARFF_Enrich("train2", ["train2", "test1", "test2", "test3", "test4"])
	getCRF_Label(["dstc2_train", "dstc2_dev"])
	#getCRF_Label(["test1_actngram", "test2_actngram", "test3_actngram", "test4_actngram"])
	print "Done"