import sys,os,argparse,shutil,glob,json,copy,time
import fio
import dataset_walker

def quote(s):
	if s == None:
		return '""'
	return '"' + s + '"'

def parenthesis(s):
	if s == None:
		return '()'
	return '(' + s + ')'

def strlist(l):
	return ';'.join(l)
	
def strdict(slot):
	l = [k+'='+v for k,v in slot.items()]
	return ";".join(l)
	
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
									
#H1: assume that the SLU is correct if and only if all the SLU hyps (slot,value) appear in the correct answer
#assume NONE is -1
#assume slu that doesn't do anything is -1
def getCorrectSLUHypRank_H1(log_turn, label_turn):
	goal_label = label_turn['goal-labels']
	method_label = label_turn['method-label']
	request_slots = label_turn['requested-slots']
	
	#fixed this first
	log_turn = fixedThis(log_turn)
	
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
		if hasInfo and correct: return k
		
	return -1

#H2: assume that the SLU is correct if and only if it matches the differences between the pervious correct answer and the current one
def getCorrectSLUHypRank_H2(log_turn, label_turn):
	pass

#H3: assume that the SLU is correct if and only if it will turn into the correct answer based on the previous one and the new SLU
def getCorrectSLUHypRank_H3(log_turn, label_turn):
	pass

def getLabels(label_turn):#goal is a dict; method is a string; request is a list
	if label_turn == None:
		return None, None, None
	
	goal_label = label_turn['goal-labels']
	method_label = label_turn['method-label']
	request_label = label_turn['requested-slots']
	return goal_label, method_label, request_label
				
def main(argv):
	parser = argparse.ArgumentParser(description='Simple hand-crafted dialog state tracker baseline.')
	parser.add_argument('--dataset', dest='dataset', action='store', metavar='DATASET', required=True,
						help='The dataset to analyze')
	parser.add_argument('--dataroot',dest='dataroot',action='store',required=True,metavar='PATH',
						help='Will look for corpus in <destroot>/<dataset>/...')
	parser.add_argument('--logfile',dest='logfile',action='store',required=True,metavar='TEXT_FILE',
						help='File to write with summary output')
	
	args = parser.parse_args()
	sessions = dataset_walker.dataset_walker(args.dataset, dataroot=args.dataroot, labels=True)

	sum = []
	
	for session in sessions:
		session_id = session.log['session-id']
		
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
				if 'transcription' in label_turn:
					input_trans = label_turn['transcription']
				elif 'transcript' in label_turn: #for test3
					input_trans = label_turn['transcript']
				else:
					input_trans = ""
				
				#output dialog acts
				output_acts = log_turn['output']['dialog-acts'] if 'dialog-acts' in log_turn['output'] else None
				
				#get correct slu label
				goal_label = label_turn['goal-labels']
				method_label = label_turn['method-label']
				request_slots = label_turn['requested-slots']
				
				#get the rank of correct slu
				rank = getCorrectSLUHypRank_H1(log_turn, label_turn)
				
				#has correct slu label
				#hasTrueLabel = hasCorrectSLULabel(label_turn)
				#correctSLULabel = getCorrectSLULabel(label_turn)
				
				#schedule
				
				row = []
				row.append(session_id)
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

				row.append(quote(strslu(top_slu)))
				row.append(quote(strslu(output_acts)))
				row.append(top_slu_score)
				
				row.append(quote(strdict(goal_label)))
				row.append(quote(method_label))
				row.append(quote(strlist(request_slots)))
				
				#row.append(hasTrueLabel)
				#row.append(quote(correctSLULabel))
				
				row.append(rank)
				#row.append(quote(correct_slu))
				
				sum.append(row)
				
			except KeyError as e:
				print str(e)
				print row
				exit()
				
	
	header = ["session_id", "turn_index"]
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
	
	header.append("top slu")
	header.append("output acts")
	header.append("top slu score")
	
	header.append("goal_label")
	header.append('method_label')
	header.append('request_slots')
				
	#header.append("hasCorrectLabel")
	#header.append("CorrectLabel")
	
	header.append("rank")
	#header.append("correct_slu")
	
	fio.writeMatrix(args.logfile, sum, header)
	
if (__name__ == '__main__'):
	main(sys.argv)
	print "Done"
