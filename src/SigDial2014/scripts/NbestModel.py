import  argparse, dataset_walker, json, time, copy, math
from collections import defaultdict

from baseline import *
import fio
import getSlotValues

request_slotnames = ['area', 'food', 'name', 'pricerange', 'addr', 'phone', 'postcode', 'signature']

priors = getSlotValues.getPrior()

def GetSlot(slu_hyps, goal):
	for score, uact in slu_hyps:
		for act in uact:
			for slot in act['slots']:
				if goal == slot[0]:
					return slot[1]
	return None

def getGoal1(goals_label, goal_stats, score, slu_hyps):#only one option
	for goal in goals_label:
		if goals_label[goal] == 'No': continue
		
		if goal == "area" or goal == 'pricerange':
			value = goals_label[goal]
			goal_stats[goal][value] = score
		else:#for food and name
			#find the first non-empty slot-value
			if goals_label[goal] == 'dontcare':
				value = 'dontcare'
			else:
				value = GetSlot(slu_hyps, goal)
			if value != None:
				goal_stats[goal][value] = score

def getGoalTop1(goals_labels, goal_stats, score, slu_hyps, turn = None):#only one option
	goals_label = goals_labels[0]
	for goal in goals_label:
		if goals_label[goal] == 'No': continue
		
		if goal == "area" or goal == 'pricerange':
			value = goals_label[goal]
			goal_stats[goal][value] = score
		else:#for food and name
			#find the first non-empty slot-value
			if goals_label[goal] == 'dontcare':
				value = 'dontcare'
			else:
				value = GetSlot(slu_hyps, goal)
			if value != None:
				goal_stats[goal][value] = score

def getGoalMajorityVoting(goals_labels, goal_stats, score, slu_hyps, turn = None, weighted = False):#majority voting
	scores = []
	for asr in turn['input']['live']['asr-hyps']:
		scores.append(asr['score'])
		
	assert(len(scores) == len(goals_labels))
	
	dict = {}
	for i, goals_label in enumerate(goals_labels):
		if i>5: continue
		
		if weighted:
			score = math.exp(scores[i])
		
		for goal in goals_label:
			if goals_label[goal] == 'No': 
				value = 'No'
			else:
				if goal == "area" or goal == 'pricerange':
					value = goals_label[goal]
					goal_stats[goal][value] = score
				else:#for food and name
					#find the first non-empty slot-value
					if goals_label[goal] == 'dontcare':
						value = 'dontcare'
					else:
						value = GetSlot(slu_hyps, goal)
					if value != None:
						goal_stats[goal][value] = score
			if goal not in dict:
				dict[goal] = defaultdict(float)
			dict[goal][value] = dict[goal][value] + score
	
	goals_label = {}
	for goal in dict:
		d = dict[goal]
		keys = sorted(d, key = d.get, reverse = True)
		if len(keys) > 0:
			goals_label[goal] = keys[0]
		
	for goal in goals_label:
		score = 1.0
		if goals_label[goal] == 'No': continue
		
		if goal == "area" or goal == 'pricerange':
			value = goals_label[goal]
			goal_stats[goal][value] = score
		else:#for food and name
			#find the first non-empty slot-value
			if goals_label[goal] == 'dontcare':
				value = 'dontcare'
			else:
				value = GetSlot(slu_hyps, goal)
			if value != None:
				goal_stats[goal][value] = score

def getGoalBayes(goals_labels, goal_stats, score, slu_hyps, turn = None, weighted = True):#majority voting
	scores = []
	for asr in turn['input']['live']['asr-hyps']:
		scores.append(asr['score'])
		
	assert(len(scores) == len(goals_labels))
	
	dict = {}
	for i, goals_label in enumerate(goals_labels):
		if weighted:
			score = math.exp(scores[i])
		
		for goal in goals_label:
			p = 1.0
			
			if goals_label[goal] == 'No': 
				value = 'No'
				p = priors[goal][value]
			else:
				if goal == "area" or goal == 'pricerange':
					value = goals_label[goal]
					goal_stats[goal][value] = score
					p = priors[goal][value]
				else:#for food and name
					#find the first non-empty slot-value
					if goals_label[goal] == 'dontcare':
						value = 'dontcare'
						p = priors[goal][value]
					else:
						value = GetSlot(slu_hyps, goal)
					if value != None:
						goal_stats[goal][value] = score
						p = priors[goal]['Yes']
			if goal not in dict:
				dict[goal] = defaultdict(float)
			dict[goal][value] = dict[goal][value] + score*p
	
	goals_label = {}
	for goal in dict:
		d = dict[goal]
		keys = sorted(d, key = d.get, reverse = True)
		if len(keys) > 0:
			goals_label[goal] = keys[0]
		
	for goal in goals_label:
		score = 1.0
		if goals_label[goal] == 'No': continue
		
		if goal == "area" or goal == 'pricerange':
			value = goals_label[goal]
			goal_stats[goal][value] = score
		else:#for food and name
			#find the first non-empty slot-value
			if goals_label[goal] == 'dontcare':
				value = 'dontcare'
			else:
				value = GetSlot(slu_hyps, goal)
			if value != None:
				goal_stats[goal][value] = score
														
