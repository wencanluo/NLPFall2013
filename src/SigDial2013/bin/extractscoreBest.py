import fio

def findBest(file, test, schedule, slot, metric, sortFlag = True):
	header, body = fio.readMatrix(file, True)
	
	test_id = header.index('testset')
	slot_id = header.index('slot')
	schedule_id = header.index('schedule')
	metric_id = header.index('metric')
	val_id = header.index('val')
	
	if sortFlag:
		maxVal = 0
	else:
		maxVal = 65535
	
	for row in body:
		testid = row[test_id]
		slotid = row[slot_id]
		scheduleid = row[schedule_id]
		metricid = row[metric_id]
		val = row[val_id]
		
		if testid != test: continue
		if slotid != slot: continue
		if scheduleid != schedule: continue
		if metricid != metric: continue
		
		if sortFlag:
			if float(val) > maxVal:
				maxVal = float(val)
		else:
			if float(val) < maxVal:
				maxVal = float(val)
				
	return maxVal
		
	
def extractScoreBest():
	file = 'res/best.txt'
	
	tests = ["test1", "test2", "test3", "test4"]
	schedules = ['schedule1','schedule2','schedule3']
	#metrics = ['accuracy', 'avgp', 'l2', 'mrr', 'roc.v1_ca05', 'roc.v2_ca05']
	metrics = ['roc.v1_ca05', 'roc.v2_ca05']
	slots = ['joint', 'all']
	
	for test in tests:
		print test
		for s in schedules:
			print s
			for m in metrics:
				print m
				for slot in slots:
					if m == 'l2':
						print '%.4f' % findBest(file, test, s, slot, m, False),
					else:
						print '%.4f' % findBest(file, test, s, slot, m),
				print
			print
		print
	print
	
			
if (__name__ == '__main__'):
	extractScoreBest()