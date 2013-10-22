'''
Created on Sep 30, 2013

@author: wencan
'''
import fio

def getActList(test):
	dict = {}

	filename = "res/"+test+"_summary.txt"
	head, body = fio.readMatrix(filename, True)
	
	out_index = head.index('output acts')
	in_index = head.index('top slu')
	
	for row in body:
		out_act = row[out_index][1:-1]
		in_act = row[in_index][1:-1]
		
		acts = set( list(getAct(out_act)) + list(getAct(in_act)))
		
		for act in acts:
			if act not in dict:
				dict[act] = 0
			dict[act] = dict[act] + 1
	
	outfile = "res/"+test+".dict"
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
		
		actions[name] = value
	return actions

def getSluSlotValueDict(slu):#return to.desc=pitt
	tokens = slu.split('&')
	
	actions = {}
	for token in tokens:
		k = token.find('(')
		if k == -1: continue
		k2 = token.find(')')
		if k2 == -1: continue
		t2 = token[k+1:k2].split('=')
		if len(t2)!=2: continue
		name = t2[0]
		value= t2[1]
		
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
		
		actions[name] = value
	return actions

def getAct(slu):#parse the action from the slu string
	tokens = slu.split('&')
	
	actions = []
	for token in tokens:
		k = token.find('(')
		if k == -1: continue
		
		actions.append(token[:k])
	return set(actions)
	
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
			label = rank if rank <= 1 else -1
			
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
		fio.ArffWriter("res/"+test+".arff", header, types, "dstc", data)	
	
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
		
		rank_index = head.index('rank')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		asr_index = head.index('top asr')
		
		for row in body:
			rank = int( row[rank_index] )
			label = rank if rank <= 1 else -1
			
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
		fio.ArffWriter("res/"+test+"_actngram.arff", header, types, "dstc", data)

def IsRequestedSlot(out_act, in_act):
	act_out = getOutActDict(out_act)
	if 'request' in act_out:
		slot = act_out['request']
		act_in = getSluActDict(in_act)
		if slot in act_in:
			return True
	return False

def AddConfirmedSlot(confirmedslot, out_act, in_act):
	acts = getAct(in_act)
	
	if 'affirm' not in acts: return
	
	#extract the first expl-conf from out_act
	tokens = out_act.split('&')
	for token in tokens:
		k = token.find('(')
		if k == -1: continue
		name = token[:k]
		if name != 'expl-conf': continue
		
		k2 = token.find(')')
		if k2 == -1: continue
		t2 = token[k+1:k2].split('=')
		if len(t2)!=2: continue
		slotname = t2[0]
		value = t2[1]
		confirmedslot[slotname] = value #update the confirmed dict

def AddNegateSlot(negateslot, out_act, in_act):
	acts = getAct(in_act)
	
	if 'negate' not in acts: return
	
	#extract the first expl-conf from out_act
	tokens = out_act.split('&')
	for token in tokens:
		k = token.find('(')
		if k == -1: continue
		name = token[:k]
		if name != 'expl-conf': continue
		
		k2 = token.find(')')
		if k2 == -1: continue
		t2 = token[k+1:k2].split('=')
		if len(t2)!=2: continue
		slotname = t2[0]
		value = t2[1]
		negateslot[slotname] = value
			
def IsConfirmed(confirmedslot, in_act):
	if len(confirmedslot) == 0: return False
	
	dict = getSluSlotValueDict(in_act)
	
	for key, value in dict.items():
		if key in confirmedslot:
			if confirmedslot[key] == value:
				return True
	return False
	
def IsNegated(negateslot, in_act):
	return IsConfirmed(negateslot, in_act)

def IsGeneralNegated(confirmedslot, in_act):
	if len(confirmedslot) == 0: return False
	
	dict = getSluSlotValueDict(in_act)
	
	for key, value in dict.items():
		if key in confirmedslot:
			if confirmedslot[key] != value:
				return True
	return False
	
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
		
		sluscore_index = head.index('top slu score')
		restart_index = head.index('restart')
		
		input_start_index = head.index('intput_start_time')
		input_end_index = head.index('intput_end_time')
		output_start_index = head.index('output_start_time')
		output_end_index = head.index('output_end_time')
		
		confirmedslot = {}
		negateslot = {}
		
		for row in body:
			rank = int( row[rank_index] )
			label = rank if rank <= 1 else -1
			
			out_act = row[out_index][1:-1]
			in_act = row[in_index][1:-1]
			asr = row[asr_index][1:-1]
			turn_id = row[turn_index]
			
			acts = set( list(getAct(out_act)) + list(getAct(in_act)))
			
			#more feature
			wordcount = len(asr.split()) if len(asr) > 0 else 0
			
			sluscore = row[sluscore_index]
			slurank = 1
			
			restart = row[restart_index]
			if restart == 'True' or turn_id == '0':
				confirmedslot = {}
				negateslot = {}
			
			input_duration = float(row[input_end_index]) - float(row[input_start_index]) if row[input_end_index] != '-1' and row[input_start_index] != '-1' else -1
			output_duration = float(row[output_end_index]) - float(row[output_start_index]) if row[output_end_index] != '-1' and row[output_start_index] != '-1' else -1
			speaker_rate = input_duration/wordcount if input_duration != -1 and wordcount > 0 else -1
			
			isrequest = IsRequestedSlot(out_act, in_act)
			
			AddConfirmedSlot(confirmedslot, out_act, in_act)
			AddNegateSlot(negateslot, out_act, in_act)
			
			isconfirmed = IsConfirmed(confirmedslot, in_act)
			isnegated = IsNegated(negateslot, in_act)
			isgeneralNegated = IsGeneralNegated(confirmedslot, in_act)
			
			frow = []
			
			frow.append(asr)
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
			frow.append(isrequest)
			frow.append(isconfirmed)
			frow.append(isnegated)
			frow.append(isgeneralNegated)
			
			frow.append(label)
			data.append(frow)
		
		header =[]
		header.append("ASR")
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
			
		header = header + ['@@Class@@']
		
		types = []
		types.append("String")
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
		fio.ArffWriter("res/"+test+"_enrich.arff", header, types, "dstc", data)
				
if (__name__ == '__main__'):
	#getActList("train2")
	#getWekaARFF("train2", ["train2", "test1", "test2", "test3", "test4"])
	#getWekaARFF_Ngram(["train2", "test1", "test2", "test3", "test4"])
	getWekaARFF_Enrich("train2", ["train2", "test1", "test2", "test3", "test4"])
	#getWekaARFF_ActNgram
	print "Done"