class Tracker(object):
	def __init__(self):
		self.reset()

	def addTurn(self, turn, rank = 0, method_label = None, request_label = None, goals_label = None):
		hyps = copy.deepcopy(self.hyps)
		if "dialog-acts" in turn["output"] :
			mact = turn["output"]["dialog-acts"]
		else :
			mact = []
		
		# clear requested-slots that have been informed
		for act in mact:
			if act["act"] == "inform" :
				for slot,value in act["slots"]:
					if slot in hyps["requested-slots"] :
						hyps["requested-slots"][slot] = 0.0
		
		slu_hyps = Uacts(turn)
		
		requested_slot_stats = defaultdict(float)
		method_stats = defaultdict(float)
		goal_stats = defaultdict(lambda : defaultdict(float))
		prev_method = "none"
		
		if len(hyps["method-label"].keys())> 0 :
			prev_method = hyps["method-label"].keys()[0]
		
		#consider only the first one if it is predited as True
		#for score, uact in slu_hyps :
		if rank == '0':
			score, uact = slu_hyps[0]
		else:# '-1'
			uact = []
		
		if True:
			score = 1.0
			
			informed_goals, denied_goals, requested, method = labels(uact, mact)
			# requested	
			
			if request_label == None:
				for slot in requested:
					requested_slot_stats[slot] += score
			else:
				for i in range(len(request_slotnames)):
					slot = request_slotnames[i]
					if request_label[i] == 1:
						requested_slot_stats[slot] += score
					else:
						if slot in hyps["requested-slots"]:
							del hyps["requested-slots"][slot]
						
						if slot in requested_slot_stats:
							del requested_slot_stats[slot]
			
			if method == "none" :
				method = prev_method
			
			if method_label == None:
				method_stats[method] = score
			else:
				if method_label == "none":
					method_stats[prev_method] = score
				else:
					method_stats[method_label] = score
			
			# goal_labels
			if goals_label == None:
				for slot in informed_goals:
					value = informed_goals[slot]
					goal_stats[slot][value] += score
			else:
				#get the top one
				#getGoal1(goals_label, goal_stats, score, slu_hyps)
				#getGoalTop1(goals_label, goal_stats, score, slu_hyps)
				#getGoalMajorityVoting(goals_label, goal_stats, score, slu_hyps, turn)
				#getGoalMajorityVoting(goals_label, goal_stats, score, slu_hyps, turn, True)
				getGoalBayes(goals_label, goal_stats, score, slu_hyps, turn)
				
		# pick top values for each slot
		for slot in goal_stats:
			curr_score = 0.0
			if (slot in hyps["goal-labels"]) :
				curr_score = hyps["goal-labels"][slot].values()[0]
			for value in goal_stats[slot]:
				score = goal_stats[slot][value]
				if score >= curr_score :
					hyps["goal-labels"][slot] = {
							value:clip(score)
						}
					curr_score = score
					
		# joint estimate is the above selection, with geometric mean score
		goal_joint_label = {"slots":{}, "scores":[]}
		for slot in  hyps["goal-labels"] :
			(value,score), = hyps["goal-labels"][slot].items()
			if score < 0.5 :
				# then None is more likely
				continue
			goal_joint_label["scores"].append(score)
			goal_joint_label["slots"][slot]= value
			
		if len(goal_joint_label["slots"]) > 0 :
			geom_mean = 1.0
			for score in goal_joint_label["scores"] :
				geom_mean *= score
			geom_mean = geom_mean**(1.0/len(goal_joint_label["scores"]))
			goal_joint_label["score"] = clip(geom_mean)
			del goal_joint_label["scores"]
			
			hyps["goal-labels-joint"] = [goal_joint_label]
		
		for slot in requested_slot_stats :
			hyps["requested-slots"][slot] = clip(requested_slot_stats[slot])
			
		# normalise method_stats	
		hyps["method-label"] = normalise_dict(method_stats)
		self.hyps = hyps 
		return self.hyps
	
	def reset(self):
		self.hyps = {"goal-labels":{}, "goal-labels-joint":[], "requested-slots":{}, "method-label":{}}
	

