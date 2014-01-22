import  argparse, dataset_walker, json, time, copy, math
from collections import defaultdict

from baseline import *
import fio
import getSlotValues

def getNbest(mat, topK = 5):
	res = []
	
	m = len(mat)
	n = len(mat[0])
	
	for i in range(n):
		dict = {}
		for j in range(m):
			if j > topK: continue
			v = mat[j][i]
			if v not in dict: 
				dict[v] = 0
			dict[v] = dict[v] + 1
		
		keys = sorted(dict, key=dict.get, reverse = True)
		if len(keys) > 0:
			res.append(keys[0])
	return res
	
def main():
	parser = argparse.ArgumentParser(description='Simple hand-crafted dialog state tracker baseline.')
	
	parser.add_argument('--dataset', dest='dataset', action='store', metavar='DATASET', required=True,
						help='The dataset to analyze')
	parser.add_argument('--dataroot',dest='dataroot',action='store',required=True,metavar='PATH',
						help='Will look for corpus in <destroot>/<dataset>/...')
	
	parser.add_argument('--goal_area',dest='goal_area',action='store',required=False,metavar='TXT',
						help='File with goal_area prediction results')
	parser.add_argument('--goal_food',dest='goal_food',action='store',required=False,metavar='TXT',
						help='File with goal_food prediction results')
	parser.add_argument('--goal_name',dest='goal_name',action='store',required=False,metavar='TXT',
						help='File with goal_name prediction results')
	parser.add_argument('--goal_pricerange',dest='goal_pricerange',action='store',required=False,metavar='TXT',
						help='File with goal_pricerange prediction results')
	
	args = parser.parse_args()
	
	for goal in [args.goal_area, args.goal_food, args.goal_name, args.goal_pricerange]:
		if goal == None: continue
		
		head, body = fio.readMatrix(goal, True)
		
		dataset = dataset_walker.dataset_walker(args.dataset, dataroot=args.dataroot)
		
		turn_count = -1
		nbest_count = 0
		
		nbest = []
		
		for call in dataset :
			for turn, _ in call :
				turn_count = turn_count + 1
				
				n_asr_live = len(turn['input']['live']['asr-hyps'])
				
				combinedgoals = getNbest(body[nbest_count:nbest_count + n_asr_live][:])
				nbest.append(combinedgoals)
				nbest_count = nbest_count + n_asr_live
		
		fio.writeMatrix(goal+".combine", nbest, head)
		
if __name__ == '__main__':
	main()
