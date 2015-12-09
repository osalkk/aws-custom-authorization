#!/usr/bin/python

import paramiko
import sys
import time


def disable_paging(remote_conn):
    '''Disable paging on a Cisco router'''

    remote_conn.send("terminal length 0\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output


if __name__ == '__main__':


    # VARIABLES THAT NEED CHANGED
    ip = '192.168.0.1'
    username = 'yemeksepeti'
    password = '3193743'

    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # initiate SSH connection
    remote_conn_pre.connect(ip, username=username, password=password,allow_agent=False)
    print "SSH connection established to %s" % ip

    # Use invoke_shell to establish an 'interactive session'
    remote_conn = remote_conn_pre.invoke_shell()
    print "Interactive SSH session established"

    # Strip the initial router prompt
    output = remote_conn.recv(1000)

    # See what we have
    print output

    # Turn off paging
    disable_paging(remote_conn)

    # Now let's try to send the router a command
    remote_conn.send("\n")
    remote_conn.send('unset vpn "SOL_VPN_S2S_IKE_SOLMETRO" bind interface\n')

    # Wait for the command to complete
    time.sleep(2)


    # Turn off paging
    disable_paging(remote_conn)

    # Now let's try to send the router a command
    remote_conn.send("\n")
    remote_conn.send("unset route 0.0.0.0/0 interface ethernet0/7 gateway 213.128.91.73\n")

    # Wait for the command to complete
    time.sleep(2)

    # Turn off paging
    disable_paging(remote_conn)

    # Now let's try to send the router a command
    remote_conn.send("\n")
    remote_conn.send("set route 0.0.0.0/0 interface ethernet0/7 gateway 213.128.91.73 preference 20 metric 1\n")

    # Wait for the command to complete
    time.sleep(2)


    
    output = remote_conn.recv(5000)
    print output





