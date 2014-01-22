import sys,os,argparse
import fio
import json
from getSummary import *
from get2wayError import *
import SlotTracker
									
def main(argv):
	parser = argparse.ArgumentParser(description='Convert Track to Label format.')
	parser.add_argument('--summaryfile',dest='summaryfile',action='store',required=True,metavar='TXT',
						help='summary file')
	parser.add_argument('--trackfile',dest='trackfile',action='store',metavar='JSON_FILE',required=True,
						help='File containing score JSON')
	
	args = parser.parse_args()

	header, body = fio.readMatrix(args.summaryfile, True)
	#header_label, body_label = fio.readMatrix(args.labelfile, True)
	
	goal_names = ['area', 'food', 'name', 'pricerange']
	
	goal_id = header.index('recovery_goals')	
	sessions = json.load(open(args.trackfile))['sessions']
	
	tracker_output = []
	for s in sessions:
		tracker_output = tracker_output + s['turns']
	
	assert(len(body) == len(tracker_output))
	
	for goal in goal_names:
		data = []
		for i in range(len(body)):
			row = body[i]
			track_turn_1 = tracker_output[i-1] if i > 0 else None 
			track_turn = tracker_output[i]
			goals = row[goal_id][1:-1]
			
			gdict = SlotTracker.getGoalsDict(goals)
			dict = utility.sub(getGoal(track_turn), getGoal(track_turn_1))
			
			row = []
			if goal in gdict:
				if goal == 'name' or goal == 'food':
					if gdict[goal]=='dontcare':
						row.append(goal + '.Yes.dontcare')
					else:
						row.append(goal + '.Yes')
				else:
					row.append(goal + '.Yes.'+gdict[goal])
			else:
				row.append(goal + '.No')
			
			if goal in dict:
				if goal == 'name' or goal == 'food':
					if dict[goal]=='dontcare':
						row.append(goal + '.Yes.dontcare')
					else:
						row.append(goal + '.Yes')
				else:
					row.append(goal + '.Yes.'+dict[goal])
			else:
				row.append(goal + '.No')
			
			data.append(row)
		
		newHead = ['True', 'Predict']
		fio.writeMatrix(args.trackfile+'.'+goal+'.label', data, newHead)
	
if (__name__ == '__main__'):
	main(sys.argv)
	print "Done"