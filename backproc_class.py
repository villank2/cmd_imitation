#Name: Kyle Angelo Villanueva
#17428562


from func import *
import subprocess
import threading
from queue import Queue

'''called my MyShell a class created to run background processses'''
class BackProc():
    #cmd is the command, args are the given arguments
    def __init__(self,cmd,args):
        self._cmd = cmd
        self._args = args.split()
        self.overwite = False
        self.set_stdout()   
        self.set_stdin()
        self.run()  #run subprocess up class creation

    def set_stdout(self):
        ''' set self.stdout to the filename(string) given at next index of > or >>'''
        try:
            if '>>' in self._args:
                self.stdout = self._args[self._args.index('>')+1]
            elif '>' in self._args:
                self.stdout = self._args[self._args.index('>>')+1]
                self.overwite = True
            else:
                self.stdout = None
        except IndexError:
            '''print output if any on terminal if no filename is given but > or >> exists'''
            None
    
    def set_stdin(self):
        '''set stdin to given filename if it exists, if non existent set it to None'''
        try:
            if '<' in self._args:
                self.stdin = self._args[self._args.index('<')+1]
            else:
                self.stdin = None
        except IndexError:
            print("Missing File corresponding to '<'")
        
    def destructor(self,proc):
        '''creates a thread that repeatedly checks if the subprocess has terminated, background_check signals the signal_handler when the subprocess terminates'''
        #using a Queue for signaling between threads
        q = Queue(1)
        worker = threading.Thread(target=background_check,args=(proc,q,))
        worker.start()
        destroy = threading.Thread(target=self.signal_handler,args=(q,))
        destroy.start()
    
    def signal_handler(self,q):
        #deletes the instance of this class once the subprocess has finished executing
        while True:
            if q.full():
                break
        del self
    
    def run(self):
        ''' determine whether io redirection is required, set o_file and r_file to None if not required
        determine whether output redirection is to be overwritten or appended'''
        try:
            if self.overwite:
                todo = 'w'
            else:
                todo = 'a'
            o_file = open(self.stdout, todo) if self.stdout else None
            r_file = open(self.stdin, 'r') if self.stdin else None
            
            '''subprocess.Popen accepts stdin and stdout which can be set to a file (existing if stdin) or None'''
            
            proc = subprocess.Popen([self._cmd,self._args[0]],stdin=r_file,stdout=o_file)
            self.destructor(proc)
            #delete this instance of the class BackProc
        except FileNotFoundError:
            print("{} does not exist".format(self.stdin))
            del self
        except:
            print("Unable to run {} {}\n".format(self._cmd," ".join(self._args)))
            del self