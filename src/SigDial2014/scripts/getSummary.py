import sys,os,argparse,shutil,glob,json,copy,time
import fio
import dataset_walker
import utility
import baseline
import TopLine
import math

goal_names = ['area', 'food', 'name', 'pricerange']

def quote(s):
	if s == None:
		return '""'
	return '"' + s + '"'

def parenthesis(s):
	if s == None:
		return '()'
	return '(' + s + ')'

def strlist(l):
	if l == None:
		return ""
	return ';'.join(l)
	
def strdict(slot):
	if slot == None:
		return ""
	l = [k+'='+v for k,v in slot.items()]
	return ";".join(l)

def getActText(slu):
	tokens = slu.split('&')
	
	text = ""
	for token in tokens:
		k = token.find('(')
		if k == -1: continue
		k3 = token.find(')')
		if k3 == -1: continue
		
		k2 = token.find('=')
		if k2==-1: continue
		
		text = text + " " + token[k2+1:k3]
		
	return text.strip()
	
def strslu(slu_hyp):#format the slu hyp into a line; input is an array of slot=value
	if slu_hyp == None: 
		return ''
	
	rhyp = []
	for slu in slu_hyp:
		hyp_array = []
		hyps = []
		for slot in slu['slots']:
			try:
				hyp = '='.join([str(s) for s in slot])
			except TypeError:
				print slot
			hyps.append(hyp)
			
		hyps = ';'.join(hyps)
		
		if 'act' in slu:
			rhyp.append(slu['act'] + parenthesis(hyps))
		else:	
			rhyp.append(hyps)
	
	return '&'.join(rhyp)
								
def checkValueDict(dict, key, value):
	if key not in dict: return False
	if dict[key] != value: return False
	return True
	
def fixedThis(log_turn):
	mact = []
	if "dialog-acts" in log_turn["output"] :
		mact = log_turn["output"]["dialog-acts"]
	
	this_slot = None
	
	for act in mact :
		if act["act"] == "request" :
			this_slot = act["slots"][0][1]
		elif act["act"] == "select" :
			this_slot = act["slots"][0][0]
		elif act["act"] == "expl-conf" :
			this_slot = act["slots"][0][0]
	
	for k, hyps in enumerate(log_turn['input']['live']['slu-hyps']):
		for hyp in hyps['slu-hyp']:
			for slot in hyp["slots"]:
				if len(slot) != 2: continue
				if slot[0] == 'this':
					if this_slot != None:
						slot[0] = this_slot
			
	return log_turn

def IsCorrectSLUHypRank_H1(hyps, label_turn):
	if label_turn == None:
		return False
	
	goal_label = label_turn['goal-labels']
	method_label = label_turn['method-label']
	request_slots = label_turn['requested-slots']
	
	correct = True
	hasInfo = False
	for hyp in hyps['slu-hyp']:
		if hyp['act'] == 'inform':
			hasInfo = True
			for slot in hyp['slots']:
				if len(slot) != 2: continue
				
				if not checkValueDict(goal_label, slot[0], slot[1]): 
					correct = False
					break
		if hyp['act'] == 'request':
			hasInfo = True
			if hyp['slots'][0][1] not in request_slots: 
				correct = False	
				break
		if hyp['act'] == 'bye':
			hasInfo = True
			if method_label != 'finished': 
				correct = False	
				break
		if hyp['act'] == 'reqalts':
			hasInfo = True
			if method_label != 'byalternatives': 
				correct = False	
				break
	if hasInfo and correct: 
		return True
	return False

def getCorrectOutGoals(log_turn):
	dict = {}
	
	if 'dialog-acts' in log_turn['output']:#the correct one is from the output
		for output_act in log_turn['output']['dialog-acts']:
			act = output_act['act']
			if act != "expl-conf" and act != "inform" and act != "impl-conf": continue
			
			slu_dict = {}
			slu_dict['slots'] = {}
			for slot in output_act['slots']:
				if len(slot) == 2:
					if slot[0] in goal_names:
						dict[slot[0]] = slot[1]
	return dict
						
