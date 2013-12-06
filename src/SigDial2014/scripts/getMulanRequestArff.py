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
		
def getMulanARFF_ActNgram(featurefile, tests):
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
		request_index = head.index('request_slots')
		
		labels = ['area', 'food', 'name', 'pricerange', 'addr', 'phone', 'postcode', 'signature']
		
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
			
			requests = row[request_index][1:-1].split(';')
			
			row = []
			
			row.append(asr)
			
			for key in features.keys():
				if key in acts:
					row.append(1)
				else:
					row.append(0)
					
			#row.append()
			
			for label in labels:
				if label in requests:
					row.append('1')
				else:
					row.append('0')
			
			data.append(row)
		
		header =[]
		header.append("ASR")
		for key in features.keys():
			header.append(key)
		#header = header + ['@@Class@@']
		for i in range(len(labels)):
			labels[i] = 'L' + labels[i]
		header = header + labels
		
		types = []
		types.append("String")
		for key in features.keys():
			types.append('Category')
		
		for label in labels:
			types = types + ['Category']
		#fio.ArffWriter("res/"+test+"_request_actngram.arff", header, types, "dstc", data)
		fio.MulanWriter("res/"+test+"_request_actngram", labels, header, types, "dstc", data)
							
if (__name__ == '__main__'):
	getMulanARFF_ActNgram("dstc2_train", ["dstc2_train", "dstc2_dev"])
	print "Done"