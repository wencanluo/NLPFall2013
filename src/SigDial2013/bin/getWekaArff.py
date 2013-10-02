'''
Created on Sep 30, 2013

@author: wencan
'''
import fio

def getActList():
	tests = ['train1a']
	
	dict = {}
	
	for test in tests:
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
	
	fio.SaveDict(dict, "res/train1a.dict")

def getAct(slu):#parse the action from the slu string
	tokens = slu.split('&')
	
	actions = []
	for token in tokens:
		k = token.find('(')
		if k == -1: continue
		
		actions.append(token[:k])
	return set(actions)
	
def getWekaTrain():
	features = fio.LoadDict("res/train1a.dict")
	
	tests = ['train1a', 'test1', 'test2', 'test3', 'test4']
	
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
	
if (__name__ == '__main__'):
	#getActList()
	getWekaTrain()
	print "Done"