# vpnbox

# About
Docker image with OpenConnect VPN server with untegrated Telegram bot to manage VPN users

#Howto run

mkdir /etc/vpnbox
nano /etc/vpnbox/bot.conf  # Fill fields in bot config
touch /etc/vpnbox/vpn.passwd   # Only if file not exists

docker run --name vpnbox --privileged -d --restart always -p 4443:443 --mount type=bind,source=/etc/vpnbox,target=/etc/ocserv/perm ghcr.io/globuslab/vpnbox:latest

# Update

docker stop vpnbox 
docker rm vpnbox
docker pull ghcr.io/globuslab/vpnbox:latest

docker run --name vpnbox --privileged -d --restart always -p 4443:443 --mount type=bind,source=/root/bot.conf,target=/etc/ocserv/bot.conf,readonly --mount type=bind,source=/root/vpn.passwd,target=/etc/ocserv/vpn.passwd  ghcr.io/globuslab/vpnbox:latest