def main():
	parser = argparse.ArgumentParser(description='Simple hand-crafted dialog state tracker baseline.')
	parser.add_argument('--dataset', dest='dataset', action='store', metavar='DATASET', required=True,
						help='The dataset to analyze')
	parser.add_argument('--dataroot',dest='dataroot',action='store',required=True,metavar='PATH',
						help='Will look for corpus in <destroot>/<dataset>/...')
	parser.add_argument('--trackfile',dest='trackfile',action='store',required=True,metavar='JSON_FILE',
						help='File to write with tracker output')
	parser.add_argument('--labelfile',dest='labelfile',action='store',required=True,metavar='TXT',
						help='File with 2-way prediction results')
	parser.add_argument('--methodfile',dest='methodfile',action='store',required=False,metavar='TXT',
						help='File with method prediction results')
	parser.add_argument('--requestfile',dest='requestfile',action='store',required=False,metavar='TXT',
						help='File with request prediction results')
	parser.add_argument('--goal_area',dest='goal_area',action='store',required=False,metavar='TXT',
						help='File with goal_area prediction results')
	parser.add_argument('--goal_food',dest='goal_food',action='store',required=False,metavar='TXT',
						help='File with goal_food prediction results')
	parser.add_argument('--goal_name',dest='goal_name',action='store',required=False,metavar='TXT',
						help='File with goal_name prediction results')
	parser.add_argument('--goal_pricerange',dest='goal_pricerange',action='store',required=False,metavar='TXT',
						help='File with goal_pricerange prediction results')
	parser.add_argument('--topK',dest='topK',action='store',type=int, help='get topK accuracy')
	
	args = parser.parse_args()
	
	global topK
	topK = args.topK
	
	head, body = fio.readMatrix(args.labelfile, True)
	labels = [item[1] for item in body]
	
	if args.methodfile != None:
		head, body = fio.readMatrix(args.methodfile, True)
		method_labels = [item[1] for item in body]
	
	if args.requestfile != None:
		request_labels = fio.MulanOutReader(args.requestfile)
	
	if args.goal_area != None and args.goal_food != None and args.goal_name != None and args.goal_pricerange != None:
		head, body = fio.readMatrix(args.goal_area, True)
		goal_area_labels = [item[1] for item in body]
		
		head, body = fio.readMatrix(args.goal_food, True)
		goal_food_labels = [item[1] for item in body]
		
		head, body = fio.readMatrix(args.goal_name, True)
		goal_name_labels = [item[1] for item in body]
		
		head, body = fio.readMatrix(args.goal_pricerange, True)
		goal_pricerange_labels = [item[1] for item in body]
		 
	dataset = dataset_walker.dataset_walker(args.dataset, dataroot=args.dataroot)
	track_file = open(args.trackfile, "wb")
	track = {"sessions":[]}
	track["dataset"]  = args.dataset
	start_time = time.time()

	turn_count = -1
	nbest_count = 0
	tracker = Tracker()
	
	for call in dataset :
		this_session = {"session-id":call.log["session-id"], "turns":[]}
		tracker.reset()
		for turn, _ in call :
			turn_count = turn_count + 1
			
			n_asr_live = len(turn['input']['live']['asr-hyps'])
			
			rank = labels[turn_count]
			method = method_labels[turn_count] if args.methodfile != None else None
			requests = request_labels[turn_count] if args.requestfile != None else None
			
			nbestGoals = []
			for k in range(nbest_count, nbest_count + n_asr_live):
				goals = None
				if args.goal_area != None and args.goal_food != None and args.goal_name != None and args.goal_pricerange != None:
					goals = {}
					goals['area'] = 'No' if goal_area_labels[k]== 'area.No' else goal_area_labels[k][len('area.Yes.'):]
					goals['food'] = goal_food_labels[k][len('food.'):]
					if goals['food'] == 'Yes.dontcare':
						goals['food'] = 'dontcare'
					goals['name'] = goal_name_labels[k][len('name.'):]
					if goals['name'] == 'Yes.dontcare':
						goals['name'] = 'dontcare'
						
					goals['pricerange'] = 'No' if goal_pricerange_labels[k]== 'pricerange.No' else goal_pricerange_labels[k][len('pricerange.Yes.'):]
				nbestGoals.append(goals)
			
			nbest_count = nbest_count + n_asr_live
			tracker_turn = tracker.addTurn(turn, rank, method, requests, nbestGoals)
			this_session["turns"].append(tracker_turn)
		
		track["sessions"].append(this_session)
	end_time = time.time()
	elapsed_time = end_time - start_time
	track["wall-time"] = elapsed_time
   
	json.dump(track, track_file,indent=4)
	
if __name__ == '__main__':
	main()
