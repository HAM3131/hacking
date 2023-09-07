FROM php:7-apache

ADD flag.txt /flag.txt
RUN chmod 0444 /flag.txt

ADD index.php /var/www/html/
RUN mkdir /var/www/html/uploads

RUN chown -R root:www-data /var/www/

RUN chmod 0755 /var/www/html
RUN chmod 0755 /var/www/html/index.php
RUN chmod 0733 /var/www/html/uploads/
