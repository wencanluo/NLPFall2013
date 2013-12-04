'''
Created on Sep 30, 2013

@author: wencan
'''
import fio
import Cosin
from SlotTracker import *
import getWekaArff
		
def getMulanARFF_ActNgram(featurefile, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+".dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		turn_index= head.index('turn_index')
		rank_index = head.index('rank')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		asr_index = head.index('top asr')
		
		goal_index = head.index('recovery_goals')
		
		#labels = ['area', 'food', 'name', 'pricerange', 'addr', 'phone', 'postcode', 'signature']
		goal_names = ['area', 'food', 'name', 'pricerange']
		
		for goal in goal_names:
			data = []
			
			for i,row in enumerate(body):
				turn_id = row[turn_index]
				
				out_act = row[out_index][1:-1]
				in_act = row[in_index][1:-1]
				asr = row[asr_index][1:-1]
				
				acts = set( list(getAct(out_act)) + list(getAct(in_act)))
				goals = row[goal_index][1:-1]
				
				goaldict = getGoalsDict(goals)
				
				row = []
				
				row.append(asr)
				
				for key in features.keys():
					if key in acts:
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
			
			header =[]
			header.append("ASR")
			for key in features.keys():
				header.append(key)
			#header = header + ['@@Class@@']
			goal = 'L' + goal
			
			header.append(goal)
			
			types = []
			types.append("String")
			for key in features.keys():
				types.append('Category')
			
			types = types + ['Category']
			
			#fio.MulanWriter("res/"+test+"_goals_actngram", goal_names, header, types, "dstc", data)
			fio.ArffWriter("res/"+test+"_goals_actngram_" + goal +".arff", header, types, "dstc", data)
			fio.writeMatrix("res/"+test+"_goals_actngram_" + goal +".matrix", data, header)

def getMulanARFF_ActWithNameNgram(featurefile, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+"_name.dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		turn_index= head.index('turn_index')
		rank_index = head.index('rank')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		asr_index = head.index('top asr')
		asr_score_index = head.index('asr_score')
		
		goal_index = head.index('recovery_goals')
		
		#labels = ['area', 'food', 'name', 'pricerange', 'addr', 'phone', 'postcode', 'signature']
		goal_names = ['area', 'food', 'name', 'pricerange']
		
		for goal in goal_names:
			data = []
			
			for i,row in enumerate(body):
				turn_id = row[turn_index]
				
				out_act = row[out_index][1:-1]
				in_act = row[in_index][1:-1]
				asr = row[asr_index][1:-1]
				asr_score = row[asr_score_index]
				
				acts = set( list(getAct(out_act, "out_", True)) + list(getAct(in_act, "in_", True)))
				goals = row[goal_index][1:-1]
				
				goaldict = getGoalsDict(goals)
				
				row = []
				
				row.append(asr)
				row.append(asr_score)
				
				for key in features.keys():
					if key in acts:
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
			
			header =[]
			header.append("ASR")
			header.append("ASR_Score")
			
			for key in features.keys():
				header.append(key)
			#header = header + ['@@Class@@']
			goal = 'L' + goal
			
			header.append(goal)
			
			types = []
			types.append("String")
			types.append("Continuous")
			
			for key in features.keys():
				types.append('Category')
			
			types = types + ['Category']
			
			#fio.MulanWriter("res/"+test+"_goals_actngram", goal_names, header, types, "dstc", data)
			fio.ArffWriter("res/"+test+"_goals_actWithNamengram_" + goal +".arff", header, types, "dstc", data)
			#fio.writeMatrix("res/"+test+"_goals_actWithNamengram_" + goal +".matrix", data, header)
	
def getMulanARFF_Enrich(featurefile, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+"_name.dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		turn_index= head.index('turn_index')
		rank_index = head.index('rank')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		asr_index = head.index('top asr')
		asr_score_index = head.index('asr_score')
		
		out_trans_index = head.index('output trans')
		in_trans_index = head.index('input trans')
		
		sluscore_index = head.index('top slu score')
		restart_index = head.index('aborted')
		
		input_start_index = head.index('intput_start_time')
		input_end_index = head.index('intput_end_time')
		output_start_index = head.index('output_start_time')
		output_end_index = head.index('output_end_time')
		
		goal_index = head.index('recovery_goals')
		
		#labels = ['area', 'food', 'name', 'pricerange', 'addr', 'phone', 'postcode', 'signature']
		goal_names = ['area', 'food', 'name', 'pricerange']
		
		for goal in goal_names:
			data = []
			
			for i,row in enumerate(body):
				turn_id = row[turn_index]
				
				out_act = row[out_index][1:-1]
				in_act = row[in_index][1:-1]
				#asr = row[asr_index][1:-1]
				asr = row[in_trans_index][1:-1]
				
				out_trans = row[out_trans_index]
			
				acts = set( list(getAct(out_act, "out_", True)) + list(getAct(in_act, "in_", True)))
				goals = row[goal_index][1:-1]
				
				goaldict = getGoalsDict(goals)
				
				restart = row[restart_index]
				asr_score = row[asr_score_index]
				cos = Cosin.compare(asr, out_trans)
				cos2 = Cosin.compare(asr, body[i-1][asr_index][1:-1]) if float(turn_id) > 0 and i > 0 else 0
				wordcount = len(asr.split()) if len(asr) > 0 else 0
				sluscore = row[sluscore_index]
				input_duration = float(row[input_end_index]) - float(row[input_start_index]) if row[input_end_index] != '-1' and row[input_start_index] != '-1' else -1
				output_duration = float(row[output_end_index]) - float(row[output_start_index]) if row[output_end_index] != '-1' and row[output_start_index] != '-1' else -1
				speaker_rate = input_duration/wordcount if input_duration != -1 and wordcount > 0 else -1
	
				row = []
				
				row.append(asr)
				
				row.append(asr_score)
				row.append(cos)
				row.append(cos2)
				row.append(wordcount)
				row.append(sluscore)
				row.append(restart)
				row.append(input_duration)
				row.append(output_duration)
				row.append(speaker_rate)
				
				for key in features.keys():
					if key in acts:
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
			
			header =[]
			header.append("ASR")
			header.append("ASR_Score")
			header.append("Cosin")
			header.append("Cosin2") #cosin between current input and previous input
			header.append('wordcount')
			header.append('sluscore')
			header.append('restartFlag')
			header.append('input_duration')
			header.append('output_duration')
			header.append('speaker_rate')
			
			for key in features.keys():
				header.append(key)
			#header = header + ['@@Class@@']
			goal = 'L' + goal
			
			header.append(goal)
			
			types = []
			types.append("String")

			types.append("Continuous")#ASR_Score
			types.append("Continuous")#Cosin
			types.append('Continuous')
			types.append('Continuous')#wordcount
			types.append('Continuous')#sluscore
			types.append('Category')#restartFlag
			types.append('Continuous')#input_duration
			types.append('Continuous')#output_duration
			types.append('Continuous')#speaker_rate
		
			for key in features.keys():
				types.append('Category')
				
			types = types + ['Category']
			
			#fio.MulanWriter("res/"+test+"_goals_actngram", goal_names, header, types, "dstc", data)
			fio.ArffWriter("res/"+test+"_goals_enrich_trans_" + goal +".arff", header, types, "dstc", data)
			#fio.writeMatrix("res/"+test+"_goals_actWithNamengram_" + goal +".matrix", data, header)
												
if (__name__ == '__main__'):
	#getMulanARFF_ActNgram("dstc2_train", ["dstc2_train", "dstc2_dev"])
	#getMulanARFF_ActWithNameNgram("dstc2_train", ["dstc2_train", "dstc2_dev"])
	getMulanARFF_Enrich("dstc2_train", ["dstc2_train", "dstc2_dev"])
	print "Done"