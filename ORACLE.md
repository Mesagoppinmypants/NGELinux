# Oracle Database Server Build

Note: for Windows, you can also use the instant server, but this is the "right" way to do it.

* Download The Latest Version of Oracle Linux (can be 64 bit)
* Install it as you would any other distro
* For your non-root user, use the name oracle
* For ease of use, choose the install option with a desktop environment

* Can also install Oracle Server on Windows host if you know what you're doing

## Initial Setup

From a root terminal:
    
    yum install oracle-rdbms-server-12cR1-preinstall
    systemctl stop firewalld
    systemctl disable firewalld
    
## Hostname

* Edit /etc/hostname and change it to something other than localhost
* Add an alias pointing 127.0.0.1 to the new hostname
    
## Download the latest Oracle Database zip files (should be 2)

* Unzip both, and run the installer as your normal oracle user
* Go through the process, setting the options where required, including the db name
* Make sure to name the database appropriately
* Make sure to specify the proper hostname of the machine you are running

## Edit /etc/oratab

As root, change the "N" at the end of the last string to "Y"

## Add some environment variables

Add to the bottom of /home/oracle/.bashrc:

    export ORACLE_HOME=/home/oracle/app/oracle/product/12.1.0/dbhome_1
    export PATH=$PATH:/home/oracle/app/oracle/product/12.1.0/dbhome_1/bin/
    export ORACLE_SID=swg; #set this to the name you chose for your database/service

Reboot

## Create /etc/init.d/dbora

Copy and pase the example below, but make sure to set the hostname and Oracle variables!

    #! /bin/sh 
    #
    # Change the value of ORACLE_HOME to specify the correct Oracle home
    # directory for your installation.
    
    ORACLE_HOME=/home/oracle/app/oracle/product/12.1.0/dbhome_1
    #
    # Change the value of ORACLE to the login name of the
    # oracle owner at your site.
    #
    ORACLE=oracle
    
    PATH=${PATH}:$ORACLE_HOME/bin
    HOST="oracle"
    PLATFORM=`uname`
    export ORACLE_HOME PATH
    #
    if [ ! "$2" = "ORA_DB" ] ; then
          runuser $ORACLE  $0 $1 ORA_DB
          if [ "$PLATFORM" = "Linux" ] ; then
             touch /var/lock/subsys/dbora
          fi
          exit
       fi
    #
    case $1 in
    'start')
            $ORACLE_HOME/bin/dbstart $ORACLE_HOME &
            ;;
    'stop')
            $ORACLE_HOME/bin/dbshut $ORACLE_HOME &
            ;;
    *)
            echo "usage: $0 {start|stop}"
            exit
            ;;
    esac
    #
    exit

Then, make it executable:
    
    chmod +x /etc/init.d/dbora

## Oracle Listener configuration

In /home/oracle/app/oracle/product/(some version number)/dbhome_1/network/admin edit 
both tnsnames.ora and listener.ora and change all mentions of "localhost" 
to the hostname you chose after installation.

## Reboot and Start the Database
After rebooting, become root and execute:

    /etc/init.d/dboracle start

## Test the database locally on the DB server and connect for management
    
    sqlplus
    
Login as SYSTEM using the password you set during installation.

### Create user and grant privs

	ALTER SESSION SET "_ORACLE_SCRIPT"=true;
    CREATE USER remoteuser IDENTIFIED BY yourpasswordhere;
    GRANT ALL PRIVILEGES TO remoteuser;
    GRANT UNLIMITED TABLESPACE TO remoteuser;

## Test connection from game server

    sqlplus remoteuser/yourpasswordhere@oracle:1521/swg

### Deleting/clearing tables for a fresh DB population

    drop user username cascade;

Then recreate the user per the previous instructions.
