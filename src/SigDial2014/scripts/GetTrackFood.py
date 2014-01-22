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
	
	#goal_id = header.index('recovery_goals')	
	goal_id = header.index('goal_label')	
	sessions = json.load(open(args.trackfile))['sessions']
	
	tracker_output = []
	for s in sessions:
		tracker_output = tracker_output + s['turns']
	
	assert(len(body) == len(tracker_output))
	
	goal = 'food'
	data = []
	for i in range(len(body)):
		row = body[i]
		track_turn = tracker_output[i]
		goals = row[goal_id][1:-1]
		
		gdict = SlotTracker.getGoalsDict(goals)
		dict = getGoal(track_turn)
		
		row = []
		if goal in gdict:
			row.append(gdict[goal])
		else:
			row.append('none')
		
		if goal in dict:
			row.append(dict[goal])
		else:
			row.append('none')
		
		data.append(row)
		
	newHead = ['True', 'Predict']
	fio.writeMatrix(args.trackfile+'.'+goal+'.prediction', data, newHead)
	
if (__name__ == '__main__'):
	main(sys.argv)
	print "Done"