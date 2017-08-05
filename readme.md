Installation on debian-like system. Use sudo:

* Clone project: git clone git@github.com:pimshtein/proxy.git
* Create a service file: touch /etc/systemd/system/proxy.service
* Change rights: chmod 664 /etc/systemd/system/proxy.service
* Add to torrent-bot.service this content:  

[Unit]  
Description=Proxy server  
After=network.target  
  
[Service]  
Type=simple  
User=root (on behalf of whom to run)  
ExecStart=/var/www/my/proxy/proxy.sh  
  
[Install]  
WantedBy=multi-user.target  
* Write path to proxy_server.py in proxy.sh (use your path): 
python3 /var/www/my/proxy/proxy_server.py 
* Feel values in config.py
* Run proxy server: sudo systemctl start proxy.service