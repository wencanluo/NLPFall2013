import fio

def extractScoreTopK():
	data="test4"
	
	score = []
	
	for topK in range(1,11):
		filename = "topline_"+data+"_score_"+str(topK)+".txt"
		lines = fio.readfile(filename)
		scorek = []
		
		for i in [5,12,19]:
			line = lines[i].strip()
			nums = line.split()
			scorek.append(nums[11])
		
		score.append(scorek)
	
	for i in range(3):
		for topK in range(10):
			print score[topK][i]

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
	extractScoreAllMetrics()