import tkinter as tk
import tkinter.ttk as ttk


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
        self.ent_lip = tk.Entry(buttonsframe, width=15)
        self.ent_lip.grid(column=0, row=2)
        lbl_sip = tk.Label(buttonsframe, text="Source IP", pady=5)
        lbl_sip.grid(column=0, row=3)
        self.ent_sip = tk.Entry(buttonsframe, width=15)
        self.ent_sip.grid(column=0, row=4)
        btn_new = ttk.Button(buttonsframe, text="New Session", command=lambda: controller.create_session())
        btn_new.grid(column=0, row=6)

        lbl_lpr = tk.Label(buttonsframe, text="Local port:", pady=5)
        lbl_lpr.grid(column=1, row=1)
        self.ent_lpr = tk.Entry(buttonsframe, width=15)
        self.ent_lpr.grid(column=1, row=2)
        lbl_spr = tk.Label(buttonsframe, text="Source port:", pady=5)
        lbl_spr.grid(column=1, row=3)
        self.ent_spr = tk.Entry(buttonsframe, width=15)
        self.ent_spr.grid(column=1, row=4)
        parent.create_menu(frame=buttonsframe, column=1, row=5, session=parent)

        lbl_ctp = tk.Label(buttonsframe, text="Connection type:", pady=5)
        lbl_ctp.grid(column=2, row=1)
        self.selected = tk.IntVar()
        rad_bth = tk.Radiobutton(buttonsframe, text="Both", value=0, variable=self.selected)
        rad_bth.grid(column=2, row=2)
        rad_tcp = tk.Radiobutton(buttonsframe, text="TCP", value=1, variable=self.selected)
        rad_tcp.grid(column=2, row=3)
        rad_udp = tk.Radiobutton(buttonsframe, text="UDP", value=2, variable=self.selected)
        rad_udp.grid(column=2, row=4)
        btn_lout = ttk.Button(buttonsframe, text="Log Out", command=lambda: parent.logout_session())
        btn_lout.grid(column=2, row=6)

        lbl_stt = tk.Label(buttonsframe, text="State")
        lbl_stt.grid(column=3, row=1)
        self.cmb_stt = ttk.Combobox(buttonsframe)
        self.cmb_stt.grid(column=3, row=2)
        self.cmb_stt['values'] = ("All", "ESTAB", "LISTEN", "TIME_WAIT", "CLOSE_WAIT", "FIN_WAIT", "LAST_ACK",
                                  "CLOSING", "CLOSE", "SYN_SENT", "SYN_RECV", "UNCONN")
        self.cmb_stt.current(0)
        lbl_pid = tk.Label(buttonsframe, text="PID:")
        lbl_pid.grid(column=3, row=3)
        self.ent_pid = tk.Entry(buttonsframe, width=15)
        self.ent_pid.grid(column=3, row=4)

        inv_lbl = tk.Label(buttonsframe, text="", padx=7)
        inv_lbl.grid(column=4, row=2)
        btn_ref = ttk.Button(buttonsframe, text="Refresh", command=lambda: self.update_list(parent, False))
        btn_ref.grid(column=5, row=2)
        btn_src = ttk.Button(buttonsframe, text="Search", command=lambda: self.update_list(parent, True))
        btn_src.grid(column=5, row=3)
        btn_rst = ttk.Button(buttonsframe, text="Reset", command=lambda: self.rst_ftr())
        btn_rst.grid(column=5, row=4)

    def get_filtr(self):
        return {"Source IP": self.ent_sip.get(), "Local IP": self.ent_lip.get(), "Local port": self.ent_lpr.get(),
                "Source port": self.ent_spr.get(), "PID": self.ent_pid.get(), "Protocol": self.selected.get(),
                "State": self.cmb_stt.get()}

    def filtr_prot(self, data):
        ftr_data = []
        choice = self.parameters["Protocol"]
        for line in data:
            if choice == 1 and line.lower().split().count("tcp"):
                ftr_data.append(line)
            elif choice == 2 and line.lower().split().count("udp"):
                ftr_data.append(line)
            elif choice == 0:
                ftr_data.append(line)
        return ftr_data

    def filtr_ip(self, data, parent, uindex, windex, key):
        ftr_data = []
        if parent.system == "Unix":
            index = uindex
        elif parent.system == "Win":
            index = windex
        for line in data:
            if "IP" in key:
                if self.parameters[key] in line.split()[index]:
                    ftr_data.append(line)
            elif "port" in key:
                if self.parameters[key] in line.split()[index].split(":")[-1]:
                    ftr_data.append(line)
        return ftr_data

    def filtr_pid(self, data, parent):
        ftr_data = []
        for line in data:
            if parent.system == "Unix" and "pid=" + self.parameters["PID"] in line.split()[-1]:
                ftr_data.append(line)
            elif parent.system == "Win" and self.parameters["PID"] in line.split()[-1]:
                ftr_data.append(line)
        return ftr_data

    def filtr_state(self, data, parent):
        ftr_data = []
        for line in data:
            if self.parameters["State"] in line.split()[1] and parent.system == "Unix":
                ftr_data.append(line)
            elif self.parameters["State"] in line.split()[-2] and parent.system == "Win":
                ftr_data.append(line)
            elif self.parameters["State"] == "UNCONN" and len(line.split()) < len(data[0].split()):
                ftr_data.append(line)
        return ftr_data


    def filtr_all(self, data, parent):
        header = data[0]
        data = data[1:-1]
        if self.parameters["Protocol"] != "":
            data = self.filtr_prot(data)
        if self.parameters["Local IP"] != "":
            data = self.filtr_ip(data, parent, 4, 1, "Local IP")
        if self.parameters["Source IP"] != "":
            data = self.filtr_ip(data, parent, 5, 2, "Source IP")
        if self.parameters["Local port"] != "":
            data = self.filtr_ip(data, parent, 4, 1, "Local port")
        if self.parameters["Source port"] != "":
            data = self.filtr_ip(data, parent, 5, 2, "Source port")
        if self.parameters["PID"] != "":
            data = self.filtr_pid(data, parent)
        if self.parameters["State"] != "All":
            data = self.filtr_state(data, parent)
        data.insert(0, header)
        return data


    def rst_ftr(self):
        self.ent_sip.delete(0, tk.END)
        self.ent_lip.delete(0, tk.END)
        self.ent_lpr.delete(0, tk.END)
        self.ent_spr.delete(0, tk.END)
        self.ent_pid.delete(0, tk.END)
        self.selected.set(0)

    def dw_socketlist(self, parent):
        pass

    def update_list(self, parent, new):
        self.socketbox.delete(0, tk.END)
        if new:
           self.parameters = self.get_filtr()
        data = self.filtr_all(self.dw_socketlist(parent), parent)
        for line in data:
            self.socketbox.insert(tk.END, line)
