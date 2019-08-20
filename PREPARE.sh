#!/bin/bash

read -p 'Database name [BucketList]: ' database_name
database_name=${name:-BucketList}
read -p 'MySQL root password: ' mysql_root_password
read -p 'Database user: ' database_user
read -p 'Database user password: ' database_password

if [ ! -d "./secrets" ]; then
	mkdir secrets
fi

echo $mysql_root_password > ./secrets/mysql_root_pass.txt
echo $database_password > ./secrets/db_pass.txt
echo $database_user > ./secrets/db_user.txt
echo $database_name > ./secrets/db_name.txt
