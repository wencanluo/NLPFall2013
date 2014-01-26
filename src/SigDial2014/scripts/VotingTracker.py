import  argparse, dataset_walker, json, time, copy, math
from collections import defaultdict

from baseline import *
import fio
import getSlotValues

import CombineNBest

def main():
	goal_names = ['area', 'food', 'name', 'pricerange']
	
	for goal in goal_names:
		for data in ['dstc2_train','dstc2_dev', 'dstc2_test']:
			voting = []
			
			lines = []
			for method in ['baseline_focus', 'HWUbaseline', 'nbest_goals']:
				file = 'res/'+method+'_'+data+'_track.json.'+goal+'.label'
				head, body = fio.readMatrix(file, True)
				lines.append(body)
				N = len(body)
			
			for body in lines:
				assert(len(body) == N)
			
			for i in range(N):
				mat = []
				for body in lines:
					mat.append(body[i])
				voting.append(CombineNBest.getNbest(mat))
				
			fio.writeMatrix('res/'+data+'_voting'+'.'+goal+'.label', voting, head)
				
if __name__ == '__main__':
	main()
