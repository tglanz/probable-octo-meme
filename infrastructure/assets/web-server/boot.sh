#!/bin/bash -ex

echo "Executing boot script"

apt update
apt -y upgrade

apt install -y nginx
# replace index.nginx-debuan.html with index.html
sed -i "s/index\.nginx-debian\.html/index\.html/g" /etc/nginx/sites-enabled/default
systemctl enable --now nginx