import GPU_utilities
import random
import threading
class GPU_Policy():
    next_dev = -1
    number_gpus = 0
    queue_tasks = {}
    gpu_list = []

    def __init__(self):
      self.GPU_count()
      if self.number_gpus== 0:
	 #there are no gpus available
	 next_dev = -1
	 return
      else:
	next_dev = 0 #first device by default
	for devicenum in range(self.number_gpus):
	  gpu_obj=GPU_utilities.GPU_data(devicenum)
	  self.gpu_list.append(gpu_obj)
	self.condition_gpu_avail = threading.Condition()


    def GPU_count(self):
      import pycuda.autoinit
      import pycuda.driver as cuda
      
      self.number_gpus= cuda.Device.count()
    def is_next(self):
      return next_dev
    
    def insert_into_queue(self, task_id, gpu_number):
      if task_id not in self.queue_tasks:
	self.queue_tasks[task_id] = gpu_number
	print str(self.queue_tasks)
	return 0
      else:
	self.queue_tasks[task_id] = gpu_number
	print '[ERROR][INSERT_INTO_QUEUE] Task_id already present in queue.\n'
	return -1
      
    def remove_from_queue(self, task_id):
      self.condition_gpu_avail.acquire()		
      if task_id in self.queue_tasks:
	gpu_num,task_mem = self.queue_tasks[task_id]
	del self.queue_tasks[task_id]
	self.gpu_list[gpu_num].free_memory = self.gpu_list[gpu_num].free_memory + task_mem 
	print str(self.queue_tasks)
	self.condition_gpu_avail.notify()
	self.condition_gpu_avail.release()
        
	return 0
      else:
	print '[ERROR][REMOVE_FROM_QUEUE] Task_id not present in queue.\n'
	self.condition_gpu_avail.release()
	return -1


class Round_Policy(GPU_Policy):
    def update_next(self, task_id,task_mem):
      self.condition_gpu_avail.acquire()
      next_dev_loc= (self.next_dev+1)%self.number_gpus
      #there is not enough memory for task in that gpu, changing to round_robin
        #check the following one 
      num_gpus_search = 0
      while self.gpu_list[next_dev_loc].free_memory <= task_mem:
      	num_gpus_search = num_gpus_search+1
	if num_gpus_search == self.number_gpus:
		self.condition_gpu_avail.wait()#There is none available
		num_gpus_search=0
	next_dev_loc=(next_dev_loc+1)%self.number_gpus 

      self.next_dev = next_dev_loc
      self.gpu_list[next_dev_loc].free_memory = self.gpu_list[next_dev_loc].free_memory-task_mem
      error=self.insert_into_queue(task_id, [next_dev_loc, task_mem])
      self.condition_gpu_avail.release()
      return next_dev_loc



#Computes what GPU has less work.
class IsEmpty_Policy(GPU_Policy):

    def count_process_GPU(self,num_dev):
      return sum(1 for x in self.queue_tasks.values() if x[0]==num_dev)
    
    def update_next(self, task_id,task_mem):
      import sys
      self.condition_gpu_avail.acquire()
      min_processes_gpu = sys.maxint
      gpu_number = 0
      for i in range(self.number_gpus):
	num_proc=self.count_process_GPU(i)      
      	if num_proc<min_processes_gpu:
		min_processes_gpu = num_proc
		gpu_number = i
      next_dev_loc= gpu_number
      #there is not enough memory for task in that gpu, changing to round_robin
        #check the following one 
      num_gpus_search = 0

      while self.gpu_list[next_dev_loc].free_memory <= task_mem:
        num_gpus_search = num_gpus_search+1
        if num_gpus_search == self.number_gpus:
                self.condition_gpu_avail.wait()#There is none available
                num_gpus_search=0
        next_dev_loc=(next_dev_loc+1)%self.number_gpus

      self.gpu_list[next_dev_loc].free_memory = self.gpu_list[next_dev_loc].free_memory-task_mem
      error=self.insert_into_queue(task_id, [next_dev_loc, task_mem])
      self.condition_gpu_avail.release()
      return next_dev_loc
class Random_Policy(GPU_Policy):
    def __init__(self):
      GPU_Policy.__init__(self)
      random.seed()
    def update_next(self, task_id, task_mem):
      self.condition_gpu_avail.acquire()
      #Update dynamic data of the GPU
      next_dev_loc= random.randint(0, self.number_gpus-1)
      #there is not enough memory for task in that gpu, changing to round_robin
        #check the following one 
      num_gpus_search = 0

      while self.gpu_list[next_dev_loc].free_memory <= task_mem:
        num_gpus_search = num_gpus_search+1
        if num_gpus_search == self.number_gpus:
                self.condition_gpu_avail.wait()#There is none available
                num_gpus_search=0
        next_dev_loc=(next_dev_loc+1)%self.number_gpus

      self.gpu_list[next_dev_loc].free_memory = self.gpu_list[next_dev_loc].free_memory-task_mem
      error=self.insert_into_queue(task_id, [next_dev_loc, task_mem])
      self.condition_gpu_avail.release()
      return next_dev_loc
 
    
class GPU_Policy_Options():   
	options = {0 : Random_Policy(),
          	   1 : Round_Policy(),
          	   2 : IsEmpty_Policy()
	}

def main():
  #Initiating 
  policy_GPU = GPU_Policy_Options.options[2]
  
  gpu= policy_GPU.update_next('spark_01',18471772)
  
  print str(gpu)
  
  print str(policy_GPU.queue_tasks)
  
  
  gpu= policy_GPU.update_next('spark_02',20)
  
  print str(gpu)
  
  print str(policy_GPU.queue_tasks)
 
  gpu= policy_GPU.update_next('spark_03',200)
  
  print str(gpu)
  
  print str(policy_GPU.queue_tasks)
  
  policy_GPU.remove_from_queue('spark_01')
  
  print str(gpu)
  
  print str(policy_GPU.queue_tasks)

  gpu= policy_GPU.update_next('spark_04',200)

  print str(gpu)

  print str(policy_GPU.queue_tasks)

  
  
  
  
if __name__ == "__main__": main()
