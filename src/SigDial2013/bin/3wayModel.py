#! D:\Python27\python.exe
import sys,os,argparse,shutil,glob,json,copy,time
import getSummary
import fio

SLOTS = ['route','from.desc','from.neighborhood','from.monument','to.desc','to.neighborhood','to.monument','date','time']

topK = -1

def main(argv):
	#
	# CMD LINE ARGS
	# 
	install_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	utils_dirname = os.path.join(install_path,'lib')
	sys.path.append(utils_dirname)
	from dataset_walker import dataset_walker
	list_dir = os.path.join(install_path,'config')

	parser = argparse.ArgumentParser(description='Simple hand-crafted dialog state tracker baseline.')
	parser.add_argument('--dataset', dest='dataset', action='store', metavar='DATASET', required=True,
						help='The dataset to analyze, for example train1 or test2 or train3a')
	parser.add_argument('--dataroot',dest='dataroot',action='store',required=True,metavar='PATH',
						help='Will look for corpus in <destroot>/<dataset>/...')
	parser.add_argument('--trackfile',dest='scorefile',action='store',required=True,metavar='JSON_FILE',
						help='File to write with tracker output')
	parser.add_argument('--null',dest='null',action='store_true',
						help='Always output "None of the above" for all slots with score 1.0')
	parser.add_argument('--ignorescores',dest='ignorescores',action='store_true',
						help='Ignore score in data; always use a score of 1.0 (nop if --null also specified)')
	parser.add_argument('--labelfile',dest='labelfile',action='store',required=True,metavar='TXT',
						help='File with 3-way prediction results')
	args = parser.parse_args()

	head, body = fio.readMatrix(args.labelfile, True)
	labels = [item[1] for item in body]
	turn_count = -1
	
	sessions = dataset_walker(args.dataset,dataroot=args.dataroot,labels=False)	
	start_time = time.time()
	r = {
		'sessions': [],
		'dataset': args.dataset,
		}
	
	for session in sessions:
		r['sessions'].append( { 'turns': [], 'session-id': session.log['session-id'], } )
		state = _InitState()		
		if (args.null == True):
			state['joint'] = { 'hyps': [], }
		for turn_index,(log_turn,notUsed) in enumerate(session):
			turn_count = turn_count + 1
			
			if (args.null == True):
				r['sessions'][-1]['turns'].append(state)
				continue
			# check whether to initialize state or copy
			if (log_turn['restart'] == True or turn_index == 0):
				state = _InitState()
			else:
				state = copy.deepcopy(state)
			r['sessions'][-1]['turns'].append(state)
			if (len(log_turn['input']['live']['slu-hyps']) == 0):
				# no recognition results; skip
				continue
		
			#get the predict
			#TODO
			rank = labels[turn_count]
			
			slu_hyp = None
			
			#replace slu_hyp with correct one
			if rank == '-1': continue
			if rank == '1':#top slu
				slu_hyp = log_turn['input']['live']['slu-hyps'][0]
			if rank == '0':#get the output slu
				slu_output = getSummary.getFirstExplConf(log_turn)
				slu_hyp = getSummary.formatSlottoLive(slu_output, 0)
			
			if slu_hyp == None: continue
			
			joint = {}
			joint_scores = []		
			for slot in SLOTS:
				for act_hyp in slu_hyp['slu-hyp']:
					this_pairset = {}
					for found_slot,val in act_hyp['slots']:
						if (found_slot.startswith(slot)):
							this_pairset[found_slot] = val
					if (len(this_pairset) == 0):
						continue
					if (True):
						score = slu_hyp['score'] if (args.ignorescores == False) else 1.0
						state[slot]['hyps'] = [ {
								'score-save': slu_hyp['score'],
								'score': score,
								'slots': this_pairset,
								} ]
				if (len(state[slot]['hyps']) > 0):
					joint_scores.append( state[slot]['hyps'][0]['score'] )
					for (my_slot,my_val) in state[slot]['hyps'][0]['slots'].items():
						joint[my_slot] = my_val
			state['joint'] = { 'hyps': [], }
			if (len(joint_scores) > 0):
				state['joint']['hyps'].append( {
						'score': sum(joint_scores) / len(joint_scores),
						'slots': joint,
						} )
		for turn in r['sessions'][-1]['turns']:
			for slots_entry in turn.values():
				for hyp_entry in slots_entry['hyps']:
					if ('score-save' in hyp_entry):
						del hyp_entry['score-save']
	end_time = time.time()
	elapsed_time = end_time - start_time
	r['wall-time'] = elapsed_time

	f = open(args.scorefile,'w')
	json.dump(r,f,indent=2)
	f.close()

def _InitState():
	state = {}
	for slot in SLOTS:
		state[slot] = {'hyps': [], }	
	return state

if (__name__ == '__main__'):
	main(sys.argv)
	print "Done"



