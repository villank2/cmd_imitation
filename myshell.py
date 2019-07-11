#Name: Kyle Angelo Villanueva
#17428562

from cmd import Cmd
from func import *
from help_class import Help
from help_class import _dic
import subprocess
import sys, os
import threading
from queue import Queue
from backproc_class import BackProc
Help = Help()
readme = None
class MyShell(Cmd):

    def __init__(self):
        #retain the parent class' attributes but add new attributes
        super().__init__(completekey='tab', stdin=None, stdout=None)
        self.overwrite = False
        self.outFile = None
        self.pwd = os.getcwd()
        self.batch()

    def batch(self):
        """A method called upon shell construction to check if there is a given argument vector and if the batch file exists.
        If the batch file exists, lines corresponding to commands and parameters will be extended to the cmdqueue.
        Raise an error if the given file does not exist and then exit the shell"""
        if len(sys.argv) > 1:
            try:
                filename = sys.argv[1]
                with open(filename) as f:
                    self.cmdqueue.extend([line for line in f.readlines()])
            except FileNotFoundError:
                print("No such file \"{}\"\nExiting...".format(filename))
                raise SystemExit
            finally:
                #keep checking if the cmdqueue is not empty, once empty exit the shell
                q = Queue()
                check = threading.Thread(target=checkq,args=(self.cmdqueue,))
                check.start()
                

    def precmd(self, line):
        """a hook method in cmd.Cmd
        overwritten to check if the line  requires IO redirection"""
        cmd, args, line = self.parseline(line)
        if '>' in line:
            self.set_outFile(args)
        elif self.outFile:
            self.outFile = None
        return line
    
    def postcmd(self, stop, line):
        '''a hook method in cmd.Cmd
        retain parent method but add self.reset(). self.reset() ensures that after every command is called,executed and terminated, self.stdout is set to sys.stdout'''
        super().postcmd(stop, line)
        self.reset()
        return stop

    def default(self, line):
        """A method for dealing with unrecognized prefixes"""
        cmd,args,line = self.parseline(line)
        try:
            background = ampersand(line)
            if background:
                bg = BackProc(cmd,args)
            else:
                self.subproc(line)
        except:
            sys.stdout.write("Unknown command '{}' returning to shell...\n".format(line))
    
    def emptyline(self):
        """Called when an empty line is entered by the user
        if so, do nothing"""
        return

    def set_outFile(self,args):
        ''' a function called by 'precmd' and takes in the arguments of the command
        it sets the outFile attribute to the string at the next index of > or >>'''
        try: 
            args = args.split()
            self.overwrite = '>' in args
            if self.overwrite:
                self.outFile = args[args.index('>')+1]
            else:
                self.outFile = args[args.index('>>')+1]
        except IndexError:
            ''' if no file is given it will raise and index error, to catch this exception
            were just gonna ignore the redirection and print the output on the terminal'''
            None

    def set_stdout(self):
        '''an important method called at the start of each method that supports io redirection, this sets up the output location, if outFile is not set then self.stdout remainis as sys.stdout'''
        if self.outFile:
                if self.overwrite:
                    self.stdout = open(self.outFile, 'w')
                else:
                    self.stdout = open(self.outFile, 'a')
    
    def subproc(self,line):
        """Called by the default method to create a non-background
        subprocess"""
        self.set_stdout()
        proc = subprocess.Popen(line.split(),stdout=self.stdout)
        proc.wait()     #ensures that the subprocess executes and terminates before returning to the shell
    
    def do_help(self,args):
        '''may or may not accept an argument(s), check if first argument is an internal command or requires output redirection'''
        '''sets up readme omly in the first call of help method'''
        self.set_stdout()
        global readme
        if not(readme):
            with open('readme','r') as f:
                readme = f.read()
        #check for the case of help on an internal method
        if args and args[0]!='>':
            '''isolate the internal method which is callable in the Help class''' 
            attr = args.split()[0]
            func = getattr(Help,attr)
            self.stdout.write(func())
        elif self.outFile:
            '''if help does not take an argument but requires output redirection, write the manual into the file'''
            self.stdout.write(readme)
        else:
            manual = readme.split('\n')
            line = 0
            m_index = 0
            '''keep going until a non enter key is inputted, couldnt get the space key listener working'''
            while True:
                '''display 25 lines at a time and keep going only if the index is less than the length of manual'''
                while m_index < len(manual) and line < 26:
                    self.stdout.write(manual[m_index]+'\n')
                    line += 1
                    m_index += 1
                if not(input()) and m_index <len(manual):
                    '''reset line in order to run inner loop'''
                    line = 0
                    continue
                else:
                    break
                
        
    def do_dir(self,args):
        '''method callable by the user, may take a directory as an argument and lists out the contents of that
        directory'''
        try:
            self.set_stdout()
            if args and args[0] != '>':
                arg1 = args.split()[0]
                directory = os.path.realpath(arg1)
                content = os.listdir(directory)
            else:
                ''' if no arguments given list the current working directory's contents'''
                content = os.listdir()
            for fname in content:
                self.stdout.write(fname+'\n')
            '''catch two main exceptions, when directory given is nonexistent and name exists but
            its not a directory'''
        except NotADirectoryError:
            sys.stdout.write("{} is not a directory\n".format(arg1))
        except FileNotFoundError:
            sys.stdout.write("{} does not exist\n".format(arg1))
    
    def do_cd(self,args=None):
        #only does something if theres a given argument
        if args:
            try:
                os.chdir(args)
                self.pwd = os.getcwd()
            #catch the exception where the given directory does not exist
            except FileNotFoundError:
                print("File \"{}\" does not exist:".format(args))
            #catch the exception wherein the given argument exists but is not a directory
            except NotADirectoryError:
                print("\"{}\" is not a directory".format(args))
            finally:
                self.prompt = 'shell='+self.pwd+'> '
        else:
            self.stdout.write(self.pwd+'\n')

    def do_environ(self,args):
        dic = os.environ
        self.set_stdout()
        for key in dic.keys():
            self.stdout.write("{} {}\n".format(key,dic[key]))
        
    def do_echo(self,comment=None):
        '''a method that prints out or writes into a file the arguments given by the user''' 
        if comment:
            #get rid of any multiple spaces inbetween
            #get rid of the output redirection indicator so it's not written or displayed
            line = comment.split('>')[0] if self.overwrite else comment.split('>>')[0]
            line = " ".join(line.split())
            self.set_stdout()
            self.stdout.write(line+'\n')
    
    
    def do_pause(self,arg=None):
        if arg:
            self.stdout.write("pause does not take an argument, argument given ->{}\n".format(arg))
            return
        #enter an infinite loop which disables the user to call any commands until enter key is pressed
        pause = input("Press <Enter> to continue..")
        while pause:    #any non <Enter> key only input, keeps the loop going
            pause = input()
    
    
    def do_quit(self,arg=None):
        if arg:
            self.stdout.write("quit does not take an argument, argument given ->{}\n".format(arg))
            return
        response = input("Exit <Y/N>?\n")
        #accept both upper and lower case 'Y'
        if response == "Y".casefold():
            print("System Exit")
            raise SystemExit
        #do nothing if "Y" isn't pressed
        return
    
    def do_clr(self,arg=None):
        '''method that clears the shell/terminal'''
        if arg:
            self.stdout.write("clr does not take an argument, argument given ->{}\n".format(arg))
            return
        os.system('clear')
    
    @staticmethod
    def do_force_exit(self):
        '''used to exit the when batchfile is given'''
        print("System Exit")
        raise SystemExit

    def reset(self):
        '''called by postcmd(), ensure that self.stdout is sys.stdout before another command is called'''
        self.stdout = sys.stdout
        self.outFile = None

if __name__ == '__main__':
    shelly = MyShell()
    shelly.prompt = 'shell='+shelly.pwd+'> '
    shelly.cmdloop()