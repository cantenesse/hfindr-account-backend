#!/bin/bash

environment=$1
action=$2
version=$(cat VERSION)

MYSQL_ROOT_PASSWORD=hfindr

# lib
database_clean () {
  echo "Stopping database container"
  docker stop account-mysql

  echo "Removing database container"
  docker rm account-mysql
}

network_clean () {
  echo "Removing devnet network"
  docker network rm devnet
}

network_up () {
  echo "creating dev network: 10.10.10.0/24"
  docker network create --subnet 10.10.10.0/24 devnet
  echo "network created"
}

database_up () {
  echo "starting database"
  docker run -p 3306:3306 --name account-mysql --network=devnet --ip=10.10.10.10 -e MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD -d mysql:8.0
  sleep 20
  echo "database started, listing on 3306"
}

database_migrate () {
  echo "Migrating database"
  docker run --rm --network=devnet -v $(pwd)/ops/database:/flyway/sql flyway/flyway -url=jdbc:mysql://10.10.10.10:3306 -schemas=account_v${version} -user=root -password=$MYSQL_ROOT_PASSWORD migrate
} 

if [[ $environment == "dev" ]];then
  if [[ $action == "up" ]];then
    network_up
    database_up
    database_migrate
  fi

  if [[ $action == "clean" ]];then
    database_clean
    network_clean
  fi
fi



