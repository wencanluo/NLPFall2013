import fio

def extractScoreAllMetrics():
	data = ["test1", "test2", "test3", "test4"]
	
	score = []
	
	schedules = ['schedule1','schedule2','schedule3']
	#modes = ['baseline_allmetrics', 'bestbyother_allmetrics', '3way_actngram_allmetrics', '3way_actngram_train23_allmetrics']
	#modes = ['bestbyother_allmetrics', '3way_actngram_allmetrics', '3way_actngram_dis_allmetrics']
	#modes = ['bestbyother_allmetrics', '3way_enrich3_allmetrics', '3way_enrich_train2_allmetrics', '3way_enrich_train3_allmetrics', '3way_enrich_train23_allmetrics']
	#modes = ['bestbyother_allmetrics', '3way_enrich_voting_allmetrics']
	modes = ['3way_enrich_voting_rawslu_allmetrics', '3way_enrich_voting_rawslu5_allmetrics']
	
	header = ['schedule', 'test', 'accuracy', 'l2', 'roc.v2_ca05']
	fio.PrintListwithName(header, 'method')
	for mode in modes:
		#for k, L in enumerate([range(5,9),range(15,19),range(25,29)]):
		for k, L in enumerate([[5,7,13],[22,24,30],[39,41,47]]):
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

def extractWeightScoreMetrics():
	data = ["test1"]
	
	score = []
	
	schedules = ['schedule1','schedule2','schedule3']
	#modes = ['baseline_allmetrics', 'bestbyother_allmetrics', '3way_actngram_allmetrics', '3way_actngram_train23_allmetrics']
	#modes = ['bestbyother_allmetrics', '3way_actngram_allmetrics', '3way_actngram_dis_allmetrics']
	#modes = ['bestbyother_allmetrics', '3way_enrich3_allmetrics', '3way_enrich_train2_allmetrics', '3way_enrich_train3_allmetrics', '3way_enrich_train23_allmetrics']
	#modes = ['bestbyother_allmetrics', '3way_enrich_voting_allmetrics']
	modes = ['3way_enrich_voting_allmetrics']
	
	header = ['schedule', 'test', 'accuracy', 'l2', 'roc.v2_ca05']
	fio.PrintListwithName(header, 'method')
	for mode in modes:
		#for k, L in enumerate([range(5,9),range(15,19),range(25,29)]):
		#for k, L in enumerate([[5,7,13],[22,24,30],[39,41,47]]):
		for k, L in enumerate([[13],[30],[47]]):
			for test in data:
				for w1 in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
					for w2 in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
						for w3 in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
							filename = "res/score/"+mode+"_"+test+"_"+str(w1)+'_'+str(w2)+'_'+str(w3)+"_score.txt"
							lines = fio.readfile(filename)
							
							s = []
							for i in L:
								line = lines[i].strip()
								nums = line.split()
								s.append(nums[11])
					
							score.append([mode]+[schedules[k]]+[test] + [w1, w2, w3] + s)
	
	for i in range(len(score)):
		for j in range(len(score[0])):
			print score[i][j], "\t",
		print
		
if (__name__ == '__main__'):
	#extractScore()
	#extractScoreAllMetrics()
	extractWeightScoreMetrics()