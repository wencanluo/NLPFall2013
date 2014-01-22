import  argparse, dataset_walker, json, time, copy
from collections import defaultdict

from baseline import *
import fio
import getSummary

topK = 0

class ToplineTracker(object):
	def __init__(self):
		self.reset()

	def addTurn(self, turn, label_turn = None):
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
						del hyps["requested-slots"][slot]
						#hyps["requested-slots"][slot] = 0.0
		
		slu_hyps = Uacts(turn)
		
		requested_slot_stats = defaultdict(float)
		method_stats = defaultdict(float)
		goal_stats = defaultdict(lambda : defaultdict(float))
		prev_method = "none"
		
		if len(hyps["method-label"].keys())> 0 :
			prev_method = hyps["method-label"].keys()[0]
		
		# Topline1: If the correct one appears in one of the SLU, add it to the output; if it doesn't appear, ignore it.
		goal_label, method_label, request_label = getSummary.getLabels(label_turn)
		
		global topK
		
		count = 0
		for score, uact in slu_hyps:
			if count > topK: continue
			
			count = count + 1
			informed_goals, denied_goals, requested, method = labels(uact, mact)
			
			score = 1.0
			# requested	
			for r in request_label:
				for slot in requested:
					if slot != r: continue
					requested_slot_stats[slot] = score
			
			if method == "none" :
				method = prev_method
			
			#if method != "none":
			if method == method_label:
				method_stats[method] = score
			
			# goal_labels
			#for slot in informed_goals:
			for k, v in goal_label.items():
				if k not in informed_goals: continue
				if informed_goals[k] != v: continue
				
				goal_stats[k][v] = score
				
		if len(method_stats) == 0:
			method_stats[prev_method] = score
		
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
			sc = clip(requested_slot_stats[slot])
			if sc == 0: continue
			hyps["requested-slots"][slot] = sc
			
		# normalise method_stats	
		hyps["method-label"] = normalise_dict(method_stats)
		self.hyps = hyps 
		return self.hyps
	
	def reset(self):
		self.hyps = {"goal-labels":{}, "goal-labels-joint":[], "requested-slots":{}, "method-label":{}}
	

def findASRGoals(turn, goals):
	if goals == None:
		return False
	
	for k, v in goals.items():
		if findASR(turn, v):
			return True
	return False
	
def findASR(turn, v):
	for asr in turn['input']['live']['asr-hyps']:
		hyp = asr['asr-hyp']
		
		hyp = " " + hyp + " "
		v = " " + v + " "
		
		if hyp.find(v) != -1:
			return True
	return False

def findTranscriptionGoals(turn, goals):
	if goals == None:
		return False
	
	for k, v in goals.items():
		if findTranscription(turn, v):
			return True
	return False
	
def findTranscription(label_turn, v):
	if v == None:
		return False
	
	if 'transcription' in label_turn:
		input_trans = label_turn['transcription']
	elif 'transcript' in label_turn: #for test3
		input_trans = label_turn['transcript']
	else:
		input_trans = ""
	
	input_trans = " " + input_trans + " "
	v = " " + v + " "
	
	if input_trans.find(v) != -1:
		return True

def findSLUGoals(turn, goals):
	if goals == None:
		return False
	
	if "dialog-acts" in turn["output"] :
		mact = turn["output"]["dialog-acts"]
	else :
		mact = []
		
	slu_hyps = Uacts(turn)
	
	for k, v in goals.items():
		for score, uact in slu_hyps:
			informed_goals, denied_goals, requested, method = labels(uact, mact)

			if k in informed_goals and informed_goals[k] == v:
				return True
	return False
	
