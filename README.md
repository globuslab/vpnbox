# vpnbox

# About
Docker image with OpenConnect VPN server with untegrated Telegram bot to manage VPN users

#Howto run

nano /root/bot.conf  # Fill fields in bot config
touch /root/vpn.passwd # Only if file not exists

docker run --privileged -d --restart always -p 4443:443 --mount type=bind,source=/root/bot.conf,target=/etc/ocserv/bot.conf,readonly --mount type=bind,source=/root/vpn.passwd,target=/etc/ocserv/vpn.passwd  <image_name>
