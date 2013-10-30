'''
Created on Sep 30, 2013

@author: wencan
'''
import fio
import Cosin
from SlotTracker import *
from getWekaArff import *

def getWekaSelfTrainingARFF_ActNgram(featurefile, train, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+".dict")
	
	train_header, train_types, train_data = getWekaARFFOneTest_ActNgram(featurefile, train)
	
	#tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
	for test in tests:
		data = []
		
		labelfile = "res/"+test+"_actngram.label"
		head, body = fio.readMatrix(labelfile, True)
		labels = [item[1] for item in body]
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		rank_index = head.index('rank')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		asr_index = head.index('top asr')
		
		for i, row in enumerate(body):
			rank = int( row[rank_index] )
			#label = rank if rank <= 1 else -1
			
			label = int(labels[i])
			
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
		
		data = train_data + data
		fio.ArffWriter("res/"+test+"_actngram_selftraining.arff", header, types, "dstc", data)
		
if (__name__ == '__main__'):
	#getActList(["train2", "train3"], "train23")
	#getActList(["train3"], "train3")
	#getWekaARFF_Act("train2", ["train2", "test1", "test2", "test4"])
	#getWekaARFF_Act("train3", ["train3", "test3"])
	#getWekaARFF_Ngram(["train2", "test1", "test2", "test3", "test4"])
	#getWekaARFF_Enrich("train2", ["test1"])
	#getWekaARFF_Enrich("train2", ["train2", "test1", "test2", "test3", "test4"])
	#getWekaARFF_Enrich("train3", ["train3", "test3"])
	getWekaSelfTrainingARFF_ActNgram("train2", "train2", ["test1", "test2", "test3", "test4"])
	getWekaSelfTrainingARFF_ActNgram("train3", "train3", ["test3"])
	#getWekaARFF_Bin("train3", ["train3", "test3"])
	
	#getWekaARFF_Enrich("train2", ["test1"])
	#getWekaARFF_ActNgram
	print "Done"