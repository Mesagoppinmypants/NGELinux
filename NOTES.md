# Allowing Outside Access

## Game Server Settings

For a VM, change network settings from NAT to bridged. Edit /etc/hosts and change the IP for the machine hostname to your public IP (http://icanhazip.com)

## SWG Config

Edit default.cfg in nge-swg-master/exe/linux and set node0 to your public IP address

## Ubuntu: Disable Firewall

(or just add rules to open the SWG ports)

sudo ufw disable

## SWG Database Modification

Open SQL Developer and go to the cluster_list table and change the address to your public IP

## DMZ or Port Forwarding

Go into your router configuration area and find the DMZ setting. Enable it and point it at the LAN address of the SWG server - you may also be able to simply forward the [SWG ports](ports) to the game server instead, which would be more secure.
   
