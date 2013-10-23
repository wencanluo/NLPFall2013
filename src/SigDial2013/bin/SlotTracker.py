from getWekaArff import getOutActExplConfDict, getAct, getSluSlotValueDict

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

	def getMax(self):
		pass
	
	def getAcc(self, out_act, in_act):
		acts = getAct(in_act)
		if 'affirm' in acts or 'negate' in acts:
			dict = getOutActExplConfDict(out_act)
		else:
			dict = getSluSlotValueDict(in_act)
			
		for key,value in dict.items():
			p = make_pair(key,value)
			if p not in self.dict: continue
			
			acc = 0
			
			break
			
		return acc
	def getBins(self, out_act, in_act):
		pass