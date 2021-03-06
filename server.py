import rpyc
import GPU_utilities as GPU_inf
import GPU_policies
import sys

def customize_policy(chose_pol):
    try:
    	policy_chosen= GPU_policies.GPU_Policy_Options.options[chose_pol]
    except KeyError,e:
	print 'That policy is not available\n'
	return -1
    class GPUAvalaibleService(rpyc.Service):
    	policy=policy_chosen
    	def exposed_gpu_selector(self,task_id, memory):	
		return self.policy.update_next(task_id, memory)
        	#return linenum + 1
       	def exposed_gpu_finish(self, task_id): 
		error=self.policy.remove_from_queue(task_id)
		return error
    	def exposed_gpu_options(self):
      		return GPU_inf.GPU_data
    return GPUAvalaibleService
'''Function in charge of starting a threaded server
It receives the port port_number'''
def start_server(port_number, gpu_opt):
  from rpyc.utils.server import ThreadedServer
  print str(gpu_opt)
  GPUService = customize_policy(gpu_opt)
  if not isinstance(GPUService,int):
  	t = ThreadedServer(GPUService, port = port_number,reuse_addr=True,listener_timeout=None )
  	print 'Starting server:'
	t.start()
  else:
	exit()
  
def main(argv):
  gpu_opt = int(argv[1])
  start_server(8888, gpu_opt)
  
if __name__ == "__main__": main(sys.argv)
