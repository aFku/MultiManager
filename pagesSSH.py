from templates import *
from globalMeth import *


class Process_ssh(Process):
    def __init__(self, parent, controller):
        Process.__init__(self, parent, controller)
        print("SSH Session") #########DEBUG

    def dw_processlist(self, parent):
        if parent.system == "Unix":
            stdin, stdout, stderr = parent.ssh.exec_command("ps -aux")
        elif parent.system == "Win":
            stdin, stdout, stderr = parent.ssh.exec_command("cmd.exe /c TASKLIST /v")
            stdout = decode_winShell(stdout)
        else:
            stdout = None
        return stdout

    def kill(self, parent, choice):
        pid = self.getpid(self.processbox.get(tk.ANCHOR))
        try:
            if parent.system == "Unix":
                parent.ssh.exec_command("kill -" + str(choice) + " " + pid)
            elif parent.system == "Win":
                parent.ssh.exec_command("taskkill " + choice + " /pid " + pid)
            else:
                raise()
        except:
            print("Can`t kill process!")
        else:
            self.update_list(parent)


class Sockets_ssh(Sockets):
    def __init__(self, parent, controller):
        Sockets.__init__(self, parent, controller)
        self.update_list(parent)

    def dw_socketlist(self, parent):
        if parent.system == "Unix":
            stdin, stdout, stderr = parent.ssh.exec_command("netstat -pnltSu")
        elif parent.system == "Win":
            stdin, stdout, stderr = parent.ssh.exec_command("netstat -anoq")
        else:
            stdout = None
        return decode_winShell(stdout)