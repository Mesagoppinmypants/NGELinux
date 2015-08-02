#!/bin/bash

basedir=$PWD
PATH=$PATH:$basedir/build/bin

DBSERVICE=
DBUSERNAME=
DBPASSWORD=
HOSTIP=
CLUSTERNAME=
NODEID=
DSRC_DIR=
DATA_DIR=

if [ ! -d $basedir/build ]
then
	mkdir $basedir/build
fi

if [ ! -f $basedir/.setup ]; then
	if [[ $(lsb_release -a) =~ .*Ubuntu.* ]] || [ -f "/etc/debian_version" ]
	then
		read -p "!!!ONLY RUN ONCE!!! Do you want to install dependencies (y/n)?" response
		response=${response,,} # tolower
		if [[ $response =~ ^(yes|y| ) ]]; then
			$basedir/utils/init/ubuntu.sh
			source /etc/profile.d/java.sh
			source /etc/profile.d/oracle.sh
			touch $basedir/.setup
			
			echo "Please login and out or reboot as changes have been made to your PATH "
		fi
	fi
fi

read -p "Do you want to build the server now? (y/n) " response
response=${response,,} # tolower
if [[ $response =~ ^(yes|y| ) ]]; then
	cd $basedir/build
	
	cmake $basedir/src -DCMAKE_BUILD_TYPE=Release

	make -j$(nproc)

	cd $basedir
fi

read -p "Do you want to build the config environment now? (y/n) " response
response=${response,,} # tolower
if [[ $response =~ ^(yes|y| ) ]]; then

	# Prompt for configuration environment.
	read -p "Configure environment (local, live, tc, design)? You probably want local. " config_env

	# Make sure the configuration environment exists.
	if [ ! -d $basedir/configs/$config_env ]; then
		echo "Invalid configuration environment."
		exit
	fi

        
	echo "Enter your IP address (LAN for port forwarding or internal, outside IP for DMZ)"
	read HOSTIP

	echo "Enter the DSN for the database connection "
	read DBSERVICE

	echo "Enter the database username "
	read DBUSERNAME

	echo "Enter the database password "
	read DBPASSWORD

	echo "Enter a name for the galaxy cluster "
	read CLUSTERNAME

	if [ -d $basedir/exe ]; then
		rm -rf $basedir/exe
	fi

	mkdir -p $basedir/exe/linux/logs
	mkdir -p $basedir/exe/shared

	ln -s $basedir/build/bin $basedir/exe/linux/bin

	cp -u $basedir/configs/$config_env/linux/* $basedir/exe/linux
	cp -u $basedir/configs/$config_env/shared/* $basedir/exe/shared

	for filename in $(find $basedir/exe -name '*.cfg'); do
		sed -i -e "s@DBSERVICE@$DBSERVICE@g" -e "s@DBUSERNAME@$DBUSERNAME@g" -e "s@DBPASSWORD@$DBPASSWORD@g" -e "s@CLUSTERNAME@$CLUSTERNAME@g" -e "s@HOSTIP@$HOSTIP@g" $filename
	done

	#
	# Generate other config files if their template exists.
	#

		# Generate at least 1 node that is the /etc/hosts IP.
		$basedir/utils/build_node_list.sh
fi

read -p "Do you want to build the scripts? (y/n) " response
response=${response,,} # tolower
if [[ $response =~ ^(yes|y| ) ]]; then
	#prepare environment to run data file builders
	oldPATH=$PATH
	PATH=$basedir/build/bin:$PATH

	
	$basedir/utils/mocha/prepare_all_scripts.sh $basedir/dsrc/sku.0/sys.server/compiled/game/script
	$basedir/utils/build_java.sh
	$basedir/utils/build_miff.sh
	$basedir/utils/build_tab.sh
	$basedir/utils/build_tpf.sh

	$basedir/utils/build_object_template_crc_string_tables.py
	$basedir/utils/build_quest_crc_string_tables.py

	PATH=$oldPATH
fi

read -p "Import database? (y/n) " response
response=${response,,}
if [[ $response =~ ^(yes|y| ) ]]; then
	cd $basedir/src/game/server/database/build/linux

	if [[ -z "$DBSERVICE" ]]; then
		echo "Enter the DSN for the database connection "
		read DBSERVICE
	fi

	if [[ -z "$DBUSERNAME" ]]; then
		echo "Enter the database username "
		read DBUSERNAME
	fi

	if [[ -z "$DBPASSWORD" ]]; then
		echo "Enter the database password "
		read DBPASSWORD
	fi

	./database_update.pl --username=$DBUSERNAME --password=$DBPASSWORD --service=$DBSERVICE --goldusername=$DBUSERNAME --loginusername=$DBUSERNAME --createnewcluster --packages

	echo "Loading template list"
	perl ../../templates/processTemplateList.pl < ../../../../../../dsrc/sku.0/sys.server/built/game/misc/object_template_crc_string_table.tab > $basedir/build/templates.sql
	sqlplus ${DBUSERNAME}/${DBPASSWORD}@${DBSERVICE} @$basedir/build/templates.sql > $basedir/build/templates.out
fi

echo "Build complete!"
