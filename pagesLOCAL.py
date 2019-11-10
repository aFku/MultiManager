from templates import *
from globalMeth import *


class Process_local(Process):
    def __init__(self, parent, controller):
        Process.__init__(self, parent, controller)
        print("Local Session")####### DEBUG

    def dw_processlist(self, parent):
        print(parent.system)
        if parent.system == "Unix":
            stdout = decode_winShell(subprocess.check_output(["ps", "-aux"]))
        elif parent.system == "Win":
            stdout = decode_winShell(subprocess.check_output("TASKLIST", shell=True))
        else:
            stdout = None
        return stdout

    def kill(self, parent, choice):
        pid = self.getpid(self.processbox.get(tk.ANCHOR))
        try:
            if parent.system == "Unix":
                subprocess.call("kill -" + str(choice) + " " + pid, shell=True)
            elif parent.system == "Win":
                subprocess.call("taskkill " + choice + " /pid " + pid, shell=True)
            else:
                raise()
        except:
            print("Can`t kill process!")
        else:
            self.update_list(parent)


class Sockets_local(Sockets):
    def __init__(self, parent, controller):
        Sockets.__init__(self, parent, controller)
        self.update_list(parent)

    def dw_socketlist(self, parent):
        if parent.system == "Unix":
            stdout = decode_winShell(subprocess.check_output(["ss", "-pnltu"]))
        elif parent.system == "Win":
            stdout = decode_winShell(subprocess.check_output(["netstat", "-anoq"]))
        else:
            stdout = None
        return stdout