from sys import platform
from tkinter import messagebox
import paramiko
import subprocess


class SystemNotFound(Exception):
    pass


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
        if "TTL=128" in stdout.strip() or "ttl=128" in stdout.strip():
            session.system = "Win"
        else:
            session.system = "Unix"
        print(session.system) #### DEBUG


def decode_winShell(stdout):
    if type(stdout) == paramiko.ChannelFile:
        stdout = stdout.read()
    stdout = stdout.decode("437")
    return stdout.split("\n")