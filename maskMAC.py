import subprocess,random

if __name__=="__main__":
    interface = "eth0"
    macs = []
    for x in range(6):
        a = random.randint(0,255)
        hex = '%02x' % a
        macs.append(hex)
    new_mac = (':'.join(macs))

    print("Shutting down the interface")
    subprocess.run(["ifconfig", "eth0", "down"])
    print("Changing the interface hw address of ", interface, "to ", new_mac)
    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])
    print("MAC address changed to ", new_mac)
    subprocess.run(["ifconfig", interface, "up"])
    print("Network interface has turned on")
