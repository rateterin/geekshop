#!/bin/sh

echo "upstream geekshop_docker {
    server geekshop:8000;
}

server {

    listen 80;
    servername ${DOMAIN_NAME};

    location / {
        proxy_pass http://geekshop_docker;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
    location /static/ {
        root /var/www/${DOMAIN_NAME};
    }

    location /media/ {
        root /var/www/${DOMAIN_NAME};
    }

}" > /etc/nginx/conf.d/default.conf
