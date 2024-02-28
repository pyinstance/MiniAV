import os
import ctypes
import psutil
import requests
import time
import threading
import json

# -------------------------------- #
from PIL import Image
from getpass import getuser
from time import sleep
from colorama import Fore
from multiprocessing import Process
from watchdog.observers import Observer
from threading import Thread, Timer, Event
from watchdog.events import FileSystemEventHandler
# ------------------------------------------- #

# ---------------------------------------------- #
ip = requests.get("https://api.ipify.org").text
# ---------------------------------------------- #

b = Fore.LIGHTBLUE_EX
g = Fore.LIGHTGREEN_EX
w = Fore.WHITE
r = Fore.LIGHTRED_EX
rs = Fore.RESET


# ---------------------------------------------- #
class title:
    def __init__(self):
        self.start = time()
        self.exit = Event()
        self.updateTitle()

    def updateTitle(self):
        try:
            uptime = round(time() - self.start, 2)
            ctypes.windll.kernel32.SetConsoleTitleW(
                f"MiniAV | @Veal1 ~ @SyntheticCuhh ~ @2btz | Uptime: {uptime}'s"
            )
        except Exception as error:
            print(f"{Fore.LIGHTWHITE_EX}An Error Occured:{Fore.RESET} {error}")

        if not self.exit.is_set():
            Timer(0.1, self.updateTitle).start()

    def stop(self):
        self.exit.set()


def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ------------------------------------------- #

b = Fore.LIGHTBLUE_EX
r = Fore.RESET

# ------------------------------------------- #




print(
    f"""                                     
                  :---:::::::::::::::::::::                  
                  =========================                  
                 -==--------------------===:                 
                -===--=---------------=--===.                
              -====--=--=============-----====               
        .-=======---=-----------------------======-:         
        ======----=----------------------------======        
        ===----=-----------------------------=----===        
        ===------------------------------------=--===        {Fore.LIGHTBLUE_EX}                   Status {Fore.LIGHTWHITE_EX}: {Fore.LIGHTBLACK_EX}Running{Fore.RESET}
        ===------------------------------------=--===        {Fore.LIGHTBLUE_EX}                   Secure {Fore.LIGHTWHITE_EX}: {Fore.LIGHTBLACK_EX}Check{Fore.RESET}
        ===------------------------------------=--===        {Fore.LIGHTBLUE_EX}                   PC Name {Fore.LIGHTWHITE_EX}: {Fore.LIGHTBLACK_EX}{os.getenv('COMPUTERNAME')}{Fore.RESET}
        ===---------------{b}@@@@@@@@@@{r}------------=--===        {Fore.LIGHTBLUE_EX}                  System IP {Fore.LIGHTWHITE_EX}: {Fore.LIGHTBLACK_EX}{ip}{Fore.RESET}
        ===--=-----------{b}@@@@@@@@@@@@{r}-----------=--===        {Fore.LIGHTBLUE_EX}                  Copyright © Mini-AV {Fore.RESET}
        ===--=----------{b}@@@{r}---{b}@@{r}---{b}@@@{r}-------------==-        {Fore.LIGHTBLUE_EX}                  Developers {Fore.LIGHTWHITE_EX}: {Fore.LIGHTBLACK_EX}Veal {Fore.RESET}
        ===-------------{b}@@@@@@@@@@@@@@{r}------------===.        {Fore.LIGHTBLUE_EX}                  Developers {Fore.LIGHTWHITE_EX}: {Fore.LIGHTBLACK_EX}Synthetic{Fore.RESET}
        .===--=----------{b}@@@{r}------{b}@@@{r}----------=--===         {Fore.LIGHTBLUE_EX}                  Developers {Fore.LIGHTWHITE_EX}: {Fore.LIGHTBLACK_EX}Sacrifice{Fore.RESET}
         ===------------------------------------===-         
          ===--=--------------------------------===          
          :===--=------------------------------===           
           -===-------------------------------===            
            -===-------------------------=---===             
             :====--=----------------------====              
               ====---=-------------------===:               
                :====----=---------=----===-                 
                  :====---------=----=====                   
                    .=====---------====-                     
                       :=====---=====                        
                          -=======                           
                             -=:                             
"""
)


print(f"[{g}✓{w}] Loading Config For Whitelisted Programs...")
sleep(1)
print(f"[{g}✓{w}] Config Loaded Successfully!")
print(
    f"{Fore.WHITE}[ {Fore.LIGHTBLUE_EX}INFO {Fore.WHITE}] Mini-AV is monitoring the current sensitive Files : [ cookies ] [ passwords ]")
sleep(2)
print(
    f"{Fore.WHITE}[ {Fore.LIGHTBLUE_EX}INFO {Fore.WHITE}] Mini-AV is monitoring the current File For Changes Or Injection : [ Discord Cache ]")
sleep(2)
print(
    f"{Fore.WHITE}[ {Fore.LIGHTBLUE_EX}INFO {Fore.WHITE}] Mini-AV is monitoring the current Registery for Changes Or Injection : [ Discord Reg Keys ]")

# List of allowed programs
allowed_programs = ["cmd.exe", 
                    "powershell.exe", 
                    "explorer.exe", 
                    "chrome.exe", 
                    "firefox.exe", 
                    "opera.exe", 
                    "msedge.exe", 
                    "discord.exe", 
                    "python.exe", 
                    "Code.exe",
                    "ShareX.exe",
                    "pia-client.exe",
                    "Mullvad VPN.exe"]

def monitor_processes():
    while True:
        # Check for new processes
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'ppid']):
            try:
                process_name = proc.info['name']
                process_exe = proc.info['exe']
                parent_pid = proc.info['ppid']
                if process_exe:  # Check if process_exe is not None
                    process_size = os.path.getsize(process_exe) / (1024 * 1024)  # Convert to MB
                    if (process_size < 40 and is_user_initiated(parent_pid) and 
                        process_name not in allowed_programs and process_name != "DiscProc"):
                        pid = proc.pid
                        print(f"[{Fore.RED}X{Fore.WHITE}] [ {Fore.RED}ALERT {Fore.WHITE}] : {process_name} (PID: {pid})")
                        # Terminate the process
                        try:
                            proc.terminate()
                            print(f"[{g}+{w}] [ {g}INFO {g}] {w}Terminated {g}{process_name}{w} (PID: {g}{pid}) {w}File Size : {g}({process_size:.2f} MB)...")
                        except psutil.NoSuchProcess:
                            print(f"Process {process_name} (PID: {pid}) not found!")
            except (psutil.AccessDenied, psutil.NoSuchProcess, FileNotFoundError, TypeError):
                pass
        time.sleep(5)

# Function to check if a process is initiated by the user
def is_user_initiated(parent_pid):
    try:
        parent_process = psutil.Process(parent_pid)
        parent_name = parent_process.name()
        if parent_name in ['explorer.exe', 'cmd.exe']:
            return True
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
    return False

if __name__ == "__main__":
    process_monitor_thread = threading.Thread(target=monitor_processes)
    process_monitor_thread.start()

    process_monitor_thread.join()
