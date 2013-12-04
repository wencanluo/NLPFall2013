'''
Created on Sep 30, 2013

@author: wencan
'''
import fio
import Cosin
from SlotTracker import *
import dataset_walker
import getSummary

def getActList(tests, fout, withname = False):
	dict = {}

	for test in tests:
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		
		for row in body:
			out_act = row[out_index][1:-1]
			in_act = row[in_index][1:-1]
			
			#acts = set( list(getAct(out_act, "out_")) + list(getAct(in_act, "in_")))
			if not withname:
				acts = set( list(getAct(out_act)) + list(getAct(in_act)))
			else:
				acts = set( list(getAct(out_act, "out_", True)) + list(getAct(in_act, "in_", True)))
			
			for act in acts:
				if act not in dict:
					dict[act] = 0
				dict[act] = dict[act] + 1
	
	if not withname:
		outfile = "res/"+fout+".dict"
	else:
		outfile = "res/"+fout+"_name.dict"
	
	fio.SaveDict(dict, outfile)
	
def getOutActDict(slu):
	tokens = slu.split('&')
	
	actions = {}
	for token in tokens:
		k = token.find('(')
		if k == -1: continue
		name = token[:k]
		
		k2 = token.find(')')
		if k2 == -1: continue
		t2 = token[k+1:k2].split('=')
		if len(t2)!=2: continue
		value = t2[0]
		
		if name == "request":
			value = t2[1]
		
		actions[name] = value
	return actions

def getSluActDict(slu):#return to=pitt
	tokens = slu.split('&')
	
	actions = {}
	for token in tokens:
		k = token.find('(')
		if k == -1: continue
		k2 = token.find(')')
		if k2 == -1: continue
		t2 = token[k+1:k2].split('=')
		if len(t2)!=2: continue
		t3 = t2[0].split('.')
		name = t3[0]
		value=t2[1]
		
		if name == "request":
			value = t2[1]
			
		actions[name] = value
	return actions
	
