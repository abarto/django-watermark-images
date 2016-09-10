# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/xenial64"

  config.vm.define "django-watermark-images-vm" do |vm_define|
  end

  config.vm.hostname = "django-watermark-images.local"

  config.vm.network "forwarded_port", guest: 80, host: 8000
  config.vm.network "forwarded_port", guest: 8000, host: 8001

  config.vm.synced_folder ".", "/home/ubuntu/django_watermark_images/"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
    vb.cpus = 1
    vb.name = "django-watermark-images"
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y nginx git build-essential python3 python3.5-venv
  SHELL

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    pyvenv-3.5 --without-pip django_watermark_images_venv
    source django_watermark_images_venv/bin/activate
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python

    pip install -r django_watermark_images/requirements.txt

    cd django_watermark_images/django_watermark_images/

    python manage.py migrate
    python manage.py collectstatic --noinput
  SHELL

  config.vm.provision "shell", inline: <<-SHELL
    echo '
upstream django_watermark_images_upstream {
    server 127.0.0.1:8000 fail_timeout=0;
}

server {
    listen 80;
    server_name localhost;

    client_max_body_size 4G;

    access_log /home/ubuntu/django_watermark_images/nginx_access.log;
    error_log /home/ubuntu/django_watermark_images/nginx_error.log;

    location /static/ {
        alias /home/ubuntu/django_watermark_images/django_watermark_images/static/;
    }

    location /media/ {
        alias /home/ubuntu/django_watermark_images/django_watermark_images/media/;
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://django_watermark_images_upstream;
            break;
        }
    }
}
    ' > /etc/nginx/conf.d/django_watermark_images.conf

    /usr/sbin/service nginx restart
  SHELL

  config.vm.provision "shell", run: "always", privileged: false, inline: <<-SHELL
    source /home/ubuntu/django_watermark_images_venv/bin/activate
    cd /home/ubuntu/django_watermark_images/django_watermark_images
    gunicorn --bind 127.0.0.1:8000 --daemon --workers 1 django_watermark_images.wsgi
  SHELL
end
