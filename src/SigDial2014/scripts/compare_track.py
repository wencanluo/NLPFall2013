import sys, os, json

def main():
	track1 = "res/topline_dstc2_dev_track_3.json"
	track2 = "res/topline_dstc2_dev_track_9.json"
	
	tracker1 = json.load(open(track1))
	tracker2 = json.load(open(track2))
	
	
	
	for session1, session2 in zip(tracker1['sessions'], tracker2['sessions']):
		turn_count = 0
		for turn1, turn2 in zip(session1['turns'],session2['turns']):
			request1 = turn1["requested-slots"]
			request2 = turn2["requested-slots"]
			
			
			if request1 != request2:
				print session1['session-id'], "\t", turn_count, "\t", request1,"\t", request2
			
			turn_count = turn_count + 1
			
if __name__ =="__main__" :
	main()