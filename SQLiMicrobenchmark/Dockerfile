FROM php:8.0-apache
RUN docker-php-ext-install mysqli pdo pdo_mysql  && docker-php-ext-enable mysqli pdo pdo_mysql 
RUN sed -i 's/Require local/Allow from all/' /etc/apache2/mods-enabled/status.conf
RUN apt-get update && apt-get upgrade -y