def IsCorrectOutSLUHyp(log_turn, label_turn):
	correct = True
	hasInfo = False
	
	goal_label = label_turn['goal-labels']
	
	if 'dialog-acts' in log_turn['output']:#the correct one is from the output
		for output_act in log_turn['output']['dialog-acts']:
			act = output_act['act']
			if act != "expl-conf" and act != "inform" and act != "impl-conf": continue
			
			slu_dict = {}
			slu_dict['slots'] = {}
			for slot in output_act['slots']:
				if len(slot) == 2:
					if slot[0] in goal_label:
						hasInfo = True
						if slot[1] != goal_label[slot[0]]:
							correct = False
							break
			
	if hasInfo and correct: 
		return True
	return False
				
def getCorrectSLUHypRank_H1(log_turn, label_turn):
	'''
	#H1: assume that the SLU is correct if and only if all the SLU hyps (slot,value) appear in the correct answer
	#assume NONE is -1
	#assume slu that doesn't do anything is -1
	'''
	if label_turn == None:
		return -1
	
	goal_label = label_turn['goal-labels']
	method_label = label_turn['method-label']
	request_slots = label_turn['requested-slots']
	
	#fixed this first
	log_turn = fixedThis(log_turn)
		
	if IsCorrectOutSLUHyp(log_turn, label_turn):
		return 0
	
	for k, hyps in enumerate(log_turn['input']['live']['slu-hyps']):
		correct = True
		hasInfo = False
		for hyp in hyps['slu-hyp']:
			if hyp['act'] == 'inform':
				hasInfo = True
				for slot in hyp['slots']:
					if len(slot) != 2: continue
					
					if not checkValueDict(goal_label, slot[0], slot[1]): 
						correct = False
						break
			if hyp['act'] == 'request':
				hasInfo = True
				if hyp['slots'][0][1] not in request_slots: 
					correct = False	
					break
			if hyp['act'] == 'bye':
				hasInfo = True
				if method_label != 'finished': 
					correct = False	
					break
			if hyp['act'] == 'reqalts':
				hasInfo = True
				if method_label != 'byalternatives': 
					correct = False	
					break
		if hasInfo and correct: return k+1
		
	return -1

def getCorrectSLUHypRank_H2(log_turn, label_turn, last_labelturn = None):
	'''
	#H2: assume that the SLU is correct if and only if it matches the differences between the previous correct answer and the current one
	only for "request" and "inform"
	'''
	if label_turn == None:
		return -1
	goal_label, method_label, request_label = getLabels(label_turn)
	p_goal_label, p_method_label, p_request_label = getLabels(last_labelturn)
	
	d_goal_label = utility.sub(goal_label, p_goal_label)
	d_request_label = utility.sub(request_label, p_request_label)
	
	#fixed this first
	log_turn = fixedThis(log_turn)
	
	for k, hyps in enumerate(log_turn['input']['live']['slu-hyps']):
		#check x in A-B
		correct = True
		for hyp in hyps['slu-hyp']:
			if hyp['act'] == 'inform':
				for slot in hyp['slots']:
					if len(slot) != 2: continue
					
					if not checkValueDict(d_goal_label, slot[0], slot[1]): 
						correct = False
						break
			if hyp['act'] == 'request':
				hasInfo = True
				if hyp['slots'][0][1] not in d_request_label: 
					correct = False
					break
			if hyp['act'] == 'bye':
				if method_label != 'finished': 
					correct = False
					break
			if hyp['act'] == 'reqalts':
				if method_label != 'byalternatives': 
					correct = False	
					break
			
		if not correct: continue
		
		#check A-B in X
		for key, value in d_goal_label.items():
			found = False
			
			for hyp in hyps['slu-hyp']:
				if hyp['act'] == 'inform':
					for slot in hyp['slots']:
						if len(slot) != 2: continue
						
						if slot[0] == key and slot[1] == value:
							found = True
							break
					if found: break
			if not found:
				correct = False
				break
						
		if not correct: continue
		
		for dk in d_request_label:
			found = False
			
			for hyp in hyps['slu-hyp']:
				if hyp['act'] == 'request':
					if hyp['slots'][0][1] == dk: 
						found = True
						break
					
			if not found:
				correct = False
				break
			
		if correct:
			return k
		
	return -1

