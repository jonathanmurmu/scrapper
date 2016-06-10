
#!/usr/bin/env bash
echo "--------------Updating--------------"
apt-get update

echo "--------------Installing pip------------"
sudo apt-get -y install python-pip python-dev build-essential


echo "--------------Installing virtualenv----------------"
sudo pip install virtualenv

echo "--------------Upgrading pip-------------"
sudo pip install --upgrade pip

echo "--------------Creating a virtual env named --------"
sudo mkdir env
virtualenv -p /usr/bin/python3 env/scrapper
source /home/vagrant/env/scrapper/bin/activate
cd /home/vagrant/scrapper/

echo "--------------Installing mysql---------------------"
MYSQL_PASSWORD="mindfire"
sudo apt-get -y install python3-dev
echo "mysql-server-5.5 mysql-server/root_password password $MYSQL_PASSWORD" | debconf-set-selections
echo "mysql-server-5.5 mysql-server/root_password_again password $MYSQL_PASSWORD" | debconf-set-selections

apt-get -y install mysql-client mysql-server sqlite3 
apt-get -y install python-mysqldb libmysqlclient-dev python-mysql.connector python3-mysql.connector

echo "--------------Installing requirements----------------------"
sudo chown -R vagrant:vagrant /home/vagrant/env/
#done to install pillow in the requirement.txt
sudo apt-get -y install libjpeg8-dev
pip install -r requirement.txt



