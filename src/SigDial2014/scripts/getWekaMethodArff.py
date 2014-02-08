'''
Created on Sep 30, 2013

@author: wencan
'''
import fio
import Cosin
from SlotTracker import *
import getWekaArff

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
		method_index = head.index('method_label')
		
		for row in body:
			rank = int( row[rank_index] )
			method = row[method_index][1:-1]
			#label = rank if rank == 0 else -1
			label = method
			
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
		fio.ArffWriter("res/"+test+"_method_act.arff", header, types, "dstc", data)	
		fio.writeMatrix('res/' + test + "_method_act.body", data, header)
	
def getWekaARFF_Ngram(tests):
	for test in tests:
		data = []
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		rank_index = head.index('rank')
		asr_index = head.index('top asr')
		
		method_index = head.index('method_label')
		
		for row in body:
			rank = int( row[rank_index] )
			method = row[method_index][1:-1]
			#label = rank if rank == 0 else -1
			label = method
			
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
		
		fio.ArffWriter("res/"+test+"_method_ngram.arff", header, types, "dstc", data)	
		
def getWekaARFF_ActNgram(featurefile, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+".dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		data = []
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		turn_index= head.index('turn_index')
		rank_index = head.index('rank')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		asr_index = head.index('top asr')
		
		method_index = head.index('method_label')
		
		for i,row in enumerate(body):
			rank = int( row[rank_index] )
			method = row[method_index][1:-1]
			
			#label = rank if rank == 0 else -1
			label = method
			turn_id = row[turn_index]
			plabel = body[i-1][method_index][1:-1] if turn_id >= 1 else 'none'
			
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
					
			#row.append()
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
		fio.ArffWriter("res/"+test+"_method_actngram.arff", header, types, "dstc", data)
		
		#return header, types, data
def getWekaARFF_ActNgramTopline(featurefile, tests):
	features = fio.LoadDict("res/"+featurefile+".dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		data = []
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		turn_index= head.index('turn_index')
		rank_index = head.index('rank')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		asr_index = head.index('top asr')
		
		method_index = head.index('method_label')
		
		for i, row in enumerate(body):
			rank = int( row[rank_index] )
			method = row[method_index][1:-1]
			
			#label = rank if rank == 0 else -1
			label = method
			turn_id = int(row[turn_index])
			plabel = body[i-1][method_index][1:-1] if turn_id >= 1 else 'none'
			
			firstTurn = False if turn_id >= 1 else True
			
			out_act = row[out_index][1:-1]
			in_act = row[in_index][1:-1]
			asr = row[asr_index][1:-1]
			
			acts = set( list(getAct(out_act)) + list(getAct(in_act)))
			
			row = []
			
			row.append(asr)
			row.append(firstTurn)
			
			for key in features.keys():
				if key in acts:
					row.append(1)
				else:
					row.append(0)
					
			row.append(plabel)
			row.append(label)
			data.append(row)
		
		header =[]
		header.append("ASR")
		header.append('firstTurn')
		for key in features.keys():
			header.append(key)
		header = header + ['PreviousTag']
		header = header + ['@@Class@@']
		
		types = []
		types.append("String")
		types = types + ['Category']
		for key in features.keys():
			types.append('Category')
		types = types + ['Category']
		types = types + ['Category']
		fio.ArffWriter("res/"+test+"_method_actngram_topline.arff", header, types, "dstc", data)

def getWekaARFF_ActNgramRecovery(featurefile, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+".dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		data = []
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		turn_index= head.index('turn_index')
		rank_index = head.index('rank')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		asr_index = head.index('top asr')
		
		method_index = head.index('recovery_method')
		
		for i,row in enumerate(body):
			rank = int( row[rank_index] )
			method = row[method_index][1:-1]
			
			#label = rank if rank == 0 else -1
			label = method
			turn_id = row[turn_index]
			plabel = body[i-1][method_index][1:-1] if turn_id >= 1 else 'none'
			
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
					
			#row.append()
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
		fio.ArffWriter("res/"+test+"_method_actngram_mindchange.arff", header, types, "dstc", data)
		
def getWekaARFF_ActwithNameNgramRecovery(featurefile, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+"_name.dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		data = []
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		turn_index= head.index('turn_index')
		rank_index = head.index('rank')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		asr_index = head.index('top asr')
		
		method_index = head.index('recovery_method')
		
		for i,row in enumerate(body):
			rank = int( row[rank_index] )
			method = row[method_index][1:-1]
			
			#label = rank if rank == 0 else -1
			label = method
			turn_id = row[turn_index]
			plabel = body[i-1][method_index][1:-1] if turn_id >= 1 else 'none'
			
			out_act = row[out_index][1:-1]
			in_act = row[in_index][1:-1]
			asr = row[asr_index][1:-1]
			
			acts = set( list(getAct(out_act, "out_", True)) + list(getAct(in_act, "in_", True)))
			
			row = []
			
			row.append(asr)
			
			for key in features.keys():
				if key in acts:
					row.append(1)
				else:
					row.append(0)
					
			#row.append()
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
		fio.ArffWriter("res/"+test+"_method_actwithNamengram_mindchange_all.arff", header, types, "dstc", data)

def getWekaARFF_ASRs_NgramRecovery(featurefile, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+"_name.dict")
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		data = []
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		turn_index= head.index('turn_index')
		rank_index = head.index('rank')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		#asr_index = head.index('top asr')
		asr_index = head.index('ASRs')
		asr_score_index = head.index('ASR_Scores')
		sr_id_index = head.index('sr_id')
		
		method_index = head.index('recovery_method')
		
		for i,row in enumerate(body):
			rank = int( row[rank_index] )
			method = row[method_index][1:-1]
			
			#label = rank if rank == 0 else -1
			label = method
			turn_id = row[turn_index]
			plabel = body[i-1][method_index][1:-1] if turn_id >= 1 else 'none'
			
			out_act = row[out_index][1:-1]
			in_act = row[in_index][1:-1]
			#asr = row[asr_index][1:-1]
			ASRs = row[asr_index][1:-1].split('#')
			ASR_Scores = row[asr_score_index][1:-1].split('#')
			
			acts = set( list(getAct(out_act, "out_", True)) + list(getAct(in_act, "in_", True)))
			sr_id = row[sr_id_index]
			
			for i,asr in enumerate(ASRs):
				row = []
				#if i>0: continue
				
				row.append(asr)
				row.append(float(ASR_Scores[i]))
				row.append(sr_id)
				
				for key in features.keys():
					if key in acts:
						row.append(1)
					else:
						row.append(0)
						
				#row.append()
				row.append(label)
				data.append(row)
		
		header =[]
		header.append("ASR")
		header.append("ASR_Score")
		header.append("SR_ID")
		
		for key in features.keys():
			header.append(key)
		header = header + ['@@Class@@']
		
		types = []
		types.append("String")
		types = types + ['Continuous']
		types.append('Category')
		for key in features.keys():
			types.append('Category')
		types = types + ['Category']
		fio.ArffWriter("res/"+test+"_method_asr_act_score_mindchange_all.arff", header, types, "dstc", data)
									
if (__name__ == '__main__'):
	#getWekaArff.getActList(["dstc2_train"], "dstc2_train", True)
	#getWekaARFF_Act("dstc2_train", ["dstc2_train", "dstc2_dev"])
	#getWekaARFF_Act("train3", ["train3", "test3"])
	#getWekaARFF_Ngram(["train2", "test1", "test2", "test3", "test4"])
	#getWekaARFF_Enrich("train2", ["test1"])
	#getWekaARFF_Enrich("train2", ["train2", "test1", "test2", "test3", "test4"])
	#getWekaARFF_Enrich("train3", ["train3", "test3"])
	#getWekaARFF_Enrich("train2", ["train2", "test1", "test2", "test3", "test4"])
	#getWekaARFF_Enrich("train3", ["train3", "test1", "test2", "test3", "test4"])
	#getWekaARFF_Enrich("train23", ["train2", "train3", "test1", "test2", "test3", "test4"])
	#getWekaARFF_Bin("train3", ["train3", "test3"])
	
	#getWekaARFF_Enrich("train2", ["test1"])
	#getWekaARFF_ActNgram("dstc2_train", ["dstc2_train", "dstc2_dev"])
	#getWekaARFF_ActNgramTopline("dstc2_train", ["dstc2_train", "dstc2_dev"])
	#getWekaARFF_ActNgramRecovery("dstc2_train", ["dstc2_train", "dstc2_dev"])
	getWekaARFF_ASRs_NgramRecovery("dstc2_train", ["dstc2_train", "dstc2_dev"])
	getWekaARFF_ASRs_NgramRecovery("dstc2_traindev", ["dstc2_traindev", "dstc2_test"])
	print "Done"