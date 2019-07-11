#Name: Kyle Angelo Villanueva
#17428562


def ampersand(line):
    return '&' in line

def checkq(queue):
    '''called as a thread, receives cmdqueue as a parameter, used for exiting the shell when batch
    file exists''' 
    while queue:
        continue
    queue.append('force_exit')

def background_check(proc,q):
    '''receives a subprocess created by a BackProc class'''
    while True:
        #proc.poll() checks if a subprocess has finished execution,returns None if it hasnt
        rcode = proc.poll()
        if rcode != None:
            break
    #signal termination 
    q.put(1)