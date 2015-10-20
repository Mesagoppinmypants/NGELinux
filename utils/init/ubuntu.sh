#/bin/sh

echo "Initializing Environment"

sudo apt-get remove --purge oracle-java*
sudo apt-get update
sudo apt-get install build-essential zlib1g-dev libpcre3-dev cmake libboost-dev libxml2-dev libncurses5-dev flex bison git-core alien libaio1 python-ply bc curl  libcurl4-openssl-dev

if [ ! -f oracle-instantclient12.1-basiclite-12.1.0.2.0-1.i386.rpm ]; then
	wget http://repo.cyrus-project.org/centos5-i386/RPMS.nonfree/oracle-instantclient12.1-basiclite-12.1.0.2.0-1.i386.rpm
fi

if [ ! -f oracle-instantclient12.1-devel-12.1.0.2.0-1.i386.rpm ]; then
	wget http://repo.cyrus-project.org/centos5-i386/RPMS.nonfree/oracle-instantclient12.1-devel-12.1.0.2.0-1.i386.rpm
fi

if [ ! -f oracle-instantclient12.1-sqlplus-12.1.0.2.0-1.i386.rpm ]; then
	wget http://repo.cyrus-project.org/centos5-i386/RPMS.nonfree/oracle-instantclient12.1-sqlplus-12.1.0.2.0-1.i386.rpm
fi

if [ ! -f IBMJava2-SDK-1.4.2-13.18.tgz ]; then
	wget https://bitbucket.org/swgmasters/swg-src/downloads/IBMJava2-SDK-1.4.2-13.18.tgz
fi

# install java
tar -xvzf IBMJava2-SDK-1.4.2-13.18.tgz
sudo mv IBMJava2-142/ /opt
sudo ln -s /opt/IBMJava2-142 /usr/java

# install oracle instantclient

# nuke old versions
sudo apt-get remove --purge oracle-instant*
sudo rm -rf /usr/lib/oracle &> /dev/null

sudo alien -i oracle-instantclient12.1-basiclite-12.1.0.2.0-1.i386.rpm
sudo alien -i oracle-instantclient12.1-devel-12.1.0.2.0-1.i386.rpm
sudo alien -i oracle-instantclient12.1-sqlplus-12.1.0.2.0-1.i386.rpm

# set env vars
sudo find /usr/lib -lname '/usr/lib/oracle/*' -delete &> /dev/null

sudo rm -f /etc/ld.so.conf.d/java.conf /etc/profile.d/java.sh /etc/profile.d/oracle.sh /etc/ld.so.conf.d/oracle.conf &> /dev/null
sudo touch /etc/ld.so.conf.d/java.conf
sudo touch /etc/profile.d/java.sh
sudo touch /etc/profile.d/oracle.sh
sudo touch /etc/ld.so.conf.d/oracle.conf

export ORACLE_HOME=/usr/lib/oracle/12.1/client
export JAVA_HOME=/usr/java

echo "/usr/java/jre/bin" | sudo tee -a /etc/ld.so.conf.d/java.conf 
echo "/usr/java/jre/bin/classic" | sudo tee -a /etc/ld.so.conf.d/java.conf

echo "export JAVA_HOME=/usr/java" | sudo tee -a /etc/profile.d/java.sh
echo "export PATH=\$PATH:\$JAVA_HOME/bin:\$JAVA_HOME/jre/bin" | sudo tee -a /etc/profile.d/java.sh

echo "/usr/lib/oracle/12.1/client/lib" | sudo tee -a /etc/ld.so.conf.d/oracle.conf

echo "export ORACLE_HOME=/usr/lib/oracle/12.1/client" | sudo tee -a /etc/profile.d/oracle.sh
echo "export PATH=$PATH:$ORACLE_HOME/bin" | sudo tee -a /etc/profile.d/oracle.sh
echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/oracle/12.1/client/lib:/usr/include/oracle/12.1/client" | sudo tee -a /etc/profile.d/oracle.sh

source /etc/profile.d/oracle.sh
source /etc/profile.d/java.sh

sudo ln -s /usr/include/oracle/12.1/client $ORACLE_HOME/include

sudo ldconfig

echo "Environment Initialization Complete! You should reboot!"
