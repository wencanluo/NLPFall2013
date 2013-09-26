import fio

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
	