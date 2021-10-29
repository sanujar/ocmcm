# Code based on Oracle's automatically generated code sample.
# Please follow the instructions in README.md to set this up.

# To make this code sample work in your Oracle Cloud tenancy,
# please replace the values for any parameters whose current values do not fit
# your use case (such as resource IDs, strings containing ‘EXAMPLE’ or ‘unique_id’, and
# boolean, number, and enum parameters with values not fitting your use case).

import oci
import time
import sys
import select
import paramiko

# Create a default config using DEFAULT profile in default location
# Refer to
# https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm#SDK_and_CLI_Configuration_File
# for more info
config = oci.config.from_file()

# Initialize service client with default config file
core_client = oci.core.ComputeClient(config)

# SSH code from http://sebastiandahlgren.se/2012/10/11/using-paramiko-to-send-ssh-commands/ and
# https://gist.github.com/batok/2352501


k = paramiko.RSAKey.from_private_key_file("path/to/key")  # TODO
i = 1

#
# Try to connect to the host.
# Retry a few times if it fails.
#
while True:
	print("Trying to connect to the server to gracefully save and stop MC.")

	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname="...", username="...", pkey=k)  # TODO
		print("Connected to the server.")
		break
	except paramiko.AuthenticationException:
		print("Authentication failed when connecting to server.")
		sys.exit(1)
	except:
		print(
			"Could not connect to server. A new connection will be attempted.")
		i += 1
		time.sleep(5)

	# If we could not connect within time limit
	if i == 30:
		print("Could not connect to the server. Giving up. Please contact me.")
		sys.exit(1)

# Send the command (non-blocking)
stdin, stdout, stderr = ssh.exec_command("""
	screen -S "MC" -X stuff "stop\r" 
	""")  # without the new line in the code there's a syntax error. The carriage return is needed to execute the command
# the -X stuff is required

# Wait for the command to terminate
while not stdout.channel.exit_status_ready():
	# Only print data if there is data to read in the channel
	if stdout.channel.recv_ready():
		rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
		if len(rl) > 0:
			# Print data from stdout
			print(stdout.channel.recv(1024))

#
# Disconnect from the host
#
print("The server has been informed to stop the MC server.")
ssh.close()

time.sleep(7)  # should be enough time to gracefully save and stop MC.

# Send the request to service, some parameters are not required, see API
# doc for more info
instance_action_response = core_client.instance_action(
	instance_id="ocid1.instance.oc1...",  # TODO
	action="SOFTSTOP", )
print("An API call has been sent to stop this server.")

time.sleep(10)  # should avoid API returning a blank response for the next query.

# Get the data from response
# print(instance_action_response.data)

# Send the request to service, some parameters are not required, see API
# doc for more info
list_instances_response = core_client.list_instances(
	compartment_id="ocid1.tenancy.oc1....",  # TODO
	display_name="...",  # TODO
	lifecycle_state="STOPPED")

# Get the data from response
# print(list_instances_response.data)

while list_instances_response.data == []:
	print("The server hasn't stopped yet.")
	time.sleep(20)
	list_instances_response = core_client.list_instances(
		compartment_id="ocid1.tenancy.oc1....",  # TODO
		display_name="...",  # TODO
		lifecycle_state="STOPPED")

print(
	"The server should have stopped.")
print("Please press enter to close this window.")
input()
