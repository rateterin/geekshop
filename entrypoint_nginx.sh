#!/bin/sh

cd ~/$(DOMAIN_NAME)/

ln -s /etc/nginx/sites-available/geekshop.conf /etc/nginx/sites-enabled/
