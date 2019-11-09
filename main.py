from sys import platform
import tkinter as tk
import tkinter.ttk as ttk
import paramiko
import subprocess
from tkinter import messagebox


####NOWE FUNKCJONALNOSCI


class SystemNotFound(Exception):
    pass

######################################## LOGIN PAGE ################################################


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        controller.tab_control.select(controller.sessions[parent.session_number])


        ip_lbl = tk.Label(self, text="IPv4 Address:", pady=5, padx=5)
        ip_lbl.grid(column=0, row=0, sticky=tk.E)
        ip_ent = tk.Entry(self, width=20)
        ip_ent.grid(column=0, row=1, sticky=tk.E)

        user_lbl = tk.Label(self, text="Login:", pady=5, padx=5)
        user_lbl.grid(column=0, row=2)
        user_ent = tk.Entry(self, width=20)
        user_ent.grid(column=0, row=3)

        pass_lbl = tk.Label(self, text="Password:", pady=5, padx=5)
        pass_lbl.grid(column=0, row=4)
        pass_ent = tk.Entry(self, width=20, show="*")
        pass_ent.grid(column=0, row=5)

        ssh_btn = ttk.Button(self, text="Login via ssh", command=lambda: ssh_login(ip_ent, user_ent, pass_ent, parent, err_lbl))
        ssh_btn.grid(column=0, row=6)
        local_btn = ttk.Button(self, text="Login Local", command=lambda: local_login(parent, err_lbl))
        local_btn.grid(column=0, row=7)
        logout_btn = ttk.Button(self, text="Logout", command=parent.logout_session)
        logout_btn.grid(column=0, row=8)

        err_lbl = tk.Label(self, text="", font=("Arial", 10), padx=10, pady=10)
        err_lbl.grid(column=0, row=10)

        new_btn = ttk.Button(self, text="New Session", command=controller.create_session)
        new_btn.grid(column=0, row=9)

        controller.tab_control.select(controller.sessions[parent.session_number])

######################################### UTILITIES TEMPLATES ##########################################################

