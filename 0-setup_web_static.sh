#!/usr/bin/env bash
# bash script that sets up web server for deployment of web_static

# install nginx if not already installed
if ! [ -x "$(command -v nginx)" ]; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create directories if they don't already exist
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared
sudo touch /data/web_static/releases/test/index.html

# Create a fake HTML file for testing
echo '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>' | sudo tee /data/web_static/releases/test/index.html >/dev/null
# creating or recreating the symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
sudo sed -i '/listen 80 default_server/a location /hbnb_static {alias /data/web_static/current/;}' /etc/nginx/sites-available/default

sudo service nginx restart

exit 0