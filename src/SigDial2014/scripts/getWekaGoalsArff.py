'''
Created on Sep 30, 2013

@author: wencan
'''
import fio
import Cosin
from SlotTracker import *
import getWekaArff
import json

ontology = json.load(open('config/ontology_dstc2.json'))
foodnamelist = [
            "afghan", 
            "african", 
            "afternoon tea", 
            "asian oriental", 
            "australasian", 
            "australian", 
            "austrian", 
            "barbeque", 
            "basque", 
            "belgian", 
            "bistro", 
            "brazilian", 
            "british", 
            "canapes", 
            "cantonese", 
            "caribbean", 
            "catalan", 
            "chinese", 
            "christmas", 
            "corsica", 
            "creative", 
            "crossover", 
            "cuban", 
            "danish", 
            "eastern european", 
            "english", 
            "eritrean", 
            "european", 
            "french", 
            "fusion", 
            "gastropub", 
            "german", 
            "greek", 
            "halal", 
            "hungarian", 
            "indian", 
            "indonesian", 
            "international", 
            "irish", 
            "italian", 
            "jamaican", 
            "japanese", 
            "korean", 
            "kosher", 
            "latin american", 
            "lebanese", 
            "light bites", 
            "malaysian", 
            "mediterranean", 
            "mexican", 
            "middle eastern", 
            "modern american", 
            "modern eclectic", 
            "modern european", 
            "modern global", 
            "molecular gastronomy", 
            "moroccan", 
            "new zealand", 
            "north african", 
            "north american", 
            "north indian", 
            "northern european", 
            "panasian", 
            "persian", 
            "polish", 
            "polynesian", 
            "portuguese", 
            "romanian", 
            "russian", 
            "scandinavian", 
            "scottish", 
            "seafood", 
            "singaporean", 
            "south african", 
            "south indian", 
            "spanish", 
            "sri lankan", 
            "steakhouse", 
            "swedish", 
            "swiss", 
            "thai", 
            "the americas", 
            "traditional", 
            "turkish", 
            "tuscan", 
            "unusual", 
            "vegetarian", 
            "venetian", 
            "vietnamese", 
            "welsh", 
            "world"
        ]
foodnames = {}
#for food in ontology['informable']['food']:
for food in foodnamelist:
	foodnames[' '+food+' '] = len(food.split())

foodnames = sorted(foodnames, key = foodnames.get, reverse = True)
		
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

def IsRequestedSlot(out_act, in_act):
	act_out = getWekaArff.getOutActDict(out_act)
	if 'request' in act_out:
		slot = act_out['request']
		act_in = getWekaArff.getSluActDict(in_act)
		if slot in act_in:
			return True
	return False


def AddConfirmedSlot(confirmedslot, out_act, in_act):
	acts = getAct(in_act)
	
	if 'affirm' not in acts: return
	
	#extract the first expl-conf from out_act
	dict = getOutActExplConfDict(out_act)
	
	for key,value in dict.items():
		confirmedslot[key] = value

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
	
	if len(dict) == 0: return False
	
	for key, value in dict.items():
		if key not in confirmedslot: return False
		if confirmedslot[key] != value: return False
	return True

def IsConfirmedOut(confirmedslot, out_act):
	if len(confirmedslot) == 0: return False
	
	dict = getOutActExplConfDict(out_act)
	if len(dict) == 0: return False
	
	for key, value in dict.items():
		if key not in confirmedslot: return False
		if confirmedslot[key] != value: return False
	return True
	
def IsNegated(negateslot, in_act):
	if len(negateslot) == 0: return False
	
	dict = getSluSlotValueDict(in_act)
	
	for key, value in dict.items():
		if key not in negateslot: continue
		if negateslot[key] == value: return True
	return False

def IsNegatedOut(negateslot, out_act):
	if len(negateslot) == 0: return False
	
	dict = getOutActExplConfDict(out_act)
	
	for key, value in dict.items():
		if key not in negateslot: continue
		if negateslot[key] == value: return True
	return False

def IsGeneralNegated(confirmedslot, in_act):
	if len(confirmedslot) == 0: return False
	
	dict = getSluSlotValueDict(in_act)
	
	for key, value in dict.items():
		if key in confirmedslot:
			if confirmedslot[key] != value:
				return True
	return False