class Process(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.processbox = tk.Listbox(self, width=110, height=15, selectmode=tk.SINGLE)
        self.processbox.grid(column=0, row=0)
        self.update_list(parent)
        if parent.system == "Unix":
            self.gui_linux(parent, controller)
        elif parent.system == "Win":
            self.gui_win(parent, controller)
        else:
            pass

    def update_list(self, parent):
        self.processbox.delete(0, tk.END)
        for line in self.dw_processlist(parent):
            self.processbox.insert(tk.END, line)

    def kill(self, parent, choice):
        pass

    def dw_processlist(self):
        pass

    @staticmethod
    def getpid(line):
        pid = line.split(" ")
        pid = [element for element in pid if element != '']
        return pid[1]

    def gui_linux(self, parent, controller):
        btn_ref = ttk.Button(self, text="Refresh", command=lambda: self.update_list(parent))
        btn_ref.grid(column=0, row=1, pady=5)
        btn_kill = ttk.Button(self, text="KILL", command=lambda: self.kill(parent, 9))
        btn_kill.grid(column=0, row=2, sticky=tk.W, padx=80)
        btn_hup = ttk.Button(self, text="Hang Up", command=lambda: self.kill(parent, 1))
        btn_hup.grid(column=0, row=2, sticky=tk.E, padx=80)
        btn_int = ttk.Button(self, text="Keyboard interrupt", command=lambda: self.kill(parent, 2))
        btn_int.grid(column=0, row=2)
        btn_ter = ttk.Button(self, text="Termination", command=lambda: self.kill(parent, 15))
        btn_ter.grid(column=0, row=3, sticky=tk.W, padx=80)
        btn_stp = ttk.Button(self, text="STOP", command=lambda: self.kill(parent, 19))
        btn_stp.grid(column=0, row=3, sticky=tk.E, padx=80)
        btn_stp = ttk.Button(self, text="Resume", command=lambda: self.kill(parent, 18))
        btn_stp.grid(column=0, row=3)
        btn_lout = ttk.Button(self, text="Log Out", command=lambda: parent.logout_session())
        btn_lout.grid(column=0, row=4)
        btn_new = ttk.Button(self, text="New Session", command=lambda: controller.create_session())
        btn_new.grid(column=0, row=5)
        parent.create_menu(frame=self, column=0, row=6, session=parent)

    def gui_win(self, parent, controller):
        btn_ref = ttk.Button(self, text="Refresh", command=lambda: self.update_list(parent))
        btn_ref.grid(column=0, row=1)
        btn_kill = ttk.Button(self, text="Send termination signal", command=lambda: self.kill(parent, ""))
        btn_kill.grid(column=0, row=1, sticky=tk.W)
        btn_force = ttk.Button(self, text="Forcefully termination", command=lambda: self.kill(parent, "/f"))
        btn_force.grid(column=0, row=1, sticky=tk.E)
        btn_chld = ttk.Button(self, text="Termination of process and any child started by it",
                              command=lambda: self.kill(parent, "/t"))
        btn_chld.grid(column=0, row=2, sticky=tk.W)
        btn_all = ttk.Button(self, text="Forcefully termination of process and any its child",
                             command=lambda: self.kill(parent, "/f /t"))
        btn_all.grid(column=0, row=2, sticky=tk.E)
        btn_lout = ttk.Button(self, text="Log Out", command=lambda: parent.logout_session())
        btn_lout.grid(column=0, row=3)
        btn_new = ttk.Button(self, text="New Session", command=lambda: controller.create_session())
        btn_new.grid(column=0, row=2)
        parent.create_menu(frame=self, column=0, row=4, session=parent)


class Sockets(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        listframe = tk.Frame(self)
        buttonsframe = tk.Frame(self)
        listframe.grid(column=0, row=0)
        buttonsframe.grid(column=0, row=1, sticky=tk.W+tk.E+tk.N+tk.S)
        self.socketbox = tk.Listbox(listframe, width=110, height=15, selectmode=tk.SINGLE)
        self.socketbox.grid(column=0, row=0)

        lbl_fltr = tk.Label(buttonsframe, text="Filters:")
        lbl_fltr.grid(column=0, row=0)
        lbl_lip = tk.Label(buttonsframe, text="Local IP:", pady=5)
        lbl_lip.grid(column=0, row=1)
        ent_lip = tk.Entry(buttonsframe, width=15)
        ent_lip.grid(column=0, row=2)
        lbl_sip = tk.Label(buttonsframe, text="Source IP", pady=5)
        lbl_sip.grid(column=0, row=3)
        ent_sip = tk.Entry(buttonsframe, width=15)
        ent_sip.grid(column=0, row=4)
        btn_new = ttk.Button(buttonsframe, text="New Session", command=lambda: controller.create_session())
        btn_new.grid(column=0, row=6)

        btn_ref = ttk.Button(buttonsframe, text="Refresh", command=lambda: self.update_list(parent))
        btn_ref.grid(column=1, row=0)
        lbl_lpr = tk.Label(buttonsframe, text="Local port:", pady=5)
        lbl_lpr.grid(column=1, row=1)
        ent_lpr = tk.Entry(buttonsframe, width=15)
        ent_lpr.grid(column=1, row=2)
        lbl_spr = tk.Label(buttonsframe, text="Source port:", pady=5)
        lbl_spr.grid(column=1, row=3)
        ent_spr = tk.Entry(buttonsframe, width=15)
        ent_spr.grid(column=1, row=4)
        parent.create_menu(frame=buttonsframe, column=1, row=5, session=parent)

        lbl_ctp = tk.Label(buttonsframe, text="Connection type:", pady=5)
        lbl_ctp.grid(column=2, row=1)
        selected = tk.IntVar()
        rad_bth = tk.Radiobutton(buttonsframe, text="Both", value=0, variable=selected)
        rad_bth.grid(column=2, row=2)
        rad_tcp = tk.Radiobutton(buttonsframe, text="TCP", value=1, variable=selected)
        rad_tcp.grid(column=2, row=3)
        rad_udp = tk.Radiobutton(buttonsframe, text="UDP", value=2, variable=selected)
        rad_udp.grid(column=2, row=4)

        lbl_stt = tk.Label(buttonsframe, text="State")
        btn_src = ttk.Button(buttonsframe, text="Search")
        btn_src.grid(column=4, row=0)
        btn_rst = ttk.Button(buttonsframe, text="Reset")
        btn_rst.grid(column=3, row=0)



    def dw_socketlist(self, parent):
        pass

    def update_list(self, parent):
        self.socketbox.delete(0, tk.END)
        for line in self.dw_socketlist(parent):
            self.socketbox.insert(tk.END, line)





############################################# SSH PAGES ###############################################################


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
            stdin, stdout, stderr = parent.ssh.exec_command("ss -pnltu")
        elif parent.system == "Win":
            stdin, stdout, stderr = parent.ssh.exec_command("netstat -anoq")
        else:
            stdout = None
        return decode_winShell(stdout)




##################################################### LOCAL PAGES ##################################################

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

###################################################### GLOBAL VAR ##################################################


session_counter = 0
pages = ((Process_ssh, Sockets_ssh), (Process_local, Sockets_local))


#################################################### GLOBAL RANGE METHODS #############################################


def read_system():
    try:
        system = platform
        if system in ("win32", "cygwin"):
            return "Win"
        elif system in ("aix", "linux", "freebsd"):
            return "Unix"
        else:
            raise SystemNotFound
    except SystemNotFound:
        messagebox.showerror("System not found!", "Sorry, but we can`t find out your system.\n"
                                                  "Please contact with software vendor!", )
        exit()


def ssh_login(ip, username, password, session, err_lbl):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:

        ssh.connect(ip.get(), username=username.get(), password=password.get(), port=22)
        session.system = read_system()
        check_remote_os(ip.get(), session)
    except:
        err_lbl.configure(text="Wrong Data!")
    else:
        session.ssh = ssh
    try:
        session.create_frame("Utilities_remote")
    except:
        err_lbl.configure(text="Something gone wrong!")


def local_login(session, err_lbl):
    try:
        session.system = read_system()
        session.create_frame("Utilities_local")
    except:
        err_lbl.configure(text="Something gone wrong!")


def check_remote_os(ip, session):
    try:
        if session.system == "Win":
            stdout = subprocess.check_output(["ping", str(ip)]).decode()
        elif session.system == "Unix":
            stdout = subprocess.check_output(["ping", "-c", "3", str(ip)]).decode()
    except:
        print("Can`t find out os of " + ip)
        session.logout_session()
    else:
        if "TTL=128" in stdout.strip():
            session.system = "Win"
        else:
            session.system = "Unix"
        print(session.system) #### DEBUG


def decode_winShell(stdout):
    if type(stdout) == paramiko.ChannelFile:
        stdout = stdout.read()
    stdout = stdout.decode("437")
    return stdout.split("\n")



############################################ SESSION CLASS ########################################################


class Session(tk.Frame):
    def __init__(self, controller, *args, **kwargs):
        global session_counter
        tk.Frame.__init__(self, *args)
        self.pack()
        self.session_number = session_counter
        session_counter += 1
        self.system = None
        self.controller = controller
        self.frames = {}
        self.ssh = None
        controller.tab_control.add(self, text="Session " + str(self.session_number))
        controller.sessions.append(self)
        self.create_frame("Login")

    def create_frame(self, choice):
        global pages
        if choice == "Login":
            frame = LoginPage(self, self.controller)
            self.frames[LoginPage] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        elif choice == "Utilities_remote":
            for page in pages[0]:
                frame = page(self, self.controller)
                self.frames[page] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame(pages[0][0])
        elif choice == "Utilities_local":
            for page in pages[1]:
                frame = page(self, self.controller)
                self.frames[page] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame(pages[1][0])

    def show_frame(self, page):
        frame = self.frames[page]
        frame.lift()

    def logout_session(self):
        if self.ssh != None:
            self.ssh.close()
        self.destroy()
        self.controller.sessions[self.session_number] = None
        if len([n for n in self.controller.sessions if n == None]) == len(self.controller.sessions):
            self.controller.destroy()

    def create_menu(self, frame, column, row, session):
        menu = ttk.Combobox(frame)
        if session.ssh == None:
            access = 1
        else:
            access = 0
        values = ("Process Manager", "Sockets Display")
        try:
            if access == 1:
                menu['values'] = values
            elif access == 0:
                menu['values'] = values
            else:
                raise ValueError()
        except ValueError:
            print("SSH check error!")
        else:
            menu.set("---Page---")
            lbl_menu = tk.Label(frame, text="Menu:")
            go_to_btn = tk.Button(frame, text="Go to!", command=lambda: self.show_frame(pages[access][menu.current()]))
            lbl_menu.grid(column=column, row=row)
            menu.grid(column=column, row=row+1)
            go_to_btn.grid(column=column, row=row+2, pady=2)







################################################### CONTROLER CLASS ###################################################


class Controller(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("667x600")
        self.title("ProcessManager")
        self.sessions = []
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand=1, fill="both")
        self.create_session()

    def create_session(self):
        x = Session(self)

    @staticmethod
    def __conv_resolution(res):
        tmp = res.split("x")
        for index, each in enumerate(tmp):
            tmp[index] = str(round(int(each) / 2))
        return 'x'.join(tmp)


if __name__ == "__main__":
    x = Controller()
    x.mainloop()