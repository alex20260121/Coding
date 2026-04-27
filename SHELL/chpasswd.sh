#!/usr/bin/env bash

IPFILE=$1
OLD_PASSWD=$2
NEW_PASSWD=$3

cat ${IPFILE} | while read ipaddr;
do
	ping -c 2 -i 0.2 ${ipaddr} >/dev/null 2>&1
	if [ $? -eq 0 ];then
		sshpass -p "${OLD_PASSWD}" ssh -n -o StrictHostKeyChecking=no dbaasadmin@${ipaddr} "echo 'dbaasadmin:${NEW_PASSWD}'| sudo chpasswd"
		if [ $? -ne 0 ];then
			echo "${ipaddr} chpasswd is failed." >> $IPFILE-chpasswd-failed.log
		else
			echo -e "${ipaddr} chpasswd is done, new password is $3"
		fi
	else
		echo "${ipaddr} chpasswd is failed." >> $IPFILE-network-error.log
	fi
done
