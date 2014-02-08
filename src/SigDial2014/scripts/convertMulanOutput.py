import fio

def main():
	data = ['dstc2_train', 'dstc2_dev', 'dstc2_test']
	for test in data:
		mulanfile = 'res/' + test + "_request_asr_act_score_all_ngram.arff.label"
		body = fio.MulanOutReader(mulanfile)
		
		header = []
		for i in range(len(body[0])):
			header.append('p' + str(i))
		
		fio.writeMatrix(mulanfile+'.matrix', body, header)

if __name__ == '__main__':
	main()
	print "Done"