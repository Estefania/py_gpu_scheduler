import GPU_utilities
import random
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


    def GPU_count(self):
      import pycuda.autoinit
      import pycuda.driver as cuda
      
      self.number_gpus= cuda.Device.count()
    def is_next(self):
      return next_dev
    
    def insert_into_queue(self, task_id, gpu_number):
      if task_id not in self.queue_tasks:
	self.queue_tasks[task_id] = gpu_number
	return 0
      else:
	print '[ERROR][INSERT_INTO_QUEUE] Task_id already present in queue.\n'
	return -1
      
    def remove_from_queue(self, task_id):
      if task_id in self.queue_tasks:
	del self.queue_tasks[task_id]
	return 0
      else:
	print '[ERROR][REMOVE_FROM_QUEUE] Task_id not present in queue.\n'
	return -1


class Round_Policy(GPU_Policy):
    def update_next(self, task_id):
      self.next_dev= (self.next_dev+1)%self.number_gpus
      error=self.insert_into_queue(task_id, self.next_dev)
      return self.next_dev
      
#Computes what GPU has less work.
class IsEmpty_Policy(GPU_Policy):

    def count_process_GPU(self,num_dev):
      return sum(1 for x in self.queue_tasks.values() if x==num_dev)
    
    def update_next(self, task_id):
      import sys
      min_processes_gpu = sys.maxint
      gpu_number = 0
      for i in range(self.number_gpus):
	num_proc=self.count_process_GPU(i)      
      	if num_proc<min_processes_gpu:
		min_processes_gpu = num_proc
		gpu_number = i
      self.next_dev= gpu_number
      error=self.insert_into_queue(task_id, self.next_dev)
      #check if there is any 
      return self.next_dev


class Random_Policy(GPU_Policy):
    def __init__(self):
      GPU_Policy.__init__(self)
      random.seed()
    def update_next(self, task_id):
      self.next_dev= random.randint(0, self.number_gpus-1)
      error=self.insert_into_queue(task_id, self.next_dev)
      return self.next_dev
    
    
class GPU_Policy_Options():   
	options = {0 : Random_Policy(),
          	   1 : Round_Policy(),
          	   2 : IsEmpty_Policy()
	}

def main():
  #Initiating 
  policy_GPU = GPU_Policy_Options.options[2]
  
  gpu= policy_GPU.update_next('spark_01')
  
  print str(gpu)
  
  print str(policy_GPU.queue_tasks)
  
  
  gpu= policy_GPU.update_next('spark_02')
  
  print str(gpu)
  
  print str(policy_GPU.queue_tasks)
 
  gpu= policy_GPU.update_next('spark_03')
  
  print str(gpu)
  
  print str(policy_GPU.queue_tasks)
  
  policy_GPU.remove_from_queue('spark_02')
  
  print str(gpu)
  
  print str(policy_GPU.queue_tasks)

  gpu= policy_GPU.update_next('spark_04')

  print str(gpu)

  print str(policy_GPU.queue_tasks)

  
  
  
  
if __name__ == "__main__": main()