class Topline2Tracker(object):
	def __init__(self):
		self.reset()

	def addTurn(self, turn, label_turn = None):
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
						del hyps["requested-slots"][slot]
						#hyps["requested-slots"][slot] = 0.0
		
		slu_hyps = Uacts(turn)
		
		requested_slot_stats = defaultdict(float)
		method_stats = defaultdict(float)
		goal_stats = defaultdict(lambda : defaultdict(float))
		prev_method = "none"
		
		if len(hyps["method-label"].keys())> 0 :
			prev_method = hyps["method-label"].keys()[0]
		
		# Topline2: If the correct one appears in ASR, it is correct
		goal_label, method_label, request_label = getSummary.getLabels(label_turn)
		
		global topK
		
		count = 0 
		for score, uact in slu_hyps:
			#if count > topK: continue
			
			#count = count + 1
			informed_goals, denied_goals, requested, method = labels(uact, mact)
			
			score = 1.0
			# requested	
			for r in request_label:
				for slot in requested:
					if slot != r: continue
					requested_slot_stats[slot] = score
			
			if method == "none" :
				method = prev_method
			
			#if method != "none":
			if method == method_label:
				method_stats[method] = score
			
			# goal_labels
			#for slot in informed_goals:
			for k, v in goal_label.items():
				if k in informed_goals and informed_goals[k] == v:
					goal_stats[k][v] = score
				else:
					#search v in the asr
					if findASR(turn, v):
						goal_stats[k][v] = score
				
		if len(method_stats) == 0:
			method_stats[prev_method] = score
		
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
	
class Topline3Tracker(object):
	def __init__(self):
		self.reset()

	def addTurn(self, turn, label_turn = None):
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
						del hyps["requested-slots"][slot]
						#hyps["requested-slots"][slot] = 0.0
		
		slu_hyps = Uacts(turn)
		
		requested_slot_stats = defaultdict(float)
		method_stats = defaultdict(float)
		goal_stats = defaultdict(lambda : defaultdict(float))
		prev_method = "none"
		
		if len(hyps["method-label"].keys())> 0 :
			prev_method = hyps["method-label"].keys()[0]
		
		# Topline3: If the correct one appears in Transcription, it is correct
		goal_label, method_label, request_label = getSummary.getLabels(label_turn)
		
		global topK
		
		count = 0 
		for score, uact in slu_hyps:
			#if count > topK: continue
			
			#count = count + 1
			informed_goals, denied_goals, requested, method = labels(uact, mact)
			
			score = 1.0
			# requested	
			for r in request_label:
				for slot in requested:
					if slot != r: continue
					requested_slot_stats[slot] = score
			
			if method == "none" :
				method = prev_method
			
			#if method != "none":
			if method == method_label:
				method_stats[method] = score
			
			# goal_labels
			#for slot in informed_goals:
			for k, v in goal_label.items():
				if k in informed_goals and informed_goals[k] == v:
					goal_stats[k][v] = score
				else:
					#search v in the asr
					if findTranscription(label_turn, v):
						goal_stats[k][v] = score
						print k, '=', v, '\t', "True"
					else:
						print k, '=', v, '\t', "False"
				
		if len(method_stats) == 0:
			method_stats[prev_method] = score
		
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
	
	parser.add_argument('--topK',dest='topK',action='store',type=int, help='get topK accuracy')
	
	args = parser.parse_args()
	
	global topK
	topK = args.topK
	
	dataset = dataset_walker.dataset_walker(args.dataset, dataroot=args.dataroot, labels=True)
	track_file = open(args.trackfile, "wb")
	track = {"sessions":[]}
	track["dataset"]  = args.dataset
	start_time = time.time()

	turn_count = -1
	
	tracker = Topline3Tracker()
	
	for call in dataset :
		this_session = {"session-id":call.log["session-id"], "turns":[]}
		tracker.reset()
		for turn, label_turn in call :
			turn_count = turn_count + 1
			
			tracker_turn = tracker.addTurn(turn, label_turn)
			this_session["turns"].append(tracker_turn)
		
		track["sessions"].append(this_session)
	end_time = time.time()
	elapsed_time = end_time - start_time
	track["wall-time"] = elapsed_time
   
	json.dump(track, track_file,indent=4)
	
if __name__ == '__main__':
	main()
