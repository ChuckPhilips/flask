#!/bin/bash

read -p 'MySQL root password: ' mysql_root_password
read -p 'Database user password: ' database_password

if [ ! -d "./secrets" ]; then
	mkdir secrets
fi

echo $mysql_root_password > ./secrets/mysql_root_pass.txt
echo $database_password > ./secrets/wp_db_pass.txt
