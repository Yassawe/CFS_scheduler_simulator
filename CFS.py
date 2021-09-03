from RBT import RBT, Node
import random

def read_input(path):
    
    #This function reads the input, and if some (or all) values are missing, it places random values there. Ranges are defined below
    #It returns the set of all processes, and the dictionary containing parameters for each process
    
    random_ranges = [[-20, 19], [1, 30], [0, 20]]    
    process_info = {}
    processes = set()

    file = open(path, "r")
    lines = file.readlines()

    for line in lines:
        tokens = line.split()
        if tokens == []:
            continue
        processes.add(tokens[0])
        
        try:
            priority = tokens[1]
        except:
            priority = random.randint(random_ranges[0][0], random_ranges[0][1])
            
        try:
            burst = tokens[2]
        except:
            burst = random.randint(random_ranges[1][0], random_ranges[1][1])
            
        try:
            arrival = tokens[3]
        except:
            arrival = random.randint(random_ranges[2][0], random_ranges[2][1])

        process_info[tokens[0]] = {
            'priority': int(priority),
            'burst': int(burst),
            'arrival': int(arrival),
            'hasEnteredQueue':False,
            'hasStarted':False,
            'hasEnded':False,
            'waiting': 0,
            'response': 0,
            'preempted': 0
        }
        
    return processes, process_info


def CFS(processes, process_info, quantum = 10, granularity=0.5, timestep = 0.05, verbose=True):
    queue = RBT() #use RBT as the queue
    time = 0 #use counter to keep track of the real time
    
    # Weights arranged in a line: for -20 nice value -- weight is 0.01 , for 19 nice value = ~2. For all others, it is interpolated along the line 
    # So, 0.01*timeslice for highest priority, 2*timeslice for the lowest.
    
    weights = lambda x: 99*x/2000 + 1 
    
    while processes:
        text = '\nTime: {}\n'.format(round(time,2))
        for key in process_info.keys():
            #add to the RBT only those processes that has arrived, and only if they did not already enter the queue
            #How new processes are added to the RBT: 
            #1) if the queue is empty, add with vruntime=0
            #2) if the queue is not empty, add with the vruntime equal to the current root. So that the new process lands in the center of the queue.
            # Why: if we add to the right, it might take a long time to get to the left. if we add to the left, we might starve those already waiting in the right
            if time>=process_info[key]['arrival'] and not process_info[key]['hasEnteredQueue']:
                if queue.root is queue.nil:
                    startvalue = 0
                else:
                    startvalue = queue.root.val    
                process_info[key]['hasEnteredQueue']=True
                node = Node(startvalue, key)
                queue.insert(node)
                
        if queue.root.val is None:
            #if there are no processes waiting, CPU is idle
            # timestep is a small step to take when that happens, to progress time
            text = text + ' CPU is idle\n'
            if verbose:
                print(text)
            time+=timestep
            continue
        
        contenders = queue.n_elements
        text = text + "{} processes are competing for CPU\n".format(contenders)
        
        #define timeslice as q/N. If it is smaller than granularity, use granularity instead
        timeslice = round(quantum/contenders, 2) if quantum/contenders>granularity else granularity
        
        
        text = text + "Timeslice = {}\n".format(timeslice)
        
        #pop from the RBT the leftmost process. This process will run for the timeslice. 
        #My implementation of RBT allows to do so without search.
        current_process = queue.get_leftmost()
        name = current_process.process
        vruntime = current_process.val
        queue.delete(current_process)
        
        
        if not process_info[name]['hasStarted']:
            #calculate response time, i.e. time from the begining to the time when process has started
            #it is simply current time (when the process has started) - arrival time
            #in order not ti repeat this code on each iteration, flag 'hasStarted' is used
            process_info[name]['response']=(time-process_info[name]['arrival'])
            process_info[name]['hasStarted'] = True
            text = text + "Process {} has started.\n".format(name, timeslice)
        
        text = text + "Process {} is running\n".format(name)
        
        for key in process_info.keys():
            #Increment waiting time for each process, except one currently running
            if key!=name and process_info[key]['hasEnteredQueue'] and not process_info[key]['hasEnded']:
                process_info[key]['waiting']+=timeslice
        
        #calculate new vruntime, according to the timeslice and weight, defined above
        vruntime = vruntime + timeslice*weights(process_info[name]['priority'])
        #decrement the remaining burst time
        process_info[name]['burst']-=timeslice

        if process_info[name]['burst']<=0 and not process_info[name]['hasEnded']:
            #if the burst time has ended, process has finished. Indicate so, using 'hasEnded' flag
            processes.remove(name)
            process_info[name]['hasEnded']=True
            text = text + "Process {} has ended\n".format(name)
        else:
            #if the process has not finished, put it back to the RBT with the updated vruntime
            node = Node(vruntime, name)
            queue.insert(node)
            #process will be preemted, if it is no longer the leftmost node, it is preemted
            next_process = queue.get_leftmost()
            if next_process.process!=name:
                text = text + "Process {} is preemted\n".format(name)
                process_info[name]['preempted']+=1
        
        #update the time 
        time+=timeslice
        
        if verbose:
            print(text)
    
    return process_info

def showresults(results):
    waitings = []
    responses = []
    
    print("==================RESULTS=================")
    
    for key in results.keys():
        text = '\nProcess {}:\n'.format(key)
        
        waiting = results[key]['waiting']
        response = results[key]['response']
        preempted = results[key]['preempted']
        
        waitings.append(waiting)
        responses.append(response)
        
        text = text + 'Response time: {}\n'.format(response)
        text = text + 'Waiting time: {}\n'.format(waiting)
        text = text + 'Was preemted {} times\n'.format(preempted)
        
        print(text)
        
    av_w = sum(waitings)/len(waitings)
    av_r = sum(responses)/len(responses)
    
    text = "Average waiting time: {}\n".format(av_w) 
    text = text + "Average response time: {}\n".format(av_r)
    print(text)      

if __name__=='__main__':
    quantum = 10
    granularity = 0.5
    timestep = 0.05
    processes, process_info = read_input('input.txt')
    results = CFS(processes, process_info, quantum, granularity, timestep, verbose=True)
    showresults(results)