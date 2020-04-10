import subprocess 
import logging

def start_adapter():
	#Configuring the logger
	logging.basicConfig(filename="./logs/start_adapter.log", 
	                    format='%(asctime)s %(message)s', 
	                    filemode='w') 

	#Creating an object 
	logger=logging.getLogger() 

	#Setting the threshold of logger to DEBUG 
	logger.setLevel(logging.DEBUG) 

	logger.info("Started airmon-ng..................................")
	airmon = subprocess.Popen(["airmon-ng","start","wlan0"],stdout = subprocess.PIPE , stderr = subprocess.PIPE)
	stdout,stderr = airmon.communicate()
        print("Note : Wifi Card is currently in MonitorMode")


