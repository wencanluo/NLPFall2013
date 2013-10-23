import sys,os,argparse,shutil,glob,json,copy,timeimport fioSLOTS = ['route','from.desc','from.neighborhood','from.monument','to.desc','to.neighborhood','to.monument','date','time']def quote(s):	if s == None:		return '""'	return '"' + s + '"'def parenthesis(s):	if s == None:		return '()'	return '(' + s + ')'		def strslu(slu_hyp):#format the slu hyp into a line; input is an array of slot=value	if slu_hyp == None: 		return ''		rhyp = []	for slu in slu_hyp:		hyp_array = []		hyps = []		for slot in slu['slots']:			try:				hyp = '='.join([str(s) for s in slot])			except TypeError:				print slot			hyps.append(hyp)					hyps = ';'.join(hyps)				if 'act' in slu:			rhyp.append(slu['act'] + parenthesis(hyps))		else:				rhyp.append(hyps)		return '&'.join(rhyp)def hasCorrectSLULabel(label_turn):	for slu in label_turn['slu-labels']:		if slu['label'] == True:			return True	return Falsedef strSLULabel(slu):#for tracker slu	top_hyp_array = []	for k in sorted(slu['slots'].keys()):		top_hyp_array.append( [k,slu['slots'][k]] )	hyp = ';'.join( [ '='.join([k,str(v)]) for k,v in top_hyp_array] )	return hypdef formatSlottoLive(correct_slu, rank):#format the string of correct_slu into live slu	if correct_slu == None or rank == -1:		return None		slu = {}	slu['score'] = 1.0		slu_hyp = {}	slu_hyp['act'] = 'inform'	slu_hyp['slots'] = []		tokens = correct_slu.split(';')		for token in tokens:		sv = token.split('=')		assert(len(sv) == 2)				if sv[0] == 'time.hour' or sv[0] == 'time.minute':			sv[1] = int(sv[1])		slu_hyp['slots'].append([sv[0], sv[1]])		slu['slu-hyp'] = [slu_hyp]	return sludef getFirstExplConf(log_turn):	if 'dialog-acts' in log_turn['output']:#the correct one is from the output		for output_act in log_turn['output']['dialog-acts']:			act = output_act['act']			if act != 'expl-conf': continue						slu_dict = {}			slu_dict['slots'] = {}			for slot in output_act['slots']:				if len(slot) == 2:					slu_dict['slots'][slot[0]] = slot[1]			strslot = strSLULabel(slu_dict)			return strslot			return None	def getCorrectSLUHyp(log_turn, label_turn):	'''	get the rank of correct slu	-1: None	0: in the output	1: first rank	...		'''	if not hasCorrectSLULabel(label_turn):		return -1, None		dict = {}	for slu in label_turn['slu-labels']:		if slu['label'] == True:			dict[strSLULabel(slu)] = True				if 'dialog-acts' in log_turn['output']:#the correct one is from the output		for output_act in log_turn['output']['dialog-acts']:			slu_dict = {}			slu_dict['slots'] = {}			for slot in output_act['slots']:				if len(slot) == 2:					slu_dict['slots'][slot[0]] = slot[1]			strslot = strSLULabel(slu_dict)			if strslot in dict:				#if output_act['act'] != 'expl-conf':				#	print output_act['act']				# it comes from expl-conf, example, n				return 0, strSLULabel(slu_dict)	index = 0	for slu_hyp in log_turn['input']['live']['slu-hyps']:		for slu in slu_hyp['slu-hyp']:			slu_dict = {}			slu_dict['slots'] = {}			for slot in slu['slots']:				assert(len(slot) == 2)				slu_dict['slots'][slot[0]] = slot[1]							index = index + 1						strslot = strSLULabel(slu_dict)			if strslot in dict:				return index, strSLULabel(slu_dict)		index = 0	if 'batch' in log_turn['input']:		for slu_hyp in log_turn['input']['batch']['slu-hyps']:			for slu in slu_hyp['slu-hyp']:				slu_dict = {}				slu_dict['slots'] = {}				for slot in slu['slots']:					assert(len(slot) == 2)					slu_dict['slots'][slot[0]] = slot[1]									index = index + 1								strslot = strSLULabel(slu_dict)				if strslot in dict:					return index, strSLULabel(slu_dict)			return -1, None						def getCorrectSLULabel(label_turn):	r = []	for slu in label_turn['slu-labels']:		if slu['label'] == True:			r.append(strSLULabel(slu))	return ';'.join(r)									def main(argv):	install_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))	utils_dirname = os.path.join(install_path,'lib')	sys.path.append(utils_dirname)	from dataset_walker import dataset_walker	list_dir = os.path.join(install_path,'config')	parser = argparse.ArgumentParser(description='Simple hand-crafted dialog state tracker baseline.')	parser.add_argument('--dataset', dest='dataset', action='store', metavar='DATASET', required=True,						help='The dataset to analyze, for example train1 or test2 or train3a')	parser.add_argument('--dataroot',dest='dataroot',action='store',required=True,metavar='PATH',						help='Will look for corpus in <destroot>/<dataset>/...')	parser.add_argument('--logfile',dest='logfile',action='store',required=True,metavar='TEXT_FILE',						help='File to write with summary output')	parser.add_argument('--null',dest='null',action='store_true',						help='Always output "None of the above" for all slots with score 1.0')	parser.add_argument('--ignorescores',dest='ignorescores',action='store_true',						help='Ignore score in data; always use a score of 1.0 (nop if --null also specified)')	args = parser.parse_args()	sessions = dataset_walker(args.dataset,dataroot=args.dataroot,labels=True)		sum = []		for session in sessions:		session_id = session.log['session-id']				for turn_index,(log_turn,label_turn) in enumerate(session):						try:				start = True if (log_turn['restart'] == True) else False								#number of asr				n_asr_live = len(log_turn['input']['live']['asr-hyps'])				n_asr_batch = len(log_turn['input']['batch']['asr-hyps']) if 'batch' in log_turn['input'] else 0								#number of slu				n_slu_live = len(log_turn['input']['live']['slu-hyps'])				n_slu_batch = len(log_turn['input']['batch']['slu-hyps']) if 'batch' in log_turn['input'] else 0								#top asr				top_asr = log_turn['input']['live']['asr-hyps'][0]['asr-hyp'] if len(log_turn['input']['live']['asr-hyps']) > 0 else ''				asr_score = log_turn['input']['live']['asr-hyps'][0]['score'] if len(log_turn['input']['live']['asr-hyps']) > 0 else -1								#top nlu				top_slu = log_turn['input']['live']['slu-hyps'][0]['slu-hyp'] if len(log_turn['input']['live']['slu-hyps']) > 0 else None								top_slu_score = log_turn['input']['live']['slu-hyps'][0]['score'] if len(log_turn['input']['live']['slu-hyps']) > 0 else -1								intput_start_time = log_turn['input']['start-time'] if 'start-time' in log_turn['input'] else -1				intput_end_time = log_turn['input']['end-time'] if 'end-time' in log_turn['input'] else -1				output_start_time = log_turn['output']['start-time'] if 'start-time' in log_turn['output'] else -1				output_end_time = log_turn['output']['end-time'] if 'end-time' in log_turn['output'] else -1								#output transcription				output_trans = log_turn['output']['transcript'] if 'transcript' in log_turn['output'] else None					#input transcription				if 'transcription' in label_turn:					input_trans = label_turn['transcription']				elif 'transcript' in label_turn: #for test3					input_trans = label_turn['transcript']				else:					input_trans = ""								#output dialog acts				output_acts = log_turn['output']['dialog-acts'] if 'dialog-acts' in log_turn['output'] else None								#get correct slu label				#get the rank of correct slu				rank, correct_slu = getCorrectSLUHyp(log_turn, label_turn)								#has correct slu label				hasTrueLabel = hasCorrectSLULabel(label_turn)				correctSLULabel = getCorrectSLULabel(label_turn)								#schedule								row = []				row.append(session_id)				row.append(turn_index)				row.append(start)				row.append(n_asr_live)				row.append(n_asr_batch)				row.append(n_slu_live)				row.append(n_slu_batch)				row.append(output_start_time)				row.append(output_end_time)				row.append(intput_start_time)				row.append(intput_end_time)				row.append(quote(output_trans))				row.append(quote(input_trans))								row.append(quote(top_asr))				row.append(asr_score)				row.append(quote(strslu(top_slu)))				row.append(quote(strslu(output_acts)))				row.append(top_slu_score)								row.append(hasTrueLabel)				row.append(quote(correctSLULabel))								row.append(rank)				row.append(quote(correct_slu))								sum.append(row)			except KeyError as e:				print str(e)				print row				exit()		header = ["session_id", "turn_index", "restart"]	header.append("# of ars_live")	header.append("# of ars_batch")	header.append("# of slu_live")	header.append("# of slu_batch")		header.append('output_start_time')	header.append('output_end_time')	header.append('intput_start_time')	header.append('intput_end_time')	header.append("output trans")	header.append("input trans")		header.append("top asr")	header.append("asr_score")		header.append("top slu")	header.append("output acts")	header.append("top slu score")		header.append("hasCorrectLabel")	header.append("CorrectLabel")		header.append("rank")	header.append("correct_slu")		fio.writeMatrix(args.logfile, sum, header)	if (__name__ == '__main__'):	main(sys.argv)	print "Done"