#Name: Kyle Angelo Villanueva
#17428562


import os,sys
_dic = {'dir':"def do_dir(self,args)\n|\tLists the contents of the current working directory or given directory.\n|\tCan be given an output file; writes into the file.\n|\n",
    'cd':"def do_cd(self,args)\n|\tAccepts one argument,\n|\tchanges the current working directory to the given argument.\n|\tRaises an exception if the given\n|\tfolder does exist or if it's not a directory.\n|\n",
    'echo':"def do_echo(self,args)\n|\tAccepts an argument <- a string and displays it on the terminal.\n|\tSupports output redirection, writes the argument into the given file.\n|\n",
    'pause':"def do_pause(self,arg=None)\n|\tPauses the shell until the user presses the <Enter> key.\n|\n",
    'env':"def do_environ(self,args)\n|\tPrints out the enviroment variables.\n|\tSupports output redirection.\n|\tWrites on the file given as an argument.\n|\n",
    'clr':"def do_clear(self,arg=None)\n|\tAccepts no arguments.\n|\tClears the terminal.\n|\n",
    'quit':"def do_quit(self,arg=None)\n|\tAccepts no arguments.\n|\tExits the shell if Y is entered.\n|\tReturns to the terminal if any other key is entered.\n|\n"}


'''provides the callable help method in MyShell'''
class Help():
    
    def dir(self):
        return _dic['dir']
    
    def cd(self):
        return _dic['cd']
    
    def echo(self):
        return _dic['echo']
    
    def pause(self):
        return _dic['pause']
    
    def environ(self):
        return _dic['env']
    
    def clear(self):
        return _dic['clr']
    
    def quit(self):
        return _dic['quit']

if __name__ == '__main__':
    #test
    screen = ''
    footer = '|---press<Enter> for more---'
    for key in _dic:
        os.system('clear')
        screen += _dic[key]
        sys.stdout.write(screen)
        sys.stdout.write(footer)
        if not(input()):
            continue
        else:
            break
        