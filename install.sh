#!/bin/bash
# CYBERPLOT MANAGER
# This script will install cyberplot manager
# https://github.com/cyberplot/cyberplot-web

# Ask user for hostname
echo '[?] Enter hostname for your server without HTTP or WWW (ex. cyberplot.io) or IP address:'
read hostname

# Create new user
mkdir /home/cyberplot
useradd cyberplot -d /home/cyberplot
echo '[?] Please input user password:'
passwd cyberplot
usermod -aG sudo cyberplot
usermod -aG www-data cyberplot
usermod --shell /bin/bash cyberplot
chown cyberplot:cyberplot /home/cyberplot

# Create firewall rules
ufw allow 80
ufw allow ssh
ufw --force enable

# Install necessary dependencies
export DEBIAN_FRONTEND=noninteractive
apt update
apt install --assume-yes python3-pip python3-dev python3-venv mysql-server sudo nginx libmysqlclient-dev nodejs npm

# Generate SQL password
export sqlpass=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

# Configure MySQL
mysql -u root -e "create user 'cyberplot'@'localhost' identified by '${sqlpass}'"
mysql -u root -e "create database cyberplot"
mysql -u root -e "grant all privileges on cyberplot.* to cyberplot@localhost"

# Move directory to new user's home directory and transfer ownership
cd ..
mv cyberplot-web /home/cyberplot/
chown cyberplot:www-data -R /home/cyberplot/
cd /home/cyberplot/cyberplot-web

# Replace paths to correspond with home directory
sed -i -e 's@~@'$(pwd)'@g' backend/cyberplotapi.ini
sed -i -e 's@~@'$(pwd)'@g' config/cyberplotapi.service
sed -i -e 's@~@'$(pwd)'@g' config/cyberplot

# Store login information to database
sed -i -e 's/SQLALCHEMY_DATABASE_URI.*/SQLALCHEMY_DATABASE_URI = "mysql:\/\/cyberplot:'${sqlpass}'@localhost:3306\/cyberplot"/g' backend/cyberplot/config.py

# Generate secret key for SQLAlchemy
export secret=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1) 
sed -i -e 's/SECRET_KEY.*/SECRET_KEY = "'${secret}'"/g' backend/cyberplot/config.py

# Run frontend on port 80 instead of 8080
sed -i -e 's/port: 8080/port: 80/g' frontend/cyberplot/config/index.js

# Configure webpack
sed -i -e 's/"dev":.*/"dev": "webpack-dev-server --inline --progress --config build\/webpack.dev.conf.js --host 0.0.0.0 --public '${hostname}':80",/g' frontend/cyberplot/package.json

# Move service file to system directory
mv config/cyberplotapi.service /etc/systemd/system/

# Tell nginx our hostname/IP
sed -i -e 's/SERVER/'${hostname}'/g' config/cyberplot

# Configure nginx
mv config/cyberplot /etc/nginx/sites-available
ln -s /etc/nginx/sites-available/cyberplot /etc/nginx/sites-enabled
rm /etc/nginx/sites-enabled/default
ufw allow 'Nginx Full'

# Point frontend API to specified hostname/IP
export CYBERPLOT_URL=${hostname}
su -c 'echo "export CYBERPLOT_URL="'${hostname}' > ~/.bash_profile' cyberplot
su -c 'echo "export CYBERPLOT_URL="'${hostname}' > ~/.bashrc' cyberplot

# Initialize Python virtual environment and database, install pip dependencies
cd backend
su -c 'python3 -m venv venv' cyberplot
su -c 'source venv/bin/activate; pip3 install -r requirements.txt; pip3 install mysqlclient; pip3 install uwsgi; python3 manage.py db init; python3 manage.py db migrate; python3 manage.py db upgrade' cyberplot

# Install npm dependencies, build frontend code
cd ../frontend/cyberplot
su -c 'npm install' cyberplot
su -c 'npm run build' cyberplot

# Restart services
systemctl enable cyberplotapi
systemctl restart nginx
systemctl start cyberplotapi

# Ignore changes to files
cd ../..
git update-index --assume-unchanged frontend/cyberplot/package.json
git update-index --assume-unchanged frontend/cyberplot/config/index.js
git update-index --assume-unchanged backend/cyberplot/config.py
git update-index --assume-unchanged backend/cyberplotapi.ini
git update-index --assume-unchanged config/cyberplot
git update-index --assume-unchanged config/cyberplotapi.service

echo '[!] Install finished, cyberplot manager should be running at http://'${hostname}'/'