import  argparse, dataset_walker, json, time, copy
from collections import defaultdict

from baseline import *
import fio

request_slotnames = ['area', 'food', 'name', 'pricerange', 'addr', 'phone', 'postcode', 'signature']

def GetSlot(slu_hyps, goal):
	for score, uact in slu_hyps:
		for act in uact:
			for slot in act['slots']:
				if goal == slot[0]:
					return slot[1]
	return None

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
	
	args = parser.parse_args()
	
	head, body = fio.readMatrix(args.labelfile, True)
	labels = [item[1] for item in body]
	
	if args.methodfile != None:
		head, body = fio.readMatrix(args.methodfile, True)
		method_labels = [item[1] for item in body]
	
	if args.requestfile != None:
		request_labels = fio.MulanOutReader(args.requestfile)
	
	if args.goal_area != None and args.goal_food != None and args.goal_name != None and args.goal_pricerange != None:
		head, body = fio.readMatrix(args.goal_area, True)
		goal_area_labels = [item[0] for item in body]
		
		head, body = fio.readMatrix(args.goal_food, True)
		goal_food_labels = [item[1] for item in body]
		
		head, body = fio.readMatrix(args.goal_name, True)
		goal_name_labels = [item[1] for item in body]
		
		head, body = fio.readMatrix(args.goal_pricerange, True)
		goal_pricerange_labels = [item[0.l.8y8u] for item in body]
		 
	dataset = dataset_walker.dataset_walker(args.dataset, dataroot=args.dataroot)
	track_file = open(args.trackfile, "wb")
	track = {"sessions":[]}
	track["dataset"]  = args.dataset
	start_time = time.time()

	turn_count = -1
	
	tracker = Tracker()
	
	for call in dataset :
		this_session = {"session-id":call.log["session-id"], "turns":[]}
		tracker.reset()
		for turn, _ in call :
			turn_count = turn_count + 1
			
			rank = labels[turn_count]
			method = method_labels[turn_count] if args.methodfile != None else None
			requests = request_labels[turn_count] if args.requestfile != None else None
			goals = None
			if args.goal_area != None and args.goal_food != None and args.goal_name != None and args.goal_pricerange != None:
				goals = {}
				goals['area'] = 'No' if goal_area_labels[turn_count]== 'area.No' else goal_area_labels[turn_count][len('area.Yes.'):]
				goals['food'] = goal_food_labels[turn_count][len('food.'):]
				if goals['food'] == 'Yes.dontcare':
					goals['food'] = 'dontcare'
				goals['name'] = goal_name_labels[turn_count][len('name.'):]
				if goals['name'] == 'Yes.dontcare':
					goals['name'] = 'dontcare'
					
				goals['pricerange'] = 'No' if goal_pricerange_labels[turn_count]== 'pricerange.No' else goal_pricerange_labels[turn_count][len('pricerange.Yes.'):]
			
			tracker_turn = tracker.addTurn(turn, rank, method, requests, goals)
			this_session["turns"].append(tracker_turn)
		
		track["sessions"].append(this_session)
	end_time = time.time()
	elapsed_time = end_time - start_time
	track["wall-time"] = elapsed_time
   
	json.dump(track, track_file,indent=4)
	
if __name__ == '__main__':
	main()
