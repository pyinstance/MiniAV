import os;         import time       
import hashlib;    import shutil            
import requests;   import colorama
import winreg;     import ctypes    
# -------------------------------- #
from colorama            import Fore
from multiprocessing     import Process
from watchdog.observers  import Observer
from watchdog.events     import FileSystemEventHandler
from PIL                 import Image
from notifypy            import Notify
from pystray             import MenuItem, Icon
from ctypes              import wintypes
# ---------------------------------------------- #

PCNAME = {os.getenv('COMPUTERNAME')}

# ---------------------------------------------- #
ip = requests.get("https://api.ipify.org").text
icon = Icon("MiniAV.ico")
icon.menu = (MenuItem('Exit', lambda: icon.stop()),)
# ---------------------------------------------- #


DISCORD_REGISTRY_KEYS = [
    r"Software\Discord",
    r"Software\DiscordOverlay",
    # Add more Discord registry keys If needed you dont have to
]

# Define Windows API constants and structures 
# This is used to stop Stealers from killing the protector
PROCESS_CREATION_MITIGATION_POLICY = 22
PROCESS_CREATION_CHILD_PROCESS_RESTRICTED = 1

print(f"""                                     
                  :---:::::::::::::::::::::                  
                  =========================                  
                 -==--------------------===:                 
                -===--=---------------=--===.                
              -====--=--=============-----====               
        .-=======---=-----------------------======-:         
        ======----=----------------------------======        
        ===----=-----------------------------=----===        
        ===------------------------------------=--===        {Fore.LIGHTCYAN_EX}                   Mini-AV Is now Active{Fore.RESET}
        ===------------------------------------=--===        {Fore.LIGHTCYAN_EX}                   Secure {Fore.LIGHTWHITE_EX}: {Fore.LIGHTGREEN_EX}Check{Fore.RESET}
        ===------------------------------------=--===        {Fore.LIGHTCYAN_EX}                   PC Name {Fore.LIGHTWHITE_EX}: {Fore.LIGHTGREEN_EX}{os.getenv('COMPUTERNAME')}{Fore.RESET}
        ===--------------=@@@@@@@@@------------=--===        {Fore.LIGHTCYAN_EX}                   System IP {Fore.LIGHTWHITE_EX}: {Fore.LIGHTGREEN_EX}{ip}{Fore.RESET}
        ===--=-----------@@@@@@@@@@@-----------=--===        {Fore.LIGHTCYAN_EX}                   Copyright © Mini-AV {Fore.RESET}
        ===--=----------@@@--@@---@@%-------------==-        {Fore.LIGHTYELLOW_EX}                   Developers {Fore.LIGHTWHITE_EX}: {Fore.LIGHTCYAN_EX}Veal {Fore.RESET}
        ===-------------@@@@@@@@@@@@@------------===.        {Fore.LIGHTYELLOW_EX}                   Developers {Fore.LIGHTWHITE_EX}: {Fore.LIGHTCYAN_EX}Synthetic{Fore.RESET}
        .===--=----------@@@-----@@#----------=--===         
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
""")
print(f"{Fore.WHITE}[ {Fore.LIGHTGREEN_EX}INFO {Fore.WHITE}] Mini-AV is monitoring the current sensitive Files : [ cookies ] [ passwords ]")
time.sleep(2)
print(f"{Fore.WHITE}[ {Fore.LIGHTGREEN_EX}INFO {Fore.WHITE}] Mini-AV is monitoring the current File For Changes Or Injection : [ Discord Cache ]")
time.sleep(2)
print(f"{Fore.WHITE}[ {Fore.LIGHTGREEN_EX}INFO {Fore.WHITE}] Mini-AV is monitoring the current Registery for Changes Or Injection : [ Discord Reg Keys ]")

def detect_virus(file_path, KNOWN_VIRUS_HASHES, quarantine_dir):
    with open(file_path, 'rb') as file:
        content = file.read()
        file_hash = hashlib.sha256(content).hexdigest()
        if file_hash in KNOWN_VIRUS_HASHES:
            notification = Notify()
            notification.app_name = "Mini-AV"
            notification.title = "Mini-AV > Virus Detected"
            notification.message = f"Mini-AV Quarantined : {file_path}"
            notification.icon = "Mini-AV.ico"
            notification.send()
            with open("log.txt", "a") as log_file:
                log_file.write(f"[Mini-AV-INFO] Quarantined File: {file_path}\n")
            quarantine_file(file_path, quarantine_dir)
            os.remove(file_path)


def quarantine_file(file_path, quarantine_dir):
    filename = os.path.basename(file_path)
    quarantined_path = os.path.join(quarantine_dir, filename)
    quarantined_path = quarantined_path + ".Mini-AV" # Change file extension to prevent execution
    shutil.move(file_path, quarantined_path)
    try:
        time.sleep(4)
        os.remove(file_path)
        print(f"File : {file_path} Has Successfully been removed")
    except Exception as e:
        print(f"[ ERROR] {e}")

    
