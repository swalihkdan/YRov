from start_adapter import start_adapter
import subprocess 
import logging
import os

#Configuring the logger
logging.basicConfig(filename="./logs/start_scan.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 

#Creating an object 
logger=logging.getLogger() 

#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG) 

start_adapter()

logger.info("Starting Airodump-ng.........................")
os.system("timeout 3s airodump-ng wlan0mon >> wifi.txt")
#P = subprocess.Popen(["timeout","5s","airodump-ng","wlan0mon"],stdout = subprocess.PIPE, stderr = subprocess.PIPE)
logger.info("Executed Airodump Command....................")
#stdout,stderr = P.communicate()  #returns stdout and stderr
#print(stdout)
#logger.info("Printed output of airodump-ng")

#logger.info("Starting Airodump-ng using check_output mode")
#airodump = subprocess.check_output(["timeout","1s","airodump-ng","wlan0mon"], stdin=None,stderr=None)
#print(airodump)

