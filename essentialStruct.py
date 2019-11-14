import tkinter as tk
import tkinter.ttk as ttk
from globalMeth import *
from pagesSSH import Process_ssh, Sockets_ssh
from pagesLOCAL import Process_local, Sockets_local



class Session(tk.Frame):
    def __init__(self, controller, *args, **kwargs):
        tk.Frame.__init__(self, *args)
        self.pack()
        self.session_number = controller.session_counter
        controller.session_counter += 1
        self.system = None
        self.controller = controller
        self.frames = {}
        self.ssh = None
        controller.tab_control.add(self, text="Session " + str(self.session_number))
        controller.sessions.append(self)
        self.create_frame("Login")

    def create_frame(self, choice):
        if choice == "Login":
            try:
                frame = LoginPage(self, self.controller)
                self.frames[LoginPage] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            except:
                print("Cannot create Login Page!")
                self.logout_session()
        elif choice == "Utilities_remote":
            for page in self.controller.pages[0]:
                try:
                    frame = page(self, self.controller)
                    self.frames[page] = frame
                    frame.grid(row=0, column=0, sticky="nsew")
                except:
                    print("Cannot create one of the remote utilities page!")
                    self.logout_session()
            self.show_frame(self.controller.pages[0][0])
        elif choice == "Utilities_local":
            for page in self.controller.pages[1]:
                try:
                    frame = page(self, self.controller)
                    self.frames[page] = frame
                    frame.grid(row=0, column=0, sticky="nsew")
                except:
                    print("Cannot create one of the local utilities page!")
                    self.logout_session()
            self.show_frame(self.controller.pages[1][0])

    def show_frame(self, page):
        frame = self.frames[page]
        frame.lift()

    def logout_session(self):
        if self.ssh != None:
            try:
                self.ssh.close()
            except:
                print("Cannot close ssh connection!")
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
            if access == 1 or access == 0:
                menu['values'] = values
            else:
                raise ValueError()
        except ValueError:
            print("SSH check error!")
        else:
            menu.set("---Page---")
            lbl_menu = tk.Label(frame, text="Menu:")
            go_to_btn = tk.Button(frame, text="Go to!", command=lambda: self.show_frame(self.controller.pages[access][menu.current()]))
            lbl_menu.grid(column=column, row=row)
            menu.grid(column=column, row=row+1)
            go_to_btn.grid(column=column, row=row+2, pady=2)


class Controller(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("667x600")
        self.title("ProcessManager")
        self.sessions = []
        self.session_counter = 0
        self.pages = ((Process_ssh, Sockets_ssh), (Process_local, Sockets_local))
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