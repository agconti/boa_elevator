def parse_input(f):    
    '''
    f is the input file's path in quotes
    ie. 'input/sample.txt'
    
    returns a parsed list of elevator tasks
    '''
    import re
    tasks = []
    with open(f, 'r') as f:
        for i in f:
            append_holder = []
            
            i = i.strip()
            split_holder = re.split(":|-|,", i)
            
            #append starting floor value
            append_holder.append(int(split_holder[0]))
            
            #append tuples of start & end floors for tasks
            for i in xrange(1, len(split_holder),2):
                append_holder.append((int(split_holder[i]), int(split_holder[i+1])))  
            
            #append out append_holder bin to our output list named tasks.
            tasks.append(append_holder)
            del append_holder
        return tasks

def mode_A(task):
    '''
    '''
    trip_total = 0
    
    #calculate distance from starting floor to first task.
    trip_total = abs(task[0] - task[1][0])
    sys.stdout.write("%s " % task[0])
    task_lag = task[0]
    for i in xrange(1, len(task)):
        # print an error if data is malformed
        if len(task[i]) != 2:
            sys.stdout.write('\n[Error!] Data in task %s is not in the correct '\
                    '[<start_floor> - <end_floor>] format.\nTask:\n%s\n'\
                    %(i, task[i]))
        
        #calculate intra-floor trip distance
        trip_total += abs(task[i][1] - task[i][0])
        
        
        #output floors traveled
        #control for tasks that share the same start / stop floors
        if task_lag != task[i][0]:
            sys.stdout.write("%s " % task[i][0])
        
        sys.stdout.write("%s " % task[i][1])
        
        task_lag = task[i][1]
        
        #calculate distance traveled between requests
        if (i+1) < len(task):
            trip_total += abs(task[i][1] - task[i+1][0])
    #output total distance traveled 
    sys.stdout.write("(%s)\n" % trip_total)
        
def safely_add_to_list(val, target_list):
    '''
    adds only unique vales to a target list
    '''
    if (val in target_list) == False:
        target_list.append(val)

def mode_B(task):
    #handle case where path cannot be optimized beyond mode A
    if len(task) < 3:
        mode_A(task)
    else:
        import math
        trip_total = 0
        
        output = []
        sequence_list = []
        previous_sequence_list = None
        last_task = False
        first_sequence = True
        starting_floor = task[0]
        safely_add_to_list(starting_floor, output)
        for task_index in xrange(1, len(task)):
            
            current_task = task[task_index]
            current_direction = math.copysign(1, (current_task[0] - current_task[1]))
            
            #check if last task
            if (task_index) == (len(task) - 1):
                last_task = True
            else:
                next_task = task[(task_index + 1)]
                next_direction = math.copysign(1, (next_task[0] - next_task[1]))
                
            safely_add_to_list(current_task[0], sequence_list)
            safely_add_to_list(current_task[1], sequence_list)
            
            if (current_direction != next_direction) or last_task:
                
                #Handle the case where the elevator is going up
                if current_direction < 0:
                    sequence_list.sort()
                    for floor in sequence_list:
                        output.append(floor)
                    
                    for i in xrange(1, len(sequence_list)):
                        trip_total += (sequence_list[i] - sequence_list[i-1])
                
                #Handle the case where the elevator is going down    
                else:
                    sequence_list.sort(reverse=True)
                    for floor in sequence_list:
                        output.append(floor)
                    
                    for i in xrange(1, len(sequence_list)):
                        trip_total += (sequence_list[i-1] - sequence_list[i])
                         
                #calculate intra-sequence dist
                if (previous_sequence_list != None):
                    trip_total += abs(previous_sequence_list[-1] - sequence_list[0])
                    
                if first_sequence == True:
                    #calculate distance from starting floor to first task.
                    trip_total += abs(starting_floor - sequence_list[0])
                    
                #reset variables for next iteration    
                previous_sequence_list = sequence_list
                del sequence_list
                sequence_list = []
                first_sequence = False
        
        #output floor movements
        for i in xrange(0, len(output)):
            if i > 0 :
                if output[i] != output[i-1]:
                    sys.stdout.write("%s " % output[i])
            else:
                sys.stdout.write("%s " % output[i])
            
        sys.stdout.write("(%s)\n" %trip_total)
                    
            
        
    

def elevator(f, mode):
    '''
    BOA elevator function
    
    --Inputs -- 
    
    f is the input file's path in quotes
    ie. 'input/sample.txt'
    
    Mode is the mode elevator's operating mode.
    ie. 'A', or 'B'
    
    '''
    import sys
    
    tasks = parse_input(f)
    
    if mode.upper() == 'A':
        for i in tasks:
            mode_A(i)
    
    if mode.upper() == 'B':
        for i in tasks:
            mode_B(i)

if __name__ == "__main__":
    import sys
    elevator(str(sys.argv[1]), str(sys.argv[2]))