import rpyc
import GPU_utilities


proxy = rpyc.connect('localhost', 15000, config={'allow_public_attrs': True})
linecount = proxy.root.gpu_selector()
gpu_data = proxy.root.gpu_options()
print 'The next GPU to be selected is', linecount
print str(gpu_data)