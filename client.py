import rpyc
import GPU_utilities


proxy = rpyc.connect('localhost', 15000, config={'allow_public_attrs': True})
for i in range(12):
	linecount = proxy.root.gpu_selector('spark_task_'+str(i))
	print 'The next GPU to be selected is', linecount

gpu_data = proxy.root.gpu_options()
print str(gpu_data)
