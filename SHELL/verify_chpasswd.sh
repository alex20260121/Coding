#!/usr/bin/env bash

IPFILE=$1
PASSWD=$2
cat $IPFILE | while read line;
do
	ping -c 2 -i 0.2 $line >/dev/null 2>&1
	if [ $? -eq 0 ];then
		sshpass -p $PASSWD ssh -n -o StrictHostKeyChecking=no dbaasadmin@$line "uptime"
		if [ $? -ne 0 ];then
			echo "$line" >> $IPFILE-password-verify-failed.log
		else
			echo "$line Password verification successful."
		fi
	else
		echo "$line" >> $IPFILE-network-connectivity-error.log
	fi
done
