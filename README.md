
Author: Estefania

Version 0.01


This repository contains an scheduler for managing and discovering NVidia GPUs inside a node. It can be used to schedule Python applications with CUDA kernels into the available GPUs. 

The main dependencies are PyCUDA and RPyc packages, both of them can be found in the package manager pip.


Use: 

python server.py <number of policy>

Where number of policy is : 
  0: Random policy
  1: Round Robin policy
  2: Least processes policy