def getWekaARFF_Act(featurefile, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+".dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		data = []
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		rank_index = head.index('rank')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		
		for row in body:
			rank = int( row[rank_index] )
			label = rank if rank == 0 else -1
			
			out_act = row[out_index][1:-1]
			in_act = row[in_index][1:-1]
			
			acts = set( list(getAct(out_act)) + list(getAct(in_act)))
			
			row = []
			
			for key in features.keys():
				if key in acts:
					row.append(1)
				else:
					row.append(0)
	
			row.append(label)
			data.append(row)
		
		header =[]
		for key in features.keys():
			header.append(key)
		header = header + ['@@Class@@']
		
		types = [] 
		for key in features.keys():
			types.append('Category')
		types = types + ['Category']
		fio.ArffWriter("res/"+test+"_act.arff", header, types, "dstc", data)	
		fio.writeMatrix('res/' + test + "_act.body", data, header)

def getWekaARFF_ActWithName(featurefile, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+"_name.dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		data = []
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		rank_index = head.index('rank')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		
		for row in body:
			rank = int( row[rank_index] )
			label = rank if rank == 0 else -1
			
			out_act = row[out_index][1:-1]
			in_act = row[in_index][1:-1]
			
			acts = set( list(getAct(out_act, "out_", True)) + list(getAct(in_act, "in_", True)))
			
			row = []
			
			for key in features.keys():
				if key in acts:
					row.append(1)
				else:
					row.append(0)
	
			row.append(label)
			data.append(row)
		
		header =[]
		for key in features.keys():
			header.append(key)
		header = header + ['@@Class@@']
		
		types = [] 
		for key in features.keys():
			types.append('Category')
		types = types + ['Category']
		fio.ArffWriter("res/"+test+"_actwithname.arff", header, types, "dstc", data)	
		fio.writeMatrix('res/' + test + "_act.body", data, header)
	
def getWekaARFF_Ngram(tests):
	for test in tests:
		data = []
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		rank_index = head.index('rank')
		asr_index = head.index('top asr')
		
		for row in body:
			rank = int( row[rank_index] )
			label = rank if rank <= 1 else -1
			
			asr = row[asr_index][1:-1]
			
			row = []
			
			row.append(asr)
			row.append(label)
			data.append(row)
		
		header =[]
		header.append("ASR")
		header = header + ['@@Class@@']
		
		types = [] 
		types.append("String")
		types.append('Category')
		
		fio.ArffWriter("res/"+test+"_ngram.arff", header, types, "dstc", data)	
		
def getWekaARFF_ActNgram(featurefile, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+".dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		data = []
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)		
		
		#rank_index = head.index('rank')
		#rank_index = head.index('rank_H2')
		rank_index = head.index('rank_H3')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		asr_index = head.index('top asr')
		
		for row in body:
			rank = int( row[rank_index] )
			label = rank if rank <= 0 else -1
			
			out_act = row[out_index][1:-1]
			in_act = row[in_index][1:-1]
			asr = row[asr_index][1:-1]
			
			acts = set( list(getAct(out_act)) + list(getAct(in_act)))
			
			row = []
			
			row.append(asr)
			
			for key in features.keys():
				if key in acts:
					row.append(1)
				else:
					row.append(0)
	
			row.append(label)
			data.append(row)
		
		header =[]
		header.append("ASR")
		for key in features.keys():
			header.append(key)
		header = header + ['@@Class@@']
		
		types = []
		types.append("String")
		for key in features.keys():
			types.append('Category')
		types = types + ['Category']
		#fio.ArffWriter("res/"+test+"_H2_actngram.arff", header, types, "dstc", data)
		#fio.ArffWriter("res/"+test+"_actngram.arff", header, types, "dstc", data)
		fio.ArffWriter("res/"+test+"_H3_actngram.arff", header, types, "dstc", data)
		
def getWekaARFFBinarySwitch_ActNgram(featurefile, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+".dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		data = []
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		sessions = dataset_walker.dataset_walker(test, dataroot='../data', labels=True)
		log_turns, label_turns = getSummary.getTurns(sessions)
		
		print len(log_turns)
		assert(len(log_turns) == len(body))
		
		rank_index = head.index('rank')
		#rank_index = head.index('rank_H2')
		#rank_index = head.index('rank_H3')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		asr_index = head.index('top asr')
		
		for i, row in enumerate(body):
			#rank = int( row[rank_index] )
			out_act = row[out_index][1:-1]
			asr = row[asr_index][1:-1]
			
			log_turn = log_turns[i]
			label_turn = label_turns[i]
			
			#in_act = row[in_index][1:-1]
			
			for k, hyps in enumerate(log_turn['input']['live']['slu-hyps']):
				#only keep top 3
				#if k >= 3: continue
				
				#get whether it is correct for each SLU
				label = 1 if getSummary.IsCorrectSLUHypRank_H1(hyps, label_turn) else 0
			
				#get acts for each input SLU
				in_act = getSummary.strslu(hyps['slu-hyp'])
					
				acts = set( list(getAct(out_act)) + list(getAct(in_act)))
				
				row = []
				
				row.append(asr)
				
				for key in features.keys():
					if key in acts:
						row.append(1)
					else:
						row.append(0)
		
				row.append(label)
				data.append(row)
		
		header =[]
		header.append("ASR")
		for key in features.keys():
			header.append(key)
		header = header + ['@@Class@@']
		
		types = []
		types.append("String")
		for key in features.keys():
			types.append('Category')
		types = types + ['Category']
		#fio.ArffWriter("res/"+test+"_H2_actngram.arff", header, types, "dstc", data)
		#fio.ArffWriter("res/"+test+"_actngram.arff", header, types, "dstc", data)
		fio.ArffWriter("res/"+test+"_H1_actngram_binaryswitch_top3_10.arff", header, types, "dstc", data)
			
def getWekaARFFBinarySwitch_ActNgramWithName(featurefile, tests):
	#Feature Set: Act with Name, System out, User Slot in
	
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+"_name.dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		data = []
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		sessions = dataset_walker.dataset_walker(test, dataroot='../data', labels=True)
		log_turns, label_turns = getSummary.getTurns(sessions)
		
		print len(log_turns)
		assert(len(log_turns) == len(body))
		
		rank_index = head.index('rank')
		#rank_index = head.index('rank_H2')
		#rank_index = head.index('rank_H3')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		asr_index = head.index('top asr')
		systemout_index = head.index('output trans')
		for i, row in enumerate(body):
			#rank = int( row[rank_index] )
			out_act = row[out_index][1:-1]
			asr = row[asr_index][1:-1]
			
			Trans_System = row[systemout_index][1:-1]
			
			log_turn = log_turns[i]
			label_turn = label_turns[i]
			
			#in_act = row[in_index][1:-1]
			
			for k, hyps in enumerate(log_turn['input']['live']['slu-hyps']):
				#if k >= 3: continue
				
				#get whether it is correct for each SLU
				label = 1 if getSummary.IsCorrectSLUHypRank_H1(hyps, label_turn) else 0
			
				#get acts for each input SLU
				in_act = getSummary.strslu(hyps['slu-hyp'])
				
				Trans_SLU = getSummary.getActText(in_act)
				
				acts = set( list(getAct(out_act, "out_", True)) + list(getAct(in_act, "in_", True)))
				
				row = []
				
				#row.append(asr)
				row.append(Trans_System)
				row.append(Trans_SLU)
				
				for key in features.keys():
					if key in acts:
						row.append(1)
					else:
						row.append(0)
		
				row.append(label)
				data.append(row)
		
		header =[]
		header.append("Trans_System")
		header.append("Trans_SLU")
		for key in features.keys():
			header.append(key)
		header = header + ['@@Class@@']
		
		types = []
		types.append("String")
		types.append("String")
		for key in features.keys():
			types.append('Category')
		types = types + ['Category']
		#fio.ArffWriter("res/"+test+"_H2_actngram.arff", header, types, "dstc", data)
		#fio.ArffWriter("res/"+test+"_actngram.arff", header, types, "dstc", data)
		fio.ArffWriter("res/"+test+"_H1_actngram_binaryswitchwithName.arff", header, types, "dstc", data)

def getWekaARFFBinarySwitch_ActWithName(featurefile, tests):
	#Feature Set: Act with Name, System out, User Slot in
	
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+"_name.dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		data = []
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		sessions = dataset_walker.dataset_walker(test, dataroot='../data', labels=True)
		log_turns, label_turns = getSummary.getTurns(sessions)
		
		print len(log_turns)
		assert(len(log_turns) == len(body))
		
		rank_index = head.index('rank')
		#rank_index = head.index('rank_H2')
		#rank_index = head.index('rank_H3')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		asr_index = head.index('top asr')
		systemout_index = head.index('output trans')
		for i, row in enumerate(body):
			#rank = int( row[rank_index] )
			out_act = row[out_index][1:-1]
			asr = row[asr_index][1:-1]
			
			Trans_System = row[systemout_index][1:-1]
			
			log_turn = log_turns[i]
			label_turn = label_turns[i]
			
			#in_act = row[in_index][1:-1]
			
			for k, hyps in enumerate(log_turn['input']['live']['slu-hyps']):
				#get whether it is correct for each SLU
				label = 1 if getSummary.IsCorrectSLUHypRank_H1(hyps, label_turn) else 0
			
				#get acts for each input SLU
				in_act = getSummary.strslu(hyps['slu-hyp'])
				
				Trans_SLU = getSummary.getActText(in_act)
				
				acts = set( list(getAct(out_act, "out_", True)) + list(getAct(in_act, "in_", True)))
				
				row = []
				
				#row.append(asr)
				#row.append(Trans_System)
				#row.append(Trans_SLU)
				
				for key in features.keys():
					if key in acts:
						row.append(1)
					else:
						row.append(0)
		
				row.append(label)
				data.append(row)
		
		header =[]
		#header.append("Trans_System")
		#header.append("Trans_SLU")
		for key in features.keys():
			header.append(key)
		header = header + ['@@Class@@']
		
		types = []
		#types.append("String")
		#types.append("String")
		for key in features.keys():
			types.append('Category')
		types = types + ['Category']
		#fio.ArffWriter("res/"+test+"_H2_actngram.arff", header, types, "dstc", data)
		#fio.ArffWriter("res/"+test+"_actngram.arff", header, types, "dstc", data)
		fio.ArffWriter("res/"+test+"_H1_actWithName_binaryswitch.arff", header, types, "dstc", data)
					
def getWekaARFF_Enrich(featurefile, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+".dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		data = []
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		turn_index = head.index('turn_index')
		rank_index = head.index('rank')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		
		asr_index = head.index('top asr')
		asr_score_index = head.index('asr_score')
		
		out_trans_index = head.index('output trans')
		
		sluscore_index = head.index('top slu score')
		restart_index = head.index('restart')
		
		input_start_index = head.index('intput_start_time')
		input_end_index = head.index('intput_end_time')
		output_start_index = head.index('output_start_time')
		output_end_index = head.index('output_end_time')
		
		confirmedslot = {}
		negateslot = {}
		
		for rid, row in enumerate(body):
			rank = int( row[rank_index] )
			label = rank if rank <= 1 else -1
			
			out_act = row[out_index][1:-1]
			in_act = row[in_index][1:-1]
			asr = row[asr_index][1:-1]
			asr_score = row[asr_score_index]
			
			out_trans = row[out_trans_index]
			
			cos = Cosin.compare(asr, out_trans)
			
			turn_id = row[turn_index]
			cos2 = Cosin.compare(asr, body[rid-1][asr_index][1:-1]) if float(turn_id) > 0 and rid > 0 else 0
			
			acts = set( list(getAct(out_act)) + list(getAct(in_act)))
			
			#more feature
			wordcount = len(asr.split()) if len(asr) > 0 else 0
			
			sluscore = row[sluscore_index]
			slurank = 1
			
			restart = row[restart_index]
			if restart == 'True' or turn_id == '0':
				confirmedslot = {}
				negateslot = {}
				tracker = CSlotTracker()
			
			input_duration = float(row[input_end_index]) - float(row[input_start_index]) if row[input_end_index] != '-1' and row[input_start_index] != '-1' else -1
			output_duration = float(row[output_end_index]) - float(row[output_start_index]) if row[output_end_index] != '-1' and row[output_start_index] != '-1' else -1
			speaker_rate = input_duration/wordcount if input_duration != -1 and wordcount > 0 else -1
			
			tracker.addInform(in_act, float(sluscore))
			tracker.addAffirm(out_act, in_act, float(sluscore))
			tracker.addNegate(out_act, in_act, float(sluscore))
			
			bins = tracker.getBins(out_act, in_act)
			
			#maxScore = tracker.getMax()
			acc = tracker.getAcc(out_act, in_act)
			
			frow = []
			
			frow.append(asr)
			frow.append(asr_score)
			frow.append(cos)
			frow.append(cos2)
			for key in features.keys():
				if key in acts:
					frow.append(1)
				else:
					frow.append(0)
			#Add feature here
			frow.append(wordcount)
			frow.append(sluscore)
			frow.append(slurank)
			frow.append(restart)
			frow.append(input_duration)
			frow.append(output_duration)
			frow.append(speaker_rate)
			
			#frow.append(maxScore)
			frow.append(acc)
			frow = frow + bins
			
			frow.append(label)
			data.append(frow)
		
		header =[]
		header.append("ASR")
		header.append("ASR_Score")
		header.append("Cosin")
		header.append("Cosin2") #cosin between current input and previous input
		
		for key in features.keys():
			header.append(key)
			
		header.append('wordcount')
		header.append('sluscore')
		header.append('slurank')
		header.append('restartFlag')
		header.append('input_duration')
		header.append('output_duration')
		header.append('speaker_rate')
		header.append('isrequest')
		header.append('isconfirmed')
		header.append('isnegated')
		header.append('isgeneralNegated')
		header.append('isconfirmedOut')
		header.append('isnegatedOut')
		header.append('isgeneralNegatedOut')
		
		#header.append('MaxScore')
		header.append('Acc')
		
		for i in range(10):
			header.append("InformBin" + str(i))
		for i in range(10):
			header.append("AffirmBin" + str(i))
		for i in range(10):
			header.append("NegateBin" + str(i))
		for i in range(10):
			header.append("MaxBin" + str(i))
			
		header = header + ['@@Class@@']
		
		types = []
		types.append("String")
		types.append("Continuous")
		types.append("Continuous")
		types.append("Continuous")
		for key in features.keys():
			types.append('Category')
		
		types.append('Continuous')
		types.append('Continuous')
		types.append('Continuous')
		types.append('Category')
		types.append('Continuous')
		types.append('Continuous')
		types.append('Continuous')
		types.append('Category')
		types.append('Category')
		types.append('Category')
		types.append('Category')
		
		types.append('Category')
		types.append('Category')
		types.append('Category')
		
		#types.append('Continuous') #maxScore
		types.append('Continuous') #Acc
		
		for i in range(40): #bins
			types.append('Continuous')
			
		types.append('Category') #Label
		
		#fio.ArffWriter("res/"+test+"_enrich.arff", header, types, "dstc", data)
		fio.ArffWriter("res/"+test+"_"+featurefile+"_enrich.arff", header, types, "dstc", data)
		#fio.writeMatrix('res/' + test + "_enrich.body", data, header)
				
def getWekaARFF_Bin(featurefile, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+".dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		data = []
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		turn_index = head.index('turn_index')
		rank_index = head.index('rank')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		
		asr_index = head.index('top asr')
		asr_score_index = head.index('asr_score')
		
		out_trans_index = head.index('output trans')
		
		sluscore_index = head.index('top slu score')
		restart_index = head.index('restart')
		
		input_start_index = head.index('intput_start_time')
		input_end_index = head.index('intput_end_time')
		output_start_index = head.index('output_start_time')
		output_end_index = head.index('output_end_time')
		
		confirmedslot = {}
		negateslot = {}
		
		for rid, row in enumerate(body):
			rank = int( row[rank_index] )
			label = rank if rank <= 1 else -1
			
			out_act = row[out_index][1:-1]
			in_act = row[in_index][1:-1]
			asr = row[asr_index][1:-1]
			asr_score = row[asr_score_index]
			
			out_trans = row[out_trans_index]
			
			cos = Cosin.compare(asr, out_trans)
			
			turn_id = row[turn_index]
			cos2 = Cosin.compare(asr, body[rid-1][asr_index][1:-1]) if float(turn_id) > 0 and rid > 0 else 0
			
			acts = set( list(getAct(out_act)) + list(getAct(in_act)))
			
			#more feature
			wordcount = len(asr.split()) if len(asr) > 0 else 0
			
			sluscore = row[sluscore_index]
			slurank = 1
			
			restart = row[restart_index]
			if restart == 'True' or turn_id == '0':
				confirmedslot = {}
				negateslot = {}
				tracker = CSlotTracker()
			
			input_duration = float(row[input_end_index]) - float(row[input_start_index]) if row[input_end_index] != '-1' and row[input_start_index] != '-1' else -1
			output_duration = float(row[output_end_index]) - float(row[output_start_index]) if row[output_end_index] != '-1' and row[output_start_index] != '-1' else -1
			speaker_rate = input_duration/wordcount if input_duration != -1 and wordcount > 0 else -1
			
			tracker.addInform(in_act, float(sluscore))
			tracker.addAffirm(out_act, in_act, float(sluscore))
			tracker.addNegate(out_act, in_act, float(sluscore))
			
			bins = tracker.getBins(out_act, in_act)
			
			#maxScore = tracker.getMax()
			acc = tracker.getAcc(out_act, in_act)
			
			frow = []
			
			frow.append(acc)
			frow = frow + bins
			
			frow.append(label)
			data.append(frow)
		
		header =[]
		header.append('Acc')
		
		for i in range(10):
			header.append("InformBin" + str(i))
		for i in range(10):
			header.append("AffirmBin" + str(i))
		for i in range(10):
			header.append("NegateBin" + str(i))
		for i in range(10):
			header.append("MaxBin" + str(i))
			
		header = header + ['@@Class@@']
		
		types = []
		types.append('Continuous') #Acc
		
		for i in range(40): #bins
			types.append('Continuous')
			
		types.append('Category') #Label
		
		fio.ArffWriter("res/"+test+"_"+featurefile+"_bins.arff", header, types, "dstc", data)
		#fio.writeMatrix('res/' + test + "_"+featurefile"_bins.body", data, header)
		
if (__name__ == '__main__'):
	#getActList(["dstc2_train"], "dstc2_train", True)
	#getWekaARFF_ActNgramWithName("dstc2_train", ["dstc2_train", "dstc2_dev"])
	#getWekaARFF_ActNgram("dstc2_train", ["dstc2_train", "dstc2_dev"])
	#getWekaARFFBinarySwitch_ActNgram("dstc2_train", ["dstc2_train", "dstc2_dev"])
	getWekaARFFBinarySwitch_ActNgramWithName("dstc2_train", ["dstc2_train", "dstc2_dev"])
	#getWekaARFFBinarySwitch_ActWithName("dstc2_train", ["dstc2_train", "dstc2_dev"])
	#getWekaARFF_ActWithName("dstc2_train", ["dstc2_train", "dstc2_dev"])
	print "Done"