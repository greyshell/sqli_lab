#!/bin/bash
# author: greyshell

sudo docker-compose down
sudo docker stop $(sudo docker ps -a -q);
sudo docker rm $(sudo docker ps -a -q);
sudo docker volume rm $(sudo docker volume ls -f dangling=true -q);
sudo docker rmi -f $(sudo docker images -a -q);
sudo docker system prune -a --volumes -f

