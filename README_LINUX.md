# Game Server Setup (Debian and Ubuntu derivatives)

## System Requirements

### sudo and passwordless elevation

Before you do anything, make sure to install sudo if it isn't already, and add your normal user to the sudoers file! For ease of use, you can disable the password requirement as specified below.

    su #and enter your root password at the prompt
    apt-get install sudo

    visudo

Add the following line anywhere in the file, replacing "user" with your username:

    user ALL=(ALL) NOPASSWD: ALL

To save, hit the ESC key, then type wq! and hit enter. You may then exit from your root shell. 

## Specifications

To run this game in any capacity, you MUST have an Oracle database server setup and configured for remote access.

To run 1 zone, you need:

* At least 4GB RAM
* Preferably 2 or more CPU cores

To run all zones and buildouts, you need:

* 8 or more CPU cores
* 16GB minimum with 24-32GB of RAM preferred

## Java Notes

Since we ONLY want to compile and run with javac and javaw specified by IBM in the RPMs, remove other javac's from path.
	
	sudo update-alternatives --remove-all javac
	
Then, double check path directories...
	
	whereis javac
	whereis javaw

They should both ONLY say the IBM path.

## Environment Setup

Add the following to your ~/.bashrc, replacing "swg" with your database name

    export ORACLE_SID=swg;

## Compilation

Using a 32 bit installation of Ubuntu or Debian Linux, clone this repo and execute the build_linux.sh script from a terminal. While building, if you haven't already, go ahead and setup the database server, as build time is quite long.

If you get errors about a CFLAG, remove the offending cflag from src/CMakeLists.txt and try again. gcc-5.2 is HIGHLY suggested, it builds a much more efficient server and supports all cflags. This is why using Debian Sid is a good option, else you can build gcc yourself or find a PPA to supply it.

## Configuration

Add preload files:

    cd exe/linux
    find ../../data/sku.0/sys.server/compiled/game/object/ -name \"*.iff\" > objectTemplates.plf
    find ../../data/sku.0/sys.server/compiled/game/datatables/ -name \"*.iff\" > datatables.plf

### Oracle Access

For the Oracle DSN, the format is //[ip or hostname][optional port]/[resource name]. For a DB on a server named "server" with resource "swg" it would thus be:

    //server/swg
    
Enter the user and password.

### Networking

Always select "local," as it works best. For IP address, use the SWG server's internal LAN address. Make sure that whatever the server's hostname is, that you have it set in the hosts file.

hosts example for "swg":

    10.0.0.32    	swg
    127.0.0.1		localhost
    
    
If you wish to externally host a server, either use 1:1 NAT (DMZ) and set your external IP as your hostname in your hosts file, or forward the SWG ports (todo, list here). Then, set your login server in default.cfg to 0.0.0.0 and the IP address in the CLUSTERS database table to your external (WAN/ISP) provided IP address.

### Configuration Options

If your machine has the CPU power and RAM required per the requirements to do so, you can uncomment startPlanet lines in the localOptions.cfg file. You may also enable Tansarii Station, and buildouts, amongst other options. In the taskmanager.rc file, you may also uncomment and enable the commodities server, to make the bazaar work.

## Server Execution

Simply

    ./startServer.sh

# Oracle Database Setup

See ORACLE.md

# Other notes, questions

See NOTES.md
