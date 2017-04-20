sudo apt-get install python-devel -y
apt-get install wget -y
apt-get install openssl-devel -y
wget --no-check-certificate https://bootstrap.pypa.io/ez_setup.py
python ez_setup.py
cd /usr/local/src
wget --no-check-certificate https://github.com/libevent/libevent/releases/download/release-2.1.8-stable/libevent-2.1.8-stable.tar.gz
tar zxf libevent-2.1.8-stable.tar.gz
cd libevent-2.1.8-stable
./configure
make
make install
cp -f /usr/local/lib/libevent* /usr/lib/
easy_install-2.7 greenlet
easy_install-2.7 pip
pip install gevent
pip install PyMySQL
pip install jinja2
pip install requests
pip install fabric
pip install celery
pip install tqdm
apt-get install git autoconf gcc gcc-c++ make automake -y
cd /usr/src
git clone https://github.com/nmap/nmap.git
cd nmap
./configure
make && make install