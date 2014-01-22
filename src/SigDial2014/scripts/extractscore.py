import fio

def extractScoreAllMetrics():
	data = ['dstc2_train', 'dstc2_dev']
	
	score = []
	
	#modes = ['baseline_allmetrics', 'bestbyother_allmetrics', '3way_actngram_allmetrics', '3way_actngram_train23_allmetrics']
	#modes = ['bestbyother_allmetrics', '3way_actngram_allmetrics', '3way_actngram_dis_allmetrics']
	#modes = ['bestbyother_allmetrics', '3way_enrich3_allmetrics', '3way_enrich_train2_allmetrics', '3way_enrich_train3_allmetrics', '3way_enrich_train23_allmetrics']
	#modes = ['baseline', 'baseline_focus', 'HWUbaseline', 'baselineTop1']
	#modes = ['baseline', 'baseline_focus', 'HWUbaseline', '2waymodel_act', '2waymodel_actngram', '2waymodel_actngram_topline']
	#modes = ['topline2','topline3']
	#modes = ['2waymodel_actngram_method_topline', '2waymodel_actngram_method_online', '2waymodel_actngram_method_mindchange']
	modes = ['2waymodel_goals_bybrid']
			
	metrics = ['Joint_Goals', 'Requested', 'Method']
	
	header = ['test', metrics[0]+'_accuracy',  metrics[1]+'_accuracy', metrics[2]+'_accuracy',metrics[0]+'_l2',metrics[1]+'_l2',metrics[2]+'_l2']
	fio.PrintListwithName(header, 'method')
	for mode in modes:
		for test in data:
			#for k, L in enumerate([range(43,45)]):
			for k, L in enumerate([range(40,42)]):
				filename = "res/"+mode+"_"+test+"_score.txt"
				lines = fio.readfile(filename)
				
				s = []
				for i in L:
					line = lines[i].strip()
					nums = line.split("|")
					
					for km, metric in enumerate(metrics):
						s.append(nums[km+1])
					
				score.append([mode]+[test] + s)
	
	for i in range(len(score)):
		for j in range(len(score[0])):
			print score[i][j], "\t",
		print

def extractScoreAllMetricsWithROC():
	data = ['dstc2_train', 'dstc2_dev']
	
	score = []
	
	#modes = ['baseline_allmetrics', 'bestbyother_allmetrics', '3way_actngram_allmetrics', '3way_actngram_train23_allmetrics']
	#modes = ['bestbyother_allmetrics', '3way_actngram_allmetrics', '3way_actngram_dis_allmetrics']
	#modes = ['bestbyother_allmetrics', '3way_enrich3_allmetrics', '3way_enrich_train2_allmetrics', '3way_enrich_train3_allmetrics', '3way_enrich_train23_allmetrics']
	#modes = ['baseline', 'baseline_focus', 'HWUbaseline', 'baselineTop1']
	#modes = ['baseline', 'baseline_focus', 'HWUbaseline', '2waymodel_act', '2waymodel_actngram', '2waymodel_actngram_topline']
	#modes = ['topline2','topline3']
	#modes = ['2waymodel_actngram_method_topline', '2waymodel_actngram_method_online', '2waymodel_actngram_method_mindchange']
	modes = ['binaryswitch_fullscore_top3']
			
	metrics = ['Joint_Goals', 'Requested', 'Method']
	
	header = ['test', metrics[0]+'_accuracy',  metrics[1]+'_accuracy', metrics[2]+'_accuracy',metrics[0]+'_l2',metrics[1]+'_l2',metrics[2]+'_l2']
	fio.PrintListwithName(header, 'method')
	for mode in modes:
		for test in data:
			#for k, L in enumerate([range(43,45)]):
			for k, L in enumerate([range(40,42)]):
				filename = "res/"+mode+"_"+test+"_score.txt"
				lines = fio.readfile(filename)
				
				s = []
				for i in L:
					line = lines[i].strip()
					nums = line.split("|")
					
					for km, metric in enumerate(metrics):
						s.append(nums[km+1])
					
				score.append([mode]+[test] + s)
	
	for i in range(len(score)):
		for j in range(len(score[0])):
			print score[i][j], "\t",
		print
					
def extractScoreAllMetricsTopLine():
	data = ['dstc2_train', 'dstc2_dev']
	
	score = []
	
	modes = ['firstcorrect']
			
	metrics = ['Joint_Goals', 'Requested', 'Method']
	
	header = ['test', 'topK', metrics[0]+'_accuracy',  metrics[1]+'_accuracy', metrics[2]+'_accuracy',metrics[0]+'_l2',metrics[1]+'_l2',metrics[2]+'_l2']
	fio.PrintListwithName(header, 'method')
	for mode in modes:
		for test in data:
			for topK in range(11):
				#for k, L in enumerate([range(43,45)]):
				for k, L in enumerate([range(40,42)]):
					filename = "res/"+mode+"_"+test+"_score_"+str(topK)+".txt"
					lines = fio.readfile(filename)
					
					s = []
					for i in L:
						line = lines[i].strip()
						nums = line.split("|")
						
						for km, metric in enumerate(metrics):
							s.append(nums[km+1])
						
					score.append([mode]+[test] + [topK] + s)
		
	for i in range(len(score)):
		for j in range(len(score[0])):
			print score[i][j], "\t",
		print
		
if (__name__ == '__main__'):
	#extractScore()
	extractScoreAllMetrics()
	#extractScoreAllMetricsTopLine()