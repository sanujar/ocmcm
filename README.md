# Oracle Cloud Minecraft Server Management Scripts (OCMCM)

## Introduction

These scripts were made, by request from non-technical players of a Minecraft server, to give them an easy way to control their server on Oracle Cloud, without having to use the web control panel and SSH manually.

The two main scripts do the following:

1. Start.py - Use the Oracle API to start a VM/instance, confirm that it has started up, then SSH into the server to start up a Minecraft server within screen.
2. Stop.py - Connect to the server via SSH to safely shut down the server, allow all the worlds to save, and then wait 7 seconds before using the Oracle API to safely shut down the server.

***
## Setup Instructions

### Python
This version of the script has been written for and tested on only Python 3.10.0. It might work on other version of Python 3, but you might run into issues with OCI and Paramiko. 

For Windows, an installer can be downloaded from [here](https://www.python.org/downloads/release/python-3100/). During install, select the options to associate .py files with Python to be able to double-click on the scripts to launch, and add it to your PATH to be able to run commands with ```pip```.

Download the repository as a ZIP, and extract it to your desired location. Then, opening a terminal in that present location (which can be done by typing ```cmd``` in your address bar in explorer), run ```pip install -r requirements.txt``` to install OCI and Paramiko.

### API Key and Config
Note: The default directory for OCI files (specifically your config file (and optionally your private key)) is ```~/.oci``` (```%HOMEPATH%\.oci\``` on Windows).

Follow the instructions at [Required Keys and OCIDs](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm) to generate your API key and config files.

Ideally, create a new user for your tenancy for API access, and give them administrator access. Then, generate and download a private key for API access for this user, saving it into the default folder mentioned above. After confirming that you have downloaded the key, Oracle will automatically generate a config file.

Save this in the default folder with the filename ```config``` (no extension), using a text editor, after adding the filename of your private key to the last line, at ```key_file=```.

### Scripts and Server-Side

The scripts will have to be modified before first use, to include variables relevant to your tenancy and your VM. There are seven variables that need to be modified in each of the scripts, and each of line containing one is marked with ```#TODO```, which IDEs like [Pycharm](https://www.jetbrains.com/pycharm/) will pick up on.
This includes linking to the path of the private key for SSH access to the server. If on Windows, it is easier to leave the private key in the same directory as the scripts, to avoid issues with file paths.

You can also perform additional modification, such as changing the commands sent to the server, or the directory in which the command is executed.

For help with finding your tenancy and VM OCIDs, please refer to [Required Keys and OCIDs](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm) and the other linked API documentation.

The specific commands used to start and stop the script assume the Minecraft server files are in ```/home/ubuntu/Minecraft```, and that Fabric server is being used. If this is not the case, the ```.jar``` file referenced in Start.py, as well as the ```cd``` command, will need to be altered/removed. The command assumes there is 8 GB allocated to the server; if not, modify the ```-Xmx``` value to maximise your RAM, while still giving some headroom for the OS, to avoid instability.

This script is not limited to Minecraft: all that needs to be modified are the commands executed over SSH in order to run a completely different program/server.

Also, the commands assume ```screen``` is being used to create a virtual console, to allow the server to continue running without the need for an active terminal session. This can be installed using ```sudo apt-get install screen``` on the server.

## Usage

Assuming you have followed the steps above correctly, double-clicking or otherwise executing the respective script for the action you wish to perform should work. While the scripts are running, they will print what is currently happening, and will not exit automatically after finishing (waiting for an ```Enter``` from the user).

***

# Expected Output

### Start.py

```
An API call has been sent to start this server.
The server hasn't started yet. Please wait.
The server hasn't started yet. Please wait.
The server should have started up. Attempting connection...
Trying to connect to the server to start up MC.
Connected to the server.
The server has been informed to start the MC server. Please wait ~10 seconds for it to be connectable.
Please press enter to close this window.
```

### Stop.py

```
Trying to connect to the server to gracefully save and stop MC.
Connected to the server.
The server has been informed to stop the MC server.
An API call has been sent to stop this server.
The server hasn't stopped yet.
The server hasn't stopped yet.
The server should have stopped.
Please press enter to close this window.
```

In case you get another message or error, it should be relatively descriptive. If it isn't, the position of the code that prints that output within the script itself may provide useful context.

***

# Error Reporting


In case there are any issues with the script, please create an issue in this GitHub repository. I unfortunately will not have time to respond to technical support requests; searching the internet is likely to get you a better response, faster, than I can provide. 

**Note: This is my first time using Python. Code quality may be questionable. Use with care.**
