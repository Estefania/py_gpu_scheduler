import pycuda.driver as cuda
import pycuda.autoinit
import pycuda.tools


class GPU_data():
    #static processes
    device_number = 0
    memory = 0
    compute_capability = ''
    number_cores = 0
    #Dynamic properties
    proccesses_executing = 0
    free_memory = 0

    def __init__(self,device_number):
      cuda.init()
      device = cuda.Device(device_number)
      contx = device.make_context()
      self.obtain_static_info(device,device_number)
      self.obtain_dynamic_info(device,device_number)
      contx.pop()
      del contx
    def get_device_number(self):
      return device_number
    def get_memory(self):
      return self.memory
    def get_compute_capability(self):
      return self.compute_capability
    def get_number_cores(self):
      return self.number_cores
    def get_processes_executing(self):
      return self.processes_executing
    def get_free_memory(self):
      return self.free_memory

    def set_device_number(self,device_number):
      self.device_number = device_number
    def set_memory(self,memory):
      self.memory = memory
    def set_compute_capability(self,compute_capability):
      self.compute_capability = compute_capability
    def set_number_cores(self,number_cores):
      self.number_cores = number_cores
    
    def set_processes_executing(self,processes_executing):
      self.processes_executing = processes_executing 
    def set_free_memory(self,free_memory):
      self.free_memory = free_memory

    
    
    def obtain_executing_processes(self,device_num):
      #to be implemented
      return 0
    
    def obtain_static_info(self,device,device_number):
      
      (free,total)=cuda.mem_get_info()
      dev_data= pycuda.tools.DeviceData(device)
      self.set_device_number(device_number)
      self.set_memory(total)
      self.set_compute_capability(device.get_attribute(cuda.device_attribute.COMPUTE_CAPABILITY_MAJOR))#getting major compute capability (possible also to get minor
      self.set_number_cores(device.get_attribute(cuda.device_attribute.MULTIPROCESSOR_COUNT))

      
    def obtain_dynamic_info(self,device,device_number):
      
      
      (free,total)=cuda.mem_get_info()
      dev_data= pycuda.tools.DeviceData(device)
      self.set_free_memory(free)
      num_processes= self.obtain_executing_processes(device_number)
      self.set_processes_executing(num_processes)

      
      
    def __repr__(self):
       #static processes
      string_res= 'DEV_NUM: '+str(self.device_number)+'\nTOTAL_MEM: '+str(self.memory)+'\nCOMPUTE_CAP: '+str(self.compute_capability)+'\nNUM_CORES: '+str(self.number_cores)+'\nPROC_EXEC: '+str(self.proccesses_executing)+'\nFREE_MEM: '+str(self.free_memory)
      return string_res
      
      
      
def main():

      
      gpu_list= []
      for devicenum in range(cuda.Device.count()):
	gpu_obj=GPU_data(devicenum)
	gpu_list.append(gpu_obj)
	print str(gpu_obj)
	
      print 'Finish testing'
	
      
if __name__ == "__main__": main()
	 