# puppet file that sets up webservers for the deployment of web_static

exec { 'Update package repository':
  command => '/usr/bin/apt-get update',
}
-> package { 'nginx':
  ensure => installed,
}
-> exec { 'Create web_static directories':
  command => '/usr/bin/mkdir -p "/data/web_static/releases/test/" "/data/web_static/shared/"',
}
-> exec { 'Create index.html file':
  command => '/usr/bin/echo "Hi!" | sudo tee /data/web_static/releases/test/index.html > /dev/null',
}
-> exec { 'Remove current directory':
  command => '/usr/bin/rm -rf /data/web_static/current',
}
-> exec { 'Create symbolic link':
  command => '/usr/bin/ln -s /data/web_static/releases/test/ /data/web_static/current',
}
-> exec { 'Change ownership of directories':
  command => '/usr/bin/chown -R ubuntu:ubuntu /data/',
}
-> exec { 'Configure Nginx for hbnb_static':
  command  => 'sudo sed -i "/^server {/a \ \n\tlocation \/hbnb_static {alias /data/web_static/current/;index index.html;}" /etc/nginx/sites-enabled/default',
  provider => shell,
}
-> exec { 'Restart Nginx service':
  command => '/usr/sbin/service nginx restart',
}