def getNewOutput(mact, slu, label_turn, last_labelturn):
	if label_turn == None:
		return None
	
	goal_label, method_label, request_label = getLabels(label_turn)
	p_goal_label, p_method_label, p_request_label = getLabels(last_labelturn)
	
	n_goal_label = copy.deepcopy(p_goal_label)
	n_method_label = copy.deepcopy(p_method_label)
	n_request_label = copy.deepcopy(p_request_label)
	
	# clear requested-slots that have been informed
	for act in mact:
		if act["act"] == "inform" :
			for slot,value in act["slots"]:
				if slot in n_request_label:
					n_request_label.remove(slot)
					
	score, uact = slu
	informed_goals, denied_goals, requested, method = baseline.labels(uact, mact)
	
	# requested	
	for slot in requested:
		if slot not in n_request_label:
			n_request_label.append(slot)
	
	n_method_label = method
	
	# goal_labels
	for slot in informed_goals:
		value = informed_goals[slot]
		n_goal_label[slot] = value
	
	return n_goal_label, n_method_label, n_request_label

def CheckNewOutput(mact, slu, label_turn, last_labelturn):
	if label_turn == None:
		return False
	
	goal_label, method_label, request_label = getLabels(label_turn)
	p_goal_label, p_method_label, p_request_label = getLabels(last_labelturn)
	
	n_goal_label = copy.deepcopy(p_goal_label)
	n_method_label = copy.deepcopy(p_method_label)
	n_request_label = copy.deepcopy(p_request_label)
	
	# clear requested-slots that have been informed
	for act in mact:
		if act["act"] == "inform" :
			for slot,value in act["slots"]:
				if slot in n_request_label:
					n_request_label.remove(slot)
					
	score, uact = slu
	informed_goals, denied_goals, requested, method = baseline.labels(uact, mact)
	
	# requested	
	for slot in requested:
		if slot not in n_request_label:
			n_request_label.append(slot)
		
	if method != "none" :
		n_method_label = method
	
	# goal_labels
	for slot in informed_goals:
		value = informed_goals[slot]
		n_goal_label[slot] = value
	
	if n_method_label != str(method_label): return False
	if sorted(n_request_label) != sorted(request_label): return False
	if n_goal_label != goal_label: return False
	
	return True
	
#H3: assume that the SLU is correct if and only if it will turn into the correct answer based on the previous one and the new SLU
def getCorrectSLUHypRank_H3(log_turn, label_turn, last_labelturn = None):
	if label_turn == None:
		return -1
	
	if "dialog-acts" in log_turn["output"] :
		mact = log_turn["output"]["dialog-acts"]
	else :
		mact = []
		
	slu_hyps = baseline.Uacts(log_turn)
	
	for k, slu in enumerate(slu_hyps):
		if CheckNewOutput(mact, slu, label_turn, last_labelturn):
			return k
		
	return -1

def getCorrectSLURequestRank(log_turn, label_turn, last_labelturn):
	request_label = label_turn['requested-slots']
	if len(request_label) == 0: return -2
	
	for k, hyps in enumerate(log_turn['input']['live']['slu-hyps']):
		correct = True
		request = []
		for hyp in hyps['slu-hyp']:
			if hyp['act'] == 'request':
				request.append(hyp['slots'][0][1])
		if(sorted(request) == sorted(request_label)):
			return k
	return -1

def getLabels(label_turn):#goal is a dict; method is a string; request is a list
	if label_turn == None:
		return {}, u'none', []
	
	goal_label = label_turn['goal-labels']
	method_label = label_turn['method-label']
	request_label = label_turn['requested-slots']
	return goal_label, method_label, request_label

def getRecoveryMethod(log_turn, label_turn, last_labelturn):
	if label_turn == None:
		return "none"
	
	if "dialog-acts" in log_turn["output"] :
		mact = log_turn["output"]["dialog-acts"]
	else :
		mact = []
	
	p_goal_label, p_method_label, p_request_label = getLabels(last_labelturn)
	goal_label, method_label, request_label = getLabels(label_turn)
	
	if method_label != p_method_label:
		return method_label
	else:
		return "none"
	
	'''
	slu_hyps = baseline.Uacts(log_turn)
	if len(slu_hyps) > 0:
		n_goal_label, n_method_label, n_request_label = getNewOutput(mact, slu_hyps[0], label_turn, last_labelturn)
		if n_method_label == method_label:
			return method_label
		
		return "none"
	else:
		return method_label
	'''
	
	return "impossible"

def getRecoveryGoals(log_turn, label_turn, last_labelturn):
	if label_turn == None:
		return {}
	
	if "dialog-acts" in log_turn["output"] :
		mact = log_turn["output"]["dialog-acts"]
	else :
		mact = []
	
	p_goal_label, p_method_label, p_request_label = getLabels(last_labelturn)
	goal_label, method_label, request_label = getLabels(label_turn)
	
	return utility.sub(goal_label, p_goal_label)

