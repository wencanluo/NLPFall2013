import fio

def extractScoreWeka():
	tests = ['res_enrich-train2',]#'res_actngram_train2',]#'res_acts_train2', 'res_acts_train2_cost', 'res_ngram_train2']
	
	score = []
	for test in tests:
		
		
		filename = "res/"+test+".txt"
		lines = fio.readfile(filename)
		n = len(lines)
		
		i = 11
		while(i<n):
			s = []
			line = lines[i].strip()
			nums = line.split()
			for k in [4,5,6]:
				s.append(nums[k])
			score.append(s)
			i = i + 20
	
	print "Precision\tRecall\tF-Measure"				
	for row in score:
		for col in row:
			print col,"\t",
		print
			
if (__name__ == '__main__'):
	extractScoreWeka()