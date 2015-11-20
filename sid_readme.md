# Debian SID SWGMasters Developer VM
## System Requirements

* Virtualbox 5.0.x 
* 4GB RAM minimum (The VM supports 64GB RAM)
* 30GB Harddisk Space

Recommended: 
* SSH-Client (Putty in Windows) 
* SCP-Client (WinSCP)
* more RAM if you want to run more then 1-2 Zones
* SSD as VM Storage

## Whats included in the VM 

* Debian SID/Testing 32Bit
* OracleDB 11g Release 2
* Oracle Enterprise Manager https://<vmip>:1158/em/console (User: SYSTEM Pass: swg)
* Clientfiles needed to start the server /home/swg/clientdata/
* Appearance Files needed to start the server /home/swg/appearance/
* Copy of https://bitbucket.org/swgmasters/swg-src/ /home/swg/swg-src/
* All dependencies installed to compile your own server
* Samba preinstalled pointed to /home/swg/ (You can use editors/IDEs or/and your git in Windows)

Default Password: swg

## What do you need todo to get a server running

Import the Appliance to Virtualbox.
* CPU Setting PAE
* Network Setting: Bridge Network

Change the /etc/hosts file to the right ipaddress. 

		nano /etc/hosts

Change the 192.168.2.x to the IP of the Virtual Machine

		<yourip>		swg

Restart the server: 

		shutdown -r now

Download Putty and point it to the IP of your VM
Login as user swg with password swg. 

		cd swg-src/
		git pull (optional updating repo content)
		./build_linux.sh
		!! Ignore the install dependencies PART !!
		
## Buildingphases
Follow the instructions on your screen. The binary building phase will take roughly 1h/1Core.
The Script Building Phase will throw errors if you skip the configphase, do configs first, then scriptbuilding.

### Configphase
use local

Database DSN: 
//127.0.0.1/swg

Database User:
swg

Database Password: 
swg

### Scriptbuilding
Scriptbuilding will take about 6hours the first time. You can later just recompile single scripts or tab files, look at the
utils/build_ and the build_linux.sh files to see the syntax of the mocha, javac and compilertools. 

### Database 
The Clustername has to be the same you used in the configphase. The same for the nodeip. The other settings are self-explaining. 

## Clientdata and Appearance Files
		cd /home/swg/
		rsync -av /home/swg/clientdata/sku.0/ /home/swg/swg-src/data/sku.0/
		rsync -av /home/swg/clientdata/sku.1/ /home/swg/swg-src/data/sku.1/
		rsync -av /home/swg/clientdata/sku.2/ /home/swg/swg-src/data/sku.2/
		rsync -av /home/swg/clientdata/sku.3/ /home/swg/swg-src/data/sku.3/

		cp -R /home/swg/appearance /home/swg/swg-src/

## First start
		./start_Server.sh

Point your login.cfg to the IP of the Virtualmachine.
