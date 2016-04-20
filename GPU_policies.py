import GPU_utilities


class GPU_Policy():
    next_dev = 0
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
	  gpu_obj=GPU_data(devicenum)
	  gpu_list.append(gpu_obj)


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
	del queue_list[task_id]
	return 0
      else:
	print '[ERROR][REMOVE_FROM_QUEUE] Task_id not present in queue.\n'
	return -1





class Round_Policy(GPU_Policy):
    def update_next(self, task_id):
      self.next_dev= (self.next_dev+1)%number_gpus
      error=GPU_Policy.insert_into_queue(task_id, self.next_dev)
      return error
      

class IsEmpty_Policy(GPU_Policy):
    def update_next(self, task_id):
      #check if there is any 


class Random_Policy(GPU_Policy):
    import random
    def update_next(self, task_id):
      self.next_dev= random.randint(0, self.number_gpus)
      error=GPU_Policy.insert_into_queue(task_id, self.next_dev)
      return error