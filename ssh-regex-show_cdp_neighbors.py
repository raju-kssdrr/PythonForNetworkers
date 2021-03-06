#####Original script taken from https://pynet.twb-tech.com/
######Written by:
######Kirk Byers
######CCIE #6243
######Twitter: @kirkbyers
######https://pynet.twb-tech.com/
######
######Garry Baker @networkbaker
######Made addtions as needed want to thank Kirk Byers for base script
######additions started 24JUNE2014

import paramiko
import time
import re

def disable_paging(remote_conn):
    '''Disable paging on a Cisco router'''

    remote_conn.send("terminal length 0\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output


if __name__ == '__main__':


    # VARIABLES THAT NEED CHANGED
    #ip = '192.168.100.6'
    #username = 'user'
    #password = 'pass'
    ##addedd 14JUNE2014 interactive input for ip,user,password
    ##--Changed input to raw_input so no more ''
    ip = raw_input("Enter IP address: ")
    username = raw_input("Enter username: ")
    password = raw_input("Enter password: ")

    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # initiate SSH connection
    remote_conn_pre.connect(ip, username=username, password=password)
    print "SSH connection established to %s" % ip

    # Use invoke_shell to establish an 'interactive session'
    remote_conn = remote_conn_pre.invoke_shell()
    print "Interactive SSH session established"

    # Strip the initial router prompt
    #output = remote_conn.recv(1000)

    # See what we have
    #print output

    # Turn off paging
    disable_paging(remote_conn)

    # Now let's try to send the router a command
    remote_conn.send("\n")
    remote_conn.send("show cdp neighbors detail\n")

    # Wait for the command to complete
    time.sleep(2)

    #get 5000 lines of output, then send it thru regex and findall IP address: and then print
    #added by Garry Baker on 29JUNE2014
    output = remote_conn.recv(5000)
    output_print = re.findall("IP address: ([0-9]*\.[0-9]*\.[0-9]*\.[0-9]*)", output)
    print output_print

    #Exit script, need this for windows powershell and cmd to exit or it hangs the prompt
    #sys.exit()
    # Now let's exit
    #added by Garry Baker on 29JUNE2014
    remote_conn.send("\n")
    remote_conn.send("exit\n")