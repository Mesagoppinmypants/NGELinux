# whitengold/SWG#

### Dependencies ###
##### Windows #####
1. Cygwin installed to c:\cygwin (DO NOT add c:\cygwin or c:\cygwin\bin to your Environment Settings/path)
2. Add C:\whitengold\tools to your Environment Settings/path
3. Make sure you are using Java 6 Update 1 and that all paths are lowercase
4. During the install change the JDK install location to c:\jdk During the install you will be prompted where to install the JRE (which installs from the JDK installer and does not need another downloaded installer) Change this JRE location to c:\jdk\jre6
5. Install Python 2.7.6 64 bit to c:\Python27 <--- again install location case sensitive
6. Install Perl 5.18.4 64 bit to c:\Perl64 (This is the ActiveState Perl NOT Strawberry or the others) <--- again install location case sensitive
7. Install OracleDB 12c 64 bit
8. Install CMake 3.2.2 if you have not done so already.
9. Additional "Environment Settings --- Path" settings after all the above are installed...
Make sure there is a semi-colon at the end of your PATH line and then add the following:
C:\Python27;c:\jdk\jre\bin;c:\jdk\jre\bin\client;C:\Perl64\site\bin;C:\Perl64\bin;C:\whitengold\tools


### Building ###

1. Open CMake 3.2.2
2. Point it to the C:\whitengold\src folder
3. Tell it to use C:\whitengold\build as the output location
4. Click Generate
5. Select Visual Studio 11 2012 (from the drop down list in CMake)
6. Click finish
7. If all went well and your dependencies are found properly, there will be no Red window inside CMake

Change the following names in exe/win32/*.cfg


* CHANGE_IP				<--- Replace with your LAN IP here
* CHANGE_CLUSTER_NAME		<--- Replace with your Cluster name here, except on DSN which should be your oracle endpoint name
* CHANGE_HOST				<--- Replace with your LAN "host name" (this must be in c:\windows\system32\drivers\etc\hosts)
* CHANGE_PASSWORD			<--- Replace with your database password in exe/win32/*.cfg

Go to the c:\whitengold\build folder and open swgnge.sln with Visual Studio 2013. Change to Release in the Build Configuration type and compile.

###### Configuration ######

If you are using Windows Firewall, add a firewall rule on Public & Private Network for Port 1521 so that you'll be able to communicate with the OracleDB listener.


Once you've got OracleDB up and running (I'm hoping you have this already, since its such a pain in the buttocks to setup) Go to the c:\whitengold folder and give the OracleDB 3 or 4 minutes of being up and running (should be 5 services)


* Start the c:\whitengold\Login.bat file
* Wait 10 seconds minimum
* Start the c:\whitengold\TaskManager.bat file

***Note: Keep the TaskManager open and on the Process tab.***


If after a few minutes, the PlanetServer.exe processes (all of them) crash (this happens sometimes, first time starting up), close out both console windows from Login.bat and TaskManager.bat. Wait 5 minutes (Minimum) and start it up again (the most crashes I've seen by rushing is twice in a row at any given startup)

