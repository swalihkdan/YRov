'''
Installation Candidate for MROV
'''

#!/usr/bin/env python3

import sys
import datetime
import os
import psutil
import logging


#____________________________________________GENERAL___SETTINGS__________________________________________________________________________________#
log_file = 'install.log'
#____________________________________________LOGGING___SETTINGS__________________________________________________________________________________#

# Configuring the logger
logging.basicConfig(filename=log_file,
                    format='%(asctime)s  %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

#_________________________________________________________________________________________________________________________________________________#

