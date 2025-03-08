# sqli_lab

Play with `INSERT` and `SELECT` query.

## How to use

- Run the docker compose file

```bash
# run the app in detached  mode
sudo docker-compose up --build -d

# open the python app
http://127.0.0.1:8000/scenario-1

# open the php app
http://127.0.0.1:8010/lookup.php

# stop and delete the container
sudo docker-compose down

# clean the docker images
chmod a+x clean_docker.sh 
./clean_docker.sh
```


## local php development notes

- set php-dev-server version: Settings -> PHP cli -> set the php virtual env `PHP_8.2.25_phpenv`
  - php language level = 8.2
- In Edit Config: create a php_dev_server - "PHP Build-in Web Server"
  - host: 127.0.0.1, port: 3030
  - set the Document root to the `/home/asinha/code_dev/php/fb_login/app` (location of your php file)
  - set the env variable: DEV_ENV=local in web server
  - when that value is blank (for docker deployment) it will be set to "mariadb"
  - check if mysqli lib is installed: `php -m | grep mysqli`
  - enable the extension: `subl /home/asinha/.phpenv/versions/8.3.13/etc/php.ini` -> uncomment the line
- In the PHP Script -> `address_lookup.php`, set the interpreter `PHP_8.2.25_phpenv`

- before push to the remote repo check if everything works fine in local docker env