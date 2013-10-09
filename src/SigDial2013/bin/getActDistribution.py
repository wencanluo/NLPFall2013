'''
Created on 10/08/2013

@author: wencan
'''
import fio

def getActDict(test):
	dict = {}

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
	
	return dict

def getAct(slu):#parse the action from the slu string
	tokens = slu.split('&')
	
	actions = []
	for token in tokens:
		k = token.find('(')
		if k == -1: continue
		
		actions.append(token[:k])
	return set(actions)
	
def getActDistribution():
	tests = ['test1', 'test2', 'test3', 'test4', 'train1a', 'train2', 'train3']
	
	acts = []
	for test in tests:
		acts.append( getActDict(test) )
	
	keys = []
	for dict in acts:
		keys = keys + dict.keys()
	keys = sorted(set(keys))
	
	data = []
	for key in keys:
		row = []
		row.append(key)
		
		for dict in acts:
			value = dict[key] if key in dict else 0
			row.append(value)
		data.append(row)
	
	header = ['act'] + tests
	fio.writeMatrix('res/acts.txt', data, header)
	
if (__name__ == '__main__'):
	getActDistribution()
	print "Done"