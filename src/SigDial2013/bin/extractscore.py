import fio

def extractScore():
	tests = ['test1', 'test2', 'test3', 'test4']
	
	for L in [[5], [12], [19]]:
		score = []
		
		for mode in ['baseline', 'nohistory', 'majoritybaseline', '3way', 'topline']:
			s = []
			for test in tests:
				filename = "res/"+mode +"_"+test+"_score.txt"
				lines = fio.readfile(filename)
				for i in L:
					line = lines[i].strip()
					nums = line.split()
					s.append(nums[11])
			score.append(s)
		
		for row in score:
			for col in row:
				print col,"\t",
			print
			
def extractScoreTopK():
	tests = ['test1', 'test2', 'test3', 'test4']
	
	for L in [[5], [12], [19]]:
		score = []
		for k in range(-1, 9):
			s = []
			for mode in ['baseline', 'nohistory', 'majoritybaseline', '3way', 'topline']:
				#filename = "res/topline_"+test+"_score_"+str(k)+".txt"
				#filename = "res/baseline_"+test+"_score.txt"
				for test in tests:
					filename = "res/"+mode +"_"+test+"_score.txt"
					lines = fio.readfile(filename)
					for i in L:
						line = lines[i].strip()
						nums = line.split()
						s.append(nums[10])
			score.append(s)
		
		for row in score:
			for col in row:
				print col,"\t",
			print

def extractScoreAllMetrics():
	data = ["test1", "test2", "test3", "test4"]
	
	score = []
	
	#L = range(43,56)
	#L = range(43,56)
	L = range(43,56)
	
	for test in data:
		filename = "res/baseline_allmetrics_"+test+"_score.txt"
		lines1 = fio.readfile(filename)
		
		filename = "res/nohistory_allmetrics_"+test+"_score.txt"
		lines2 = fio.readfile(filename)

		s = []
		for i in L:
			line = lines1[i].strip()
			nums = line.split()
			s.append(nums[11])
			
		score.append(s)
		
		s = []
		for i in L:			
			line = lines2[i].strip()
			nums = line.split()
			s.append(nums[11])
		score.append(s)
	
	for j in range(len(score[0])):
		for i in range(len(score)):
			print score[i][j], "\t",
		print
			

if (__name__ == '__main__'):
	extractScore()