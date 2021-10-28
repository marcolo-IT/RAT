# Remote Access Trojan

Inside this repository, there are five scripts.

1. arp_scanner.py will help identifying the IP address and MAC address of each local device (You will need this to find your local target)
2. maskMAC.py changes the MAC address to a random one (Use this to hide your MAC address)

3. receive_attack.py is the Trojan that is meant to be executed on the victim machine (Need to be packaged into a trustworthy executable)
4. keylogger.py creates a log file in the existing directory and appends pressed keys (Could be included in the main script as well or be delivered after gaining remote access)
5. sock.py is run on the hacker machine and is constantly waiting for victim to connect so the hacker can send remote commands

# Functionality

attacker.py has a few custom functionalities besides the commands that already exist in Windows Command Prompt. With that being said, you can basically run any command you want.
   - cd = change directory
   - download <filename> = download a file from the victim
   - upload <filename> = upload a file to the victim (for example, the keylogger)
   - screenshot = victim takes a screenshot and stores the image in the same directory
   - persistance = Change Windows Registry to gain persistance through Powershell

# Attacker's POV
    
![RAT](https://user-images.githubusercontent.com/81070073/139211842-1094cbe0-649f-4ceb-a081-d20c510cc77f.gif)

    
This gif demonstrates the basics of what the attacker can do after the victim executes the malware and connects to the attacker's server. 

# Packaging

I have also packaged the malware with a legitimate Spotify Installer and a fake Spotify logo icon to show a plausible attack example.
There are four files inside.
- Spotify.exe is the finalized trojan
- Spotify_Setup.exe is the compiled sock.py script using Pyinstaller
- spotify-256.ico is the icon used to decorate the Python executable
- SpotifySetup.exe is the legitimate installer downloaded from Spotify

This project could be improved further if I obfuscated the code to help it bypass antivirus software.
The attack demonstrated in the gif was under the condition that the host's antivirus had been disabled OR
that the infected folder was excluded from the antivirus' protection.

