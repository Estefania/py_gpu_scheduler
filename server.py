import rpyc
import GPU_utilities as GPU_inf

class GPUAvalaibleService(rpyc.Service):
    def exposed_gpu_selector(self):
	GPU_id = 0
	return GPU_id
        #return linenum + 1
        
    def exposed_gpu_options(self):
      return GPU_inf.GPU_data(0)

'''Function in charge of starting a threaded server
It receives the port port_number'''
def start_server(port_number):
  from rpyc.utils.server import ThreadedServer
  t = ThreadedServer(GPUAvalaibleService, port = port_number )
  t.start()
  
  
def main():
  start_server(15000)
  
if __name__ == "__main__": main()