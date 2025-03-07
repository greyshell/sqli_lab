FROM php:8.0-apache

RUN apt-get update -y
RUN apt-get install -y gcc wget curl net-tools
RUN docker-php-ext-install mysqli
RUN docker-php-ext-enable mysqli
WORKDIR /var/www/html
COPY login.php .
COPY source_code.txt .
COPY config.php .
RUN chmod 755 config.php
RUN chmod 755 login.php

