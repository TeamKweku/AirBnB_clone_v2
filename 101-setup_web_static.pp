# puppet file that sets up webservers for the deployment of web_static

# Update system
exec { 'update system':
  command => '/usr/bin/apt-get update',
}

# Install nginx server
package { 'nginx':
  ensure  => 'installed',
  require => Exec['update system']
}

# Create parent directories using mkdir -p
exec { 'create_web_static_directories':
  command => '/bin/mkdir -p /data/web_static/releases/test /data/web_static/shared',
}

# Create a fake HTML file for testing
file { '/data/web_static/releases/test/index.html':
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => present,
  content => "server {
      listen 80 default_server;
      server_name _;

      location /hbnb_static {
          alias /data/web_static/current/;
      }

      # Add custom HTTP headers
      add_header X-Served-By '"$hostname"';

      # Redirect 301 Moved Permanently
      location /redirect_me {
          rewrite ^/redirect_me https://www.youtube.com/watch?v=xJJsoquu70o/ permanent;
      }
  }",
  require => Package['nginx'],
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
}

# Start nginx service
service { 'nginx':
  ensure  => running,
  require => [Package['nginx'], Exec['create_web_static_directories'], File['/data/web_static/current']],
}

