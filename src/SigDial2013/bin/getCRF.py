'''
Created on Sep 30, 2013

@author: wencan
'''
import fio
from getWekaArff import *
	
def getCRF_Act(featurefile, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+featurefile+".dict")
	
	for test in tests:
		data = []
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		turn_index = head.index('turn_index')
		rank_index = head.index('rank')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		
		for row in body:
			rank = int( row[rank_index] )
			label = rank if rank <= 1 else -1
			
			turn_id = row[turn_index]
			out_act = row[out_index][1:-1]
			in_act = row[in_index][1:-1]
			
			if turn_id == '0':#add a blank line
				row = []
				data.append(row)
				
			acts = set( list(getAct(out_act)) + list(getAct(in_act)))
			
			row = []
			
			for key in features.keys():
				if key in acts:
					row.append(1)
				else:
					row.append(0)
	
			row.append(label)
			data.append(row)
		
		data = data[1:]
		fio.CRFWriter("res/"+test+"_act.crf", data)

def getCRF_ActNgram(acts, unigrams, tests):
	#features = fio.LoadDict("res/train1a.dict")
	features = fio.LoadDict("res/"+acts+".dict")
	unigram = [' ' + word.strip() + ' ' for word in fio.readfile('res/' + unigrams + ".dict")]
	
	for test in tests:
		data = []
		
		filename = "res/"+test+"_summary.txt"
		head, body = fio.readMatrix(filename, True)
		
		turn_index = head.index('turn_index')
		rank_index = head.index('rank')
		out_index = head.index('output acts')
		in_index = head.index('top slu')
		asr_index = head.index('top asr')
		
		for row in body:
			rank = int( row[rank_index] )
			label = rank if rank <= 1 else -1
			
			turn_id = row[turn_index]
			out_act = row[out_index][1:-1]
			in_act = row[in_index][1:-1]
			asr = row[asr_index][1:-1]
			
			if turn_id == '0':#add a blank line
				row = []
				data.append(row)
				
			acts = set( list(getAct(out_act)) + list(getAct(in_act)))
			
			row = []
			
			for key in features.keys():
				if key in acts:
					row.append(1)
				else:
					row.append(0)
			
			asr = ' ' + asr + ' '
			for word in unigram:
				if asr.find(word) != -1:
					row.append(1)
				else:
					row.append(0)
	
			row.append(label)
			data.append(row)
		
		data = data[1:]
		fio.CRFWriter("res/"+test+"_actngram.crf", data)
			
def getCRF_Label(tests):
	for test in tests:
		out = "res/"+test+".out"
		header, body = fio.CRFReader(out)
		fio.writeMatrix("res/"+test+"_crf.label", body, header)
	
if (__name__ == '__main__'):
	#getCRF_Act("train2", ["train2", "test1", "test2", "test3", "test4"])
	#getCRF_ActNgram("train2", 'unigram', ["train2", "test1", "test2", "test3", "test4"])
	#getWekaARFF_Enrich("train2", ["train2", "test1", "test2", "test3", "test4"])
	getCRF_Label(["test1", "test2", "test3", "test4"])
	#getCRF_Label(["test1_actngram", "test2_actngram", "test3_actngram", "test4_actngram"])
	print "Done"