#!/usr/bin/env python3

'''
Installation Candidate for MROV
'''


import sys
import datetime
import os
import logging
import subprocess


#____________________________________________GENERAL___SETTINGS__________________________________________________________________________________#
log_file = 'install.log'
#____________________________________________LOGGING___SETTINGS__________________________________________________________________________________#

# Configuring the logger
logging.basicConfig(filename=log_file,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

# adding a handler to output logs to stdout
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

#_________________________________________________________________________________________________________________________________________________#


def run_command(command_as_list):

    command = ' '.join(command_as_list)
    logger.info("running \' {} \' command".format(command))

    try:
        result = subprocess.run(
            command_as_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output = result.stdout.decode()
        error = result.stderr.decode()
        return_code = result.returncode

        if return_code == 0:
            logger.info('command \'{}\' executed succesfully'.format(command))
            print(output)
        else:
            logger.error(
                'command \'{}\' exited with error {}'.format(command, error))
            sys.exit(1)
            logger.info("Exiting program")

    except Exception as e:
        logger.error(
            'command \'{}\' exited with error {}'.format(command, e))

        sys.exit(1)
        logger.info("Exiting program")


#___________________________________________________Install_Puppet_Confuguration_Manager_________________________________________________________________________________________#

def install_puppet():

    logger.info("Inside function install_puppet")

    run_command(
        ['wget', 'https://apt.puppetlabs.com/puppet5-release-wheezy.deb'])
    logger.info("downloaded puppetlabs repo file")

    run_command(['sudo', 'dpkg', '-i', 'puppet5-release-wheezy.deb'])
    logger.info("successfully added puppet repo")

    run_command(['sudo', 'rm', '-rf', 'puppet5-release-wheezy.deb'])
    logger.info("removing puppet files")

    run_command(['sudo', 'apt', 'update', '-y'])
    logger.info("updating repos")

    # run_command(['sudo', 'apt', 'install', '-y', 'puppet-agent'])
    run_command(['sudo', 'apt', 'install', '-y', 'puppet'])
    logger.info("installing puppet agent")

    # run_command(['PATH=$PATH:/opt/puppetlabs/bin/'])
    # logger.info("temporarily added puppet to path")

#__________________________________________________________Download_and_execute mrov.pp___________________________________________________________________________________#


def execute_mrov_puppet():
    run_command(['wget', 'https://tinyurl.com/yrov-puppet', '-O', 'yrov.pp'])
    logger.info('Downloaded yrov.pp')

    # run_command(['sudo', '/opt/puppetlabs/bin/puppet', 'apply', 'yrov.pp'])
    run_command(['sudo', 'puppet', 'apply', 'yrov.pp'])
    logger.info('executed yrov.pp')
#___________________________________________________________Clone project files______________________________________________________________________________________#


def clone_project_files():
    run_command(['git', 'clone', 'https://github.com/rezraf77/YRov.git'])
    logger.info('Cloned project repository')
#_________________________________________________________________________________________________________________________________________________#


if __name__ == "__main__":
    install_puppet()
    execute_mrov_puppet()
    clone_project_files()

#_________________________________________________________________________________________________________________________________________________#