def IsGeneralNegatedOut(confirmedslot, out_act):
	if len(confirmedslot) == 0: return False
	
	dict = getOutActExplConfDict(out_act)
	
	for key, value in dict.items():
		if key in confirmedslot:
			if confirmedslot[key] != value:
				return True
	return False

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

def IsRequestedSlotGoals(out_act, goal_names):
	act_out = getWekaArff.getOutActDict(out_act)
	
	goals = {}
	for goal in goal_names:
		if 'request' in act_out:
			slot = act_out['request']
			goals[slot] = True
			
	return goals
	
def getMulanARFF_Enrich(featurefile, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+"_name.dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		#labels = ['area', 'food', 'name', 'pricerange', 'addr', 'phone', 'postcode', 'signature']
		goal_names = ['area', 'food', 'name', 'pricerange']
		
		for goal in goal_names:
			
			predictions = []
			for method in ['baseline_focus', 'HWUbaseline','nbest_goals']:
				file = 'res/'+method+'_'+test+'_track.json.'+goal+'.label'
				head, body = fio.readMatrix(file, True)
				predictions.append([row[1] for row in body])
			
			filename = "res/"+test+"_summary.txt"
			head, body = fio.readMatrix(filename, True)
			
			sr_id_index = head.index('sr_id')
			dm_id_index = head.index('dm_id')
			
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
		
			data = []
			
			confirmedslot = {}
			negateslot = {}
		
			for i,row in enumerate(body):
				turn_id = row[turn_index]
				
				sr_id = row[sr_id_index]
				dm_id = row[dm_id_index]
			
				if turn_id == '0':
					confirmedslot = {}
					negateslot = {}

				out_act = row[out_index][1:-1]
				in_act = row[in_index][1:-1]
				asr = row[asr_index][1:-1]
				#asr = row[in_trans_index][1:-1]
				
				out_trans = row[out_trans_index]
			
				acts = set( list(getAct(out_act, "out_", True)) + list(getAct(in_act, "in_", True)))
				goals = row[goal_index][1:-1]
				
				goaldict = getGoalsDict(goals)
				
				restart = row[restart_index]
				asr_score = math.exp(float(row[asr_score_index]))
				cos = Cosin.compare(asr, out_trans)
				cos2 = Cosin.compare(asr, body[i-1][asr_index][1:-1]) if float(turn_id) > 0 and i > 0 else 0
				wordcount = len(asr.split()) if len(asr) > 0 else 0
				sluscore = row[sluscore_index]
				input_duration = float(row[input_end_index]) - float(row[input_start_index]) if row[input_end_index] != '-1' and row[input_start_index] != '-1' else -1
				output_duration = float(row[output_end_index]) - float(row[output_start_index]) if row[output_end_index] != '-1' and row[output_start_index] != '-1' else -1
				speaker_rate = input_duration/wordcount if input_duration != -1 and wordcount > 0 else -1
	
				isrequest = IsRequestedSlot(out_act, in_act)
			
				AddConfirmedSlot(confirmedslot, out_act, in_act)
				AddNegateSlot(negateslot, out_act, in_act)
				
				isconfirmed = IsConfirmed(confirmedslot, in_act)
				isnegated = IsNegated(negateslot, in_act)
				isgeneralNegated = IsGeneralNegated(confirmedslot, in_act)
				
				isconfirmedOut = IsConfirmedOut(confirmedslot, out_act)
				isnegatedOut = IsNegatedOut(negateslot, out_act)
				isgeneralNegatedOut = IsGeneralNegatedOut(confirmedslot, out_act)
			
				isRequestedGoal = IsRequestedSlotGoals(out_act, goal_names)
				
				row = []
				
				row.append(asr)
				
				#row.append(sr_id)
				#row.append(dm_id)
				
				row.append(asr_score)
				row.append(cos)
				row.append(cos2)
				row.append(wordcount)
				row.append(sluscore)
				row.append(restart)
				row.append(input_duration)
				row.append(output_duration)
				row.append(speaker_rate)
				
				row.append(isrequest)
				row.append(isconfirmed)
				row.append(isnegated)
				row.append(isgeneralNegated)
				
				row.append(isconfirmedOut)
				row.append(isnegatedOut)
				row.append(isgeneralNegatedOut)
			
				for key in features.keys():
					if key in acts:
						row.append(1)
					else:
						row.append(0)
				
				if goal in isRequestedGoal:
					row.append(1)
				else:
					row.append(0)
				
				for p in predictions:
					row.append(p[i])
						
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
			#header.append("sr_id")
			#header.append("dm_id")
			header.append("ASR_Score")
			header.append("Cosin")
			header.append("Cosin2") #cosin between current input and previous input
			header.append('wordcount')
			header.append('sluscore')
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
		
			for key in features.keys():
				header.append(key)
			#header = header + ['@@Class@@']
			
			header.append('isRequestedGoal')
			
			for p in ['focus','hwu','nbest']:
				header.append(p)
					
			goal = 'L' + goal

			header.append(goal)
			
			types = []
			types.append("String")
			#types.append("Continuous")#SR_ID
			#types.append("Continuous")#DM_ID
			types.append("Continuous")#ASR_Score
			types.append("Continuous")#Cosin
			types.append('Continuous')
			types.append('Continuous')#wordcount
			types.append('Continuous')#sluscore
			types.append('Category')#restartFlag
			types.append('Continuous')#input_duration
			types.append('Continuous')#output_duration
			types.append('Continuous')#speaker_rate
		
			types.append('Category')#isrequest
			types.append('Category')
			types.append('Category')
			types.append('Category')
			
			types.append('Category')
			types.append('Category')
			types.append('Category')
		
			for key in features.keys():
				types.append('Category')
				
			types = types + ['Category']
			
			for p in ['focus','hwu','nbest']:
				types.append('Category')
				
			types = types + ['Category']
			
			#fio.MulanWriter("res/"+test+"_goals_actngram", goal_names, header, types, "dstc", data)
			#fio.ArffWriter("res/"+test+"_goals_enrich_sr_" + goal +".arff", header, types, "dstc", data)
			#fio.ArffWriter("res/"+test+"_goals_enrich_dm_" + goal +".arff", header, types, "dstc", data)
			fio.ArffWriter("res/"+test+"_goals_enrich_logasr_hybrid_" + goal +".arff", header, types, "dstc", data)
			#fio.writeMatrix("res/"+test+"_goals_enrich_logasr_" + goal +".matrix", data, header)

def getMulanARFF_WizOz(featurefile, tests):
	features = fio.LoadDict("res/"+featurefile+"_name.dict")
	
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
		#goal_names = ['area', 'food', 'name', 'pricerange']
		goal_names = ['area', 'pricerange']
		
		for goal in goal_names:
			data = []
			
			confirmedslot = {}
			negateslot = {}
		
			for i,row in enumerate(body):
				turn_id = row[turn_index]
				
				if turn_id == '0':
					confirmedslot = {}
					negateslot = {}

				out_act = row[out_index][1:-1]
				in_act = row[in_index][1:-1]
				asr = row[asr_index][1:-1]
				#asr = row[in_trans_index][1:-1]
				
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
	
				isrequest = IsRequestedSlot(out_act, in_act)
			
				AddConfirmedSlot(confirmedslot, out_act, in_act)
				AddNegateSlot(negateslot, out_act, in_act)
				
				isconfirmed = IsConfirmed(confirmedslot, in_act)
				isnegated = IsNegated(negateslot, in_act)
				isgeneralNegated = IsGeneralNegated(confirmedslot, in_act)
				
				isconfirmedOut = IsConfirmedOut(confirmedslot, out_act)
				isnegatedOut = IsNegatedOut(negateslot, out_act)
				isgeneralNegatedOut = IsGeneralNegatedOut(confirmedslot, out_act)
			
				isRequestedGoal = IsRequestedSlotGoals(out_act, goal_names)
				
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
				
				row.append(isrequest)
				row.append(isconfirmed)
				row.append(isnegated)
				row.append(isgeneralNegated)
				
				row.append(isconfirmedOut)
				row.append(isnegatedOut)
				row.append(isgeneralNegatedOut)
			
				for key in features.keys():
					if key in acts:
						row.append(1)
					else:
						row.append(0)
				
				if goal in isRequestedGoal:
					row.append(1)
				else:
					row.append(0)
				
				for other in goal_names:
					if other == goal: continue
					if other in goaldict:
						if other == 'name' or other == 'food':
							if goaldict[other]=='dontcare':
								row.append(other + '.Yes.dontcare')
							else:
								row.append(other + '.Yes')
						else:
							row.append(other + '.Yes.'+goaldict[other])
					else:
						row.append(other + '.No')
							
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
			
			header.append('isrequest')
			header.append('isconfirmed')
			header.append('isnegated')
			header.append('isgeneralNegated')
			header.append('isconfirmedOut')
			header.append('isnegatedOut')
			header.append('isgeneralNegatedOut')
		
			for key in features.keys():
				header.append(key)
			#header = header + ['@@Class@@']
			
			header.append('isRequestedGoal')
			
			for other in goal_names:
				if other == goal: continue
				other = 'L' + other
				header.append(other)
					
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
		
			types.append('Category')#isrequest
			types.append('Category')
			types.append('Category')
			types.append('Category')
			
			types.append('Category')
			types.append('Category')
			types.append('Category')
		
			for key in features.keys():
				types.append('Category')
				
			types = types + ['Category']#isRequestedGoal
			
			for other in goal_names:
				if other == goal: continue
				types = types + ['Category']
				
			types = types + ['Category']
			
			#fio.ArffWriter("res/"+test+"_goals_wizoz_" + goal +".arff", header, types, "dstc", data)
			fio.ArffWriter("res/"+test+"_goals_wizoz_area&price_" + goal +".arff", header, types, "dstc", data)

def getMulanARFF_ASRs(featurefile, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+"_name.dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		sr_id_index = head.index('sr_id')
		dm_id_index = head.index('dm_id')
		
		turn_index= head.index('turn_index')
		rank_index = head.index('rank')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		asr_index = head.index('ASRs')
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
			
			confirmedslot = {}
			negateslot = {}
		
			for i,row in enumerate(body):
				turn_id = row[turn_index]
				
				sr_id = row[sr_id_index]
				dm_id = row[dm_id_index]
			
				if turn_id == '0':
					confirmedslot = {}
					negateslot = {}

				out_act = row[out_index][1:-1]
				in_act = row[in_index][1:-1]
				asr = row[asr_index][1:-1]
				asr = asr.replace('#',' ')
				
				#asr = row[in_trans_index][1:-1]
				
				out_trans = row[out_trans_index]
				#acts = set( list(getAct(out_act, "out_", True)) + list(getAct(in_act, "in_", True)))
				acts = set( list(getAct(out_act, "out_", True)))
				
				goals = row[goal_index][1:-1]
				
				goaldict = getGoalsDict(goals)
				
				restart = row[restart_index]
				asr_score = math.exp(float(row[asr_score_index]))
				cos = Cosin.compare(asr, out_trans)
				cos2 = Cosin.compare(asr, body[i-1][asr_index][1:-1]) if float(turn_id) > 0 and i > 0 else 0
				wordcount = len(asr.split()) if len(asr) > 0 else 0
				sluscore = row[sluscore_index]
				input_duration = float(row[input_end_index]) - float(row[input_start_index]) if row[input_end_index] != '-1' and row[input_start_index] != '-1' else -1
				output_duration = float(row[output_end_index]) - float(row[output_start_index]) if row[output_end_index] != '-1' and row[output_start_index] != '-1' else -1
				speaker_rate = input_duration/wordcount if input_duration != -1 and wordcount > 0 else -1
	
				isrequest = IsRequestedSlot(out_act, in_act)
			
				AddConfirmedSlot(confirmedslot, out_act, in_act)
				AddNegateSlot(negateslot, out_act, in_act)
				
				isconfirmed = IsConfirmed(confirmedslot, in_act)
				isnegated = IsNegated(negateslot, in_act)
				isgeneralNegated = IsGeneralNegated(confirmedslot, in_act)
				
				isconfirmedOut = IsConfirmedOut(confirmedslot, out_act)
				isnegatedOut = IsNegatedOut(negateslot, out_act)
				isgeneralNegatedOut = IsGeneralNegatedOut(confirmedslot, out_act)
			
				isRequestedGoal = IsRequestedSlotGoals(out_act, goal_names)
				
				row = []
				
				row.append(asr)
				
				#row.append(sr_id)
				#row.append(dm_id)
				
				#row.append(asr_score)
				#row.append(cos)
				#row.append(cos2)
				#row.append(wordcount)
				#row.append(sluscore)
				#row.append(restart)
				#row.append(input_duration)
				#row.append(output_duration)
				#row.append(speaker_rate)
				
				#row.append(isrequest)
				#row.append(isconfirmed)
				#row.append(isnegated)
				#row.append(isgeneralNegated)
				
				#row.append(isconfirmedOut)
				#row.append(isnegatedOut)
				#row.append(isgeneralNegatedOut)
			
				for key in features.keys():
					if key in acts:
						row.append(1)
					else:
						row.append(0)
				
				#if goal in isRequestedGoal:
				#	row.append(1)
				#else:
				#	row.append(0)
						
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
			#header.append("sr_id")
			#header.append("dm_id")
			#header.append("ASR_Score")
			#header.append("Cosin")
			#header.append("Cosin2") #cosin between current input and previous input
			#header.append('wordcount')
			#header.append('sluscore')
			#header.append('restartFlag')
			#header.append('input_duration')
			#header.append('output_duration')
			#header.append('speaker_rate')
			
			#header.append('isrequest')
			#header.append('isconfirmed')
			#header.append('isnegated')
			#header.append('isgeneralNegated')
			#header.append('isconfirmedOut')
			#header.append('isnegatedOut')
			#header.append('isgeneralNegatedOut')
		
			for key in features.keys():
				header.append(key)
			#header = header + ['@@Class@@']
			
			#header.append('isRequestedGoal')
			
			goal = 'L' + goal

			header.append(goal)
			
			types = []
			types.append("String")
			#types.append("Continuous")#SR_ID
			#types.append("Continuous")#DM_ID
			#types.append("Continuous")#ASR_Score
			#types.append("Continuous")#Cosin
			#types.append('Continuous')
			#types.append('Continuous')#wordcount
			#types.append('Continuous')#sluscore
			#types.append('Category')#restartFlag
			#types.append('Continuous')#input_duration
			#types.append('Continuous')#output_duration
			#types.append('Continuous')#speaker_rate
		
			#types.append('Category')#isrequest
			#types.append('Category')
			#types.append('Category')
			#types.append('Category')
			
			#types.append('Category')
			#types.append('Category')
			#types.append('Category')
		
			for key in features.keys():
				types.append('Category')
				
			#types = types + ['Category']
			types = types + ['Category']
			
			#fio.MulanWriter("res/"+test+"_goals_actngram", goal_names, header, types, "dstc", data)
			#fio.ArffWriter("res/"+test+"_goals_enrich_sr_" + goal +".arff", header, types, "dstc", data)
			#fio.ArffWriter("res/"+test+"_goals_enrich_dm_" + goal +".arff", header, types, "dstc", data)
			fio.ArffWriter("res/"+test+"_goals_enrich_asrs_" + goal +".arff", header, types, "dstc", data)
			#fio.writeMatrix("res/"+test+"_goals_enrich_logasr_" + goal +".matrix", data, header)

def getWekaARFFBinarySwitch_ASRs(featurefile, tests):
	#Feature Set: Act with Name, System out, User Slot in
	
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+"_name.dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		out_index = head.index('output acts')
		
		asr_index = head.index('ASRs')
		goal_index = head.index('recovery_goals')
		goal_names = ['area', 'food', 'name', 'pricerange']
		#goal_names = ['food']
		sr_id_index = head.index('sr_id')
		
		data = []
		
		for goal in goal_names:
			data = []
			
			for i,row in enumerate(body):
				out_act = row[out_index][1:-1]
				
				ASRs = row[asr_index][1:-1].split('#')
				acts = set( list(getAct(out_act, "out_", True)))
				goals = row[goal_index][1:-1]
				goaldict = getGoalsDict(goals)
				sr_id = row[sr_id_index]
				
				#asr = ASRs[0]
				
				#if True:
				for asr in ASRs:
					row = []
					
					#asr = asr.replace("'","\\'")
					
					#hasFood = -1
					#e_asr = ' ' + asr + ' '
					#for food in foodnames:
					#	if e_asr.find(food) != -1:
					#		hasFood = 0
					#		e_asr = e_asr.replace(food, ' FFFFD ')
					#		#break
					
					#asr = e_asr.strip()
						
					row.append(asr)
					row.append(sr_id)

					for key in features.keys():
						if key in acts:
							row.append(1)
						else:
							row.append(0)
					
					#row.append(hasFood)
							
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
			header.append("SR_ID")
			
			for key in features.keys():
				header.append(key)
			
			#header.append("hasFood")
			
			goal = 'L' + goal

			header.append(goal)
			
			types = []
			types.append("String")
			types.append('Category')
			for key in features.keys():
				types.append('Category')
			
			#types = types + ['Category']#hasFood
				
			types = types + ['Category']
			
			#fio.ArffWriter("res/"+test+"_nbest_goals_enrich_asrs_class_" + goal +".arff", header, types, "dstc", data)
			fio.ArffWriter("res/"+test+"_nbest_goals_asrs_" + goal +".arff", header, types, "dstc", data)
																				
def getWekaARFFBinarySwitch_ASR_Act_Score(featurefile, tests):
	#Feature Set: Act with Name, System out, User Slot in
	
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+"_name.dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		out_index = head.index('output acts')
		
		#asr_index = head.index('ASRs')
		goal_index = head.index('recovery_goals')
		goal_names = ['area', 'food', 'name', 'pricerange']
		#goal_names = ['food']
		sr_id_index = head.index('sr_id')
		
		#asr_index = head.index('ASRs')
		asr_index = head.index('input trans')
		asr_score_index = head.index('ASR_Scores')
		sr_id_index = head.index('sr_id')
		
		data = []
		
		for goal in goal_names:
			data = []
			
			for i,row in enumerate(body):
				out_act = row[out_index][1:-1]
				
				#ASRs = row[asr_index][1:-1].split('#')
				acts = set( list(getAct(out_act, "out_", True)))
				goals = row[goal_index][1:-1]
				goaldict = getGoalsDict(goals)
				sr_id = row[sr_id_index]
				
				ASRs = row[asr_index][1:-1].split('#')
				ASR_Scores = row[asr_score_index][1:-1].split('#')
				sr_id = row[sr_id_index]
			
				#asr = ASRs[0]
				
				#if True:
				for i,asr in enumerate(ASRs):
					row = []
					
					#asr = asr.replace("'","\\'")
					
					#hasFood = -1
					#e_asr = ' ' + asr + ' '
					#for food in foodnames:
					#	if e_asr.find(food) != -1:
					#		hasFood = 0
					#		e_asr = e_asr.replace(food, ' FFFFD ')
					#		#break
					
					#asr = e_asr.strip()
					
					if i>0: continue
				
					row.append(asr)
					row.append(float(ASR_Scores[i]))
					row.append(sr_id)
					
					for key in features.keys():
						if key in acts:
							row.append(1)
						else:
							row.append(0)
					
					#row.append(hasFood)
					'''
					if goal in goaldict:
						if goal == 'name':
							if goaldict[goal]=='dontcare':
								row.append(goal + '.Yes.dontcare')
							else:
								row.append(goal + '.Yes')
						else:
							row.append(goal + '.Yes.'+goaldict[goal])
					else:
						row.append(goal + '.No')
					'''

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
			header.append("SR_ID")
			
			for key in features.keys():
				header.append(key)
			
			#header.append("hasFood")
			
			goal = 'L' + goal

			header.append(goal)
			
			types = []
			types.append("String")
			types = types + ['Continuous']
			types.append('Category')
			for key in features.keys():
				types.append('Category')
			
			#types = types + ['Category']#hasFood
				
			types = types + ['Category']
			
			#fio.ArffWriter("res/"+test+"_nbest_goals_enrich_asrs_class_" + goal +".arff", header, types, "dstc", data)
			fio.ArffWriter("res/"+test+"_trans_" + goal +".arff", header, types, "dstc", data)
																				
if (__name__ == '__main__'):
						
	#getMulanARFF_ActNgram("dstc2_train", ["dstc2_train", "dstc2_dev"])
	#getMulanARFF_ActWithNameNgram("dstc2_train", ["dstc2_train", "dstc2_dev"])
	#getMulanARFF_ASRs("dstc2_train", ["dstc2_train", "dstc2_dev"])
	#getMulanARFF_Enrich("dstc2_train", ["dstc2_train", "dstc2_dev"])
	#getMulanARFF_Enrich("dstc2_train", ["dstc2_train", "dstc2_test"])
	getWekaARFFBinarySwitch_ASR_Act_Score("dstc2_train", ["dstc2_train", "dstc2_dev"])
	getWekaARFFBinarySwitch_ASR_Act_Score("dstc2_traindev", ["dstc2_traindev", "dstc2_test"])
	#getWekaARFFBinarySwitch_ASRs("dstc2_traindev", ["dstc2_dev"])
	#getWekaARFFBinarySwitch_ASRs("dstc2_traindevtest", ["dstc2_test"])
	#getMulanARFF_WizOz("dstc2_train", ["dstc2_train", "dstc2_dev"])
	print "Done"