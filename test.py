from playsound import playsound
import os, pythoncom, time, wmi
from threading import Thread


def listener():
    pythoncom.CoInitialize()
    c = wmi.WMI()
    process_watcher = c.Win32_Process.watch_for("creation")
    while True:
        new_process = process_watcher()
        if new_process.Caption == 'myApplication.exe':
            playsound()
            exit()
        time.sleep(1)


t = Thread(target=listener)
t.daemon = True
t.start()
