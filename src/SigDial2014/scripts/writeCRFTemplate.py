import fio

def writeCRFTemplate():
	
	#for i in range(51):
	for i in range(432):
		print 'U'+str(i)+':'+'%x[-2,'+str(i)+']'
		print 'U'+str(i)+':'+'%x[-1,'+str(i)+']'
		print 'U'+str(i)+':'+'%x[0,'+str(i)+']'
		#print 'U'+str(i)+':'+'%x[1,'+str(i)+']'
		#print 'U'+str(i)+':'+'%x[2,'+str(i)+']'
		#print 'U'+str(i)+':'+'%x[-1,'+str(i)+']/%x[0,'+str(i)+']'
		#print 'U'+str(i)+':'+'%x[0,'+str(i)+']/%x[1,'+str(i)+']'
		print
	
	print 'B'
	print

if (__name__ == '__main__'):
	writeCRFTemplate()