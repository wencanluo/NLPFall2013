import fio

def extractScoreWeka():
	tests = ['res_act_remove_this',]
	score = []
	for test in tests:
		filename = "res/"+test+".txt"
		lines = fio.readfile(filename)
		n = len(lines)
		
		i = 10
		while(i<n):
			s = []
			line = lines[i].strip()
			nums = line.split()
			for k in [4,5,6]:
				s.append(nums[k])
			score.append(s)
			i = i + 18
	
	print "Precision\tRecall\tF-Measure"				
	for row in score:
		for col in row:
			print col,"\t",
		print

def extractScoreWekaMethod():
	tests = ['res_method_actngram',]
	score = []
	for test in tests:
		filename = "res/"+test+".txt"
		lines = fio.readfile(filename)
		n = len(lines)
		
		i = 13
		while(i<n):
			s = []
			line = lines[i].strip()
			nums = line.split()
			for k in [4,5,6]:
				s.append(nums[k])
			score.append(s)
			i = i + 38-14
	
	print "Precision\tRecall\tF-Measure"				
	for row in score:
		for col in row:
			print col,"\t",
		print
			
if (__name__ == '__main__'):
	extractScoreWeka()
	#extractScoreWekaMethod()