def getTurns(sessions, label = True):# fixed this
	log_turns = []
	label_turns = []
		
	for session in sessions:
		for turn_index,(log_turn,label_turn) in enumerate(session):
			log_turn = fixedThis(log_turn)
			log_turns.append(log_turn)
			label_turns.append(label_turn)
	return log_turns, label_turns

def getASRs(log_turn):
	ASRs = []
	#score = 0
	for asr in log_turn['input']['live']['asr-hyps']:
		ASRs.append(asr['asr-hyp'])
		#score = score + math.exp(asr['score'])
		#score = score + math.pow(2, asr['score'])
	#print score
	return "#".join(ASRs)

def getASR_Scores(log_turn):
	ASRs = []
	#score = 0
	for asr in log_turn['input']['live']['asr-hyps']:
		ASRs.append(str(math.exp(asr['score'])))
		#score = score + math.exp(asr['score'])
		#score = score + math.pow(2, asr['score'])
	#print score
	return "#".join(ASRs)
							
def main(argv):
	parser = argparse.ArgumentParser(description='Simple hand-crafted dialog state tracker baseline.')
	parser.add_argument('--dataset', dest='dataset', action='store', metavar='DATASET', required=True,
						help='The dataset to analyze')
	parser.add_argument('--dataroot',dest='dataroot',action='store',required=True,metavar='PATH',
						help='Will look for corpus in <destroot>/<dataset>/...')
	parser.add_argument('--logfile',dest='logfile',action='store',required=True,metavar='TEXT_FILE',
						help='File to write with summary output')
	
	args = parser.parse_args()
	
	#if "test" in args.dataset:
	#	sessions = dataset_walker.dataset_walker(args.dataset, dataroot=args.dataroot, labels=False)
	#else:
	sessions = dataset_walker.dataset_walker(args.dataset, dataroot=args.dataroot, labels=True)
		
	sum = []
	
	for session in sessions:
		session_id = session.log['session-id']
		sr_id = session.log['system-specific']['acoustic-condition'] #speech recognizer id
		dm_id = session.log['system-specific']['dialog-manager'] #dialog manager id
		
		last_labelturn = None
		
		for turn_index,(log_turn,label_turn) in enumerate(session):
			
			try:
				aborted = log_turn['output']['aborted'] if 'aborted' in log_turn['output'] else None
				
				#number of asr
				n_asr_live = len(log_turn['input']['live']['asr-hyps'])
				#n_asr_batch = len(log_turn['input']['batch']['asr-hyps']) if 'batch' in log_turn['input'] else 0
				
				#number of slu
				n_slu_live = len(log_turn['input']['live']['slu-hyps'])
				#n_slu_batch = len(log_turn['input']['batch']['slu-hyps']) if 'batch' in log_turn['input'] else 0
				
				#top asr
				top_asr = log_turn['input']['live']['asr-hyps'][0]['asr-hyp'] if len(log_turn['input']['live']['asr-hyps']) > 0 else ''
				asr_score = log_turn['input']['live']['asr-hyps'][0]['score'] if len(log_turn['input']['live']['asr-hyps']) > 0 else -1
				
				ASRs = getASRs(log_turn)
				ASR_Scores = getASR_Scores(log_turn)
				
				#top nlu
				top_slu = log_turn['input']['live']['slu-hyps'][0]['slu-hyp'] if len(log_turn['input']['live']['slu-hyps']) > 0 else None
				
				top_slu_score = log_turn['input']['live']['slu-hyps'][0]['score'] if len(log_turn['input']['live']['slu-hyps']) > 0 else -1
				
				intput_start_time = log_turn['input']['start-time'] if 'start-time' in log_turn['input'] else -1
				intput_end_time = log_turn['input']['end-time'] if 'end-time' in log_turn['input'] else -1
				output_start_time = log_turn['output']['start-time'] if 'start-time' in log_turn['output'] else -1
				output_end_time = log_turn['output']['end-time'] if 'end-time' in log_turn['output'] else -1
				
				#output transcription
				output_trans = log_turn['output']['transcript'] if 'transcript' in log_turn['output'] else None
	
				#input transcription
				if label_turn != None:
					if 'transcription' in label_turn:
						input_trans = label_turn['transcription']
					elif 'transcript' in label_turn: #for test3
						input_trans = label_turn['transcript']
					else:
						input_trans = ""
				else:
					input_trans = ""
				
				#output dialog acts
				output_acts = log_turn['output']['dialog-acts'] if 'dialog-acts' in log_turn['output'] else None
				
				#get correct slu label
				goal_label = label_turn['goal-labels'] if label_turn != None else {}
				method_label = label_turn['method-label'] if label_turn != None else "none"
				request_slots = label_turn['requested-slots'] if label_turn != None else []
				
				#get the rank of correct slu
				rank = getCorrectSLUHypRank_H1(log_turn, label_turn)
				rank_H2 = getCorrectSLUHypRank_H2(log_turn, label_turn, last_labelturn)
				rank_H3 = getCorrectSLUHypRank_H3(log_turn, label_turn, last_labelturn)
				rank_request = getCorrectSLURequestRank(log_turn, label_turn, last_labelturn)
				num_request = len(request_slots)
				
				recovery_method = getRecoveryMethod(log_turn, label_turn, last_labelturn)
				recovery_goals = getRecoveryGoals(log_turn, label_turn, last_labelturn)
				
				InSLU = TopLine.findSLUGoals(log_turn, goal_label)
				InARS = TopLine.findASRGoals(log_turn, goal_label)
				InTrans = TopLine.findTranscriptionGoals(label_turn, goal_label)

				#has correct slu label
				#hasTrueLabel = hasCorrectSLULabel(label_turn)
				#correctSLULabel = getCorrectSLULabel(label_turn)
				
				#schedule
				
				row = []
				row.append(session_id)
				row.append(sr_id)
				row.append(dm_id)
				
				row.append(turn_index)
				row.append(aborted)
				row.append(n_asr_live)
				#row.append(n_asr_batch)
				row.append(n_slu_live)
				#row.append(n_slu_batch)

				row.append(output_start_time)
				row.append(output_end_time)
				row.append(intput_start_time)
				row.append(intput_end_time)

				row.append(quote(output_trans))
				row.append(quote(input_trans))
				
				row.append(quote(top_asr))
				row.append(asr_score)
				row.append(quote(ASRs))
				row.append(quote(ASR_Scores))
				row.append(quote(strslu(top_slu)))
				row.append(quote(strslu(output_acts)))
				row.append(top_slu_score)
				
				row.append(quote(strdict(goal_label)))
				row.append(quote(method_label))
				row.append(quote(strlist(request_slots)))
				
				#row.append(hasTrueLabel)
				#row.append(quote(correctSLULabel))
				
				row.append(rank)
				row.append(rank_H2)
				row.append(rank_H3)
				row.append(rank_request)
				row.append(num_request)
				#row.append(quote(correct_slu))
				row.append(quote(recovery_method))
				row.append(quote(strdict(recovery_goals)))
				
				row.append(InSLU)
				row.append(InARS)
				row.append(InTrans)
				
				sum.append(row)
				
			except KeyError as e:
				print str(e)
				print row
				exit()
			
			
			last_labelturn = copy.deepcopy(label_turn)
	
	header = ["session_id"]
	header.append('sr_id')
	header.append('dm_id')
	
	header.append("turn_index")		
	header.append("aborted")
	header.append("# of ars_live")
	#header.append("# of ars_batch")
	header.append("# of slu_live")
	#header.append("# of slu_batch")
	
	header.append('output_start_time')
	header.append('output_end_time')
	header.append('intput_start_time')
	header.append('intput_end_time')

	header.append("output trans")
	header.append("input trans")
	
	header.append("top asr")
	header.append("asr_score")
	header.append("ASRs")
	header.append("ASR_Scores")
	
	header.append("top slu")
	header.append("output acts")
	header.append("top slu score")
	
	header.append("goal_label")
	header.append('method_label')
	header.append('request_slots')
				
	#header.append("hasCorrectLabel")
	#header.append("CorrectLabel")
	
	header.append("rank")
	header.append("rank_H2")
	header.append("rank_H3")
	
	header.append("rank_request")
	header.append("num_request")
	
	header.append("recovery_method")
	header.append("recovery_goals")
	
	header.append('InSLU')
	header.append('InARS')
	header.append('InTrans')
				
	fio.writeMatrix(args.logfile, sum, header)
	
if (__name__ == '__main__'):
	main(sys.argv)
	print "Done"
