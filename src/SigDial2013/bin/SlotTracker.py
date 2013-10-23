import fio
import math

def getSluSlotValueDict(slu):#return to.desc=pitt
	tokens = slu.split('&')
	
	actions = {}
	for token in tokens:
		k = token.find('(')
		if k == -1: continue
		k2 = token.find(')')
		if k2 == -1: continue
		t2 = token[k+1:k2].split('=')
		if len(t2)!=2: continue
		name = t2[0]
		value= t2[1]
		
		actions[name] = value
	return actions

def getAct(slu, prefix = ""):#parse the action from the slu string
	tokens = slu.split('&')
	
	actions = []
	for token in tokens:
		k = token.find('(')
		if k == -1: continue
		
		actions.append(prefix + token[:k])
	return set(actions)

def getOutActExplConfDict(out_act):
	dict = {}
	tokens = out_act.split('&')
	for token in tokens:
		k = token.find('(')
		if k == -1: continue
		name = token[:k]
		if name != 'expl-conf': continue
		
		k2 = token.find(')')
		if k2 == -1: continue
		
		#another split
		t2 = token[k+1:k2].split(';')
		for tt in t2:
			t3 = tt.split('=')
			if len(t3)!=2: continue
			slotname = t3[0]
			value = t3[1]
			dict[slotname] = value
	return dict

def make_pair(key, value):
	return str(key) + "=" + str(value)
	
class CSlotTracker:
	def __init__(self):
		self.dict = {}
		
	def addInform(self, in_act, slu_score):
		dict = getSluSlotValueDict(in_act)
		
		for key, value in dict.items():
			p = make_pair(key,value)
			
			if p not in self.dict:
				self.dict[p] = {}
				self.dict[p]['inform'] = []
				self.dict[p]['affirm'] = []
				self.dict[p]['negate'] = []
			self.dict[p]['inform'].append(slu_score)
	
	def addAffirm(self, out_act, in_act, slu_score):
		acts = getAct(in_act)
	
		if 'affirm' not in acts: return
		
		#extract the first expl-conf from out_act
		dict = getOutActExplConfDict(out_act)
		
		for key,value in dict.items():
			p = make_pair(key,value)
			
			if p not in self.dict:
				self.dict[p] = {}
				self.dict[p]['inform'] = []
				self.dict[p]['affirm'] = []
				self.dict[p]['negate'] = []
			self.dict[p]['affirm'].append(slu_score)
	
	def addNegate(self, out_act, in_act, slu_score):
		acts = getAct(in_act)
	
		if 'negate' not in acts: return
		
		#extract the first expl-conf from out_act
		dict = getOutActExplConfDict(out_act)
		
		for key,value in dict.items():
			p = make_pair(key,value)
			
			if p not in self.dict:
				self.dict[p] = {}
				self.dict[p]['inform'] = []
				self.dict[p]['affirm'] = []
				self.dict[p]['negate'] = []
			self.dict[p]['negate'].append(slu_score)

	def getMax(self, out_act, in_act):
		p = self.getKey(out_act, in_act)
		
		if p==None: return 0
		
		max = 0
		for s in self.dict[p]['inform']:
			if s > max:
				max = s
		return max
	
	def getKey(self, out_act, in_act):
		acts = getAct(in_act)
		if 'affirm' in acts or 'negate' in acts:
			dict = getOutActExplConfDict(out_act)
		else:
			dict = getSluSlotValueDict(in_act)
		
		for key,value in dict.items():
			p = make_pair(key,value)
			if p not in self.dict: continue
			
			return p
			
		return None
	
	def getAcc(self, out_act, in_act):
		p = self.getKey(out_act, in_act)
		
		if p != None:
			acc = 0
			
			for s in self.dict[p]['inform']:
				acc = acc + s
			for s in self.dict[p]['affirm']:
				acc = acc + s
			for s in self.dict[p]['negate']:
				acc = acc - s 
			
			return acc
			
		return -100
	
	def getBin(self, list):
		bins = [0]*10
		
		for s in list:
			if s < 0 or s > 1: continue
			k = int(s*10) if s != 1 else 9
			bins[k] = bins[k] + 1
		return bins
			
	def getBins(self, out_act, in_act):
		p = self.getKey(out_act, in_act)
		if p == None:
			bins = [0]*40
			return bins
		
		max = self.getMax(out_act, in_act)
		maxBins = self.getBin([max])
		informBins = self.getBin(self.dict[p]['inform'])
		affirmBins = self.getBin(self.dict[p]['affirm'])
		negateBins = self.getBin(self.dict[p]['negate'])
		
		bins = informBins + affirmBins + negateBins + maxBins
		
		return bins
	
if (__name__ == '__main__'):
	tracker = CSlotTracker()

	bins = tracker.getBin([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
	fio.PrintListwithName(bins, '0.15')
	
	bins = tracker.getBin([0.3])
	fio.PrintListwithName(bins, '0.3')
	
	bins = tracker.getBin([0.9])
	fio.PrintListwithName(bins, '0.9')
	
	bins = tracker.getBin([1])
	fio.PrintListwithName(bins, '1')	