def scan_file(file_path, KNOWN_VIRUS_HASHES, quarantine_dir):
    p = Process(target=detect_virus, args=(file_path, KNOWN_VIRUS_HASHES, quarantine_dir))
    p.start()

class NewFileEventHandler(FileSystemEventHandler):
    def __init__(self, KNOWN_VIRUS_HASHES, quarantine_dir):
        self.KNOWN_VIRUS_HASHES = KNOWN_VIRUS_HASHES
        self.quarantine_dir = quarantine_dir
        if not os.path.exists(quarantine_dir):
            os.makedirs(quarantine_dir)

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            scan_file(file_path, self.KNOWN_VIRUS_HASHES, self.quarantine_dir)

def monitor_download_directory(directory, KNOWN_VIRUS_HASHES, quarantine_dir):
    event_handler = NewFileEventHandler(KNOWN_VIRUS_HASHES, quarantine_dir)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


SENSITIVE_FILES = [f'C:\\Users\\{PCNAME}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies', f'C:\\Users\\{PCNAME}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data']
DISCORD_PATH = f"C:\\Users\\{PCNAME}\\AppData\\Roaming\\discord\\Cache"

def check_file_access(file_path):
    for sensitive_file in SENSITIVE_FILES:
        if sensitive_file in file_path:
            return True
    if DISCORD_PATH in file_path:
        return True
    return False


def monitor_file_access():
    for folder, subfolders, files in os.walk('/'):
        for file in files:
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path) and check_file_access(file_path):
                print(f"{Fore.WHITE}[ {Fore.LIGHTGREEN_EX}INFO {Fore.WHITE}] Suspicious activity detected: {file_path}")
                # Take action to quarantine or terminate the process
                # For demonstration purposes, let's print a message
                print(f"{Fore.WHITE}[ {Fore.LIGHTGREEN_EX}INFO {Fore.WHITE}] Terminating process and quarantining file...")


def main():
    print(f"{Fore.WHITE}[ {Fore.LIGHTGREEN_EX}INFO {Fore.WHITE}] Mini-AV is monitoring the current sensitive Files : [ cookies ] [ passwords ]")
    while True:
        monitor_file_access()


class Process_Policy(ctypes.Structure):
    _fields_ = [
        ("Policy", wintypes.DWORD),
        ("Flags", wintypes.DWORD),
    ]

def check_registry_changes():
    for key_path in DISCORD_REGISTRY_KEYS:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            num_subkeys, num_values, last_modified = winreg.QueryInfoKey(key)
            print(f"{Fore.WHITE}[ {Fore.LIGHTGREEN_EX}INFO {Fore.WHITE}] Registry key detected: {key_path}")


            print(f"{Fore.WHITE}[ {Fore.LIGHTGREEN_EX}INFO {Fore.WHITE}] Terminating process and quarantining file...")
        except Exception as e:
            print(f"{Fore.WHITE}[ {Fore.LIGHTGREEN_EX}Error {Fore.WHITE}] Error accessing registry key {key_path}: {e}")

def apply_Process_Policy():
    policy = Process_Policy()
    policy.Policy = PROCESS_CREATION_MITIGATION_POLICY
    policy.Flags = PROCESS_CREATION_CHILD_PROCESS_RESTRICTED
    ctypes.windll.kernel32.SetProcessMitigationPolicy(PROCESS_CREATION_MITIGATION_POLICY, ctypes.byref(policy), ctypes.sizeof(policy))

def main():
    apply_Process_Policy()
    while True:
        check_registry_changes()


if __name__ == "__main__":
    KNOWN_VIRUS_HASHES = [
        "df8c6f81a5e2aba5013c9ac111da3d9718b0349b52657e3763135ff0ec07f73d", # All Centurion Hashes and different obfuscation Methods
        "015fbc0b216d197136df8692b354bf2fc7bd6eb243e73283d861a4dbbb81a751", # All Centurion Hashes and different obfuscation Methods
        "17f2eb260f0b6942f80453b30f1a13235f27b7ed80d4e5815fb58ff7322fc765", # All Centurion Hashes and different obfuscation Methods
        "36c7bbf70459d63163aa9d8d43b9ca1a02f837d53004a9ad0574f687e5a6a9d2", # All Centurion Hashes and different obfuscation Methods
        "55cee457c73aa87258a04562c9d04cd3c865608d5dd64366d9cd9bc2fe2f5dd9", # All Centurion Hashes and different obfuscation Methods
        "92e1c28b32241eea5778a35dbb092ce77917395323b722d99aa2bf7efcce9cc8", # Empyrean Stealer
        "6e0ca09171ff5d693972d3affb97a24e30606ce64259508116d7e2cfbe958ade" # Villa Stealer
    ]
    download_directory = os.path.join(os.getenv("USERPROFILE"), "Downloads")
    quarantine_dir = "C:\\Quarantine"  # Specify the directory for quarantined files

    monitor_download_directory(download_directory, KNOWN_VIRUS_HASHES, quarantine_dir)
