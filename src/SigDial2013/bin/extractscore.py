import fio

def extractScore():
	tests = ['test1', 'test2', 'test3', 'test4']
	
	print "method","\t", 'test1',"\t", 'test2',"\t", 'test3',"\t", 'test4'
	#modes = ['baseline', 'majoritybaseline','bestbyother', '3way', '3way_actngram', '3way_crf_act', '3way_crf_act', 'topline']
	modes = ['baseline', 'bestbyother', '3way', '3way_actngram', '3way_crf_act', '3way_crf_actngram', 'topline']
	for L in [[5], [12], [19]]:
		score = []
		
		for mode in modes:
			s = []
			for test in tests:
				filename = "res/"+mode +"_"+test+"_score.txt"
				lines = fio.readfile(filename)
				for i in L:
					line = lines[i].strip()
					nums = line.split()
					s.append(nums[10])#11 for all, 10 for joint
			score.append(s)
		
		
		for i, row in enumerate(score):
			print modes[i],"\t",
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
	
	schedules = ['schedule1','schedule2','schedule3']
	#modes = ['baseline_allmetrics', 'bestbyother_allmetrics', '3way_actngram_allmetrics', '3way_actngram_train23_allmetrics']
	#modes = ['bestbyother_allmetrics', '3way_actngram_allmetrics', '3way_actngram_dis_allmetrics']
	#modes = ['bestbyother_allmetrics', '3way_enrich3_allmetrics', '3way_enrich_train2_allmetrics', '3way_enrich_train3_allmetrics', '3way_enrich_train23_allmetrics']
	modes = ['3way_actngram_allmetrics']
	
	header = ['test', 'method', 'accuracy', 'avgp', 'l2', 'mrr']
	fio.PrintListwithName(header, 'schedule')
	for mode in modes:
		for k, L in enumerate([range(5,9),range(15,19),range(25,29)]):
			for test in data:
				filename = "res/"+mode+"_"+test+"_score.txt"
				lines = fio.readfile(filename)
				
				s = []
				for i in L:
					line = lines[i].strip()
					nums = line.split()
					s.append(nums[11])
					
				score.append([mode]+[schedules[k]]+[test] + s)
	
	for i in range(len(score)):
		for j in range(len(score[0])):
			print score[i][j], "\t",
		print
			

if (__name__ == '__main__'):
	#extractScore()
	extractScoreAllMetrics()