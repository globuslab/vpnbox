FROM almalinux:latest
LABEL name = "VPNBox"
LABEL author = "Globuslab"
RUN dnf install -y epel-release
RUN dnf repolist enabled
RUN dnf install -y ocserv
RUN yum install gnutls-utils
COPY ./configs /etc/ocserv
COPY ./certs/server-cert.pem /etc/ocserv/server-cert.pem
COPY ./certs/server-key.pem /etc/ocserv/server-key.pem
COPY ./scripts/bot.py /etc/ocserv/bot.py
#RUN certtool --generate-privkey --outfile /etc/ocserv/ca-key.pem
#RUN certtool --generate-self-signed --load-privkey /etc/ocserv/ca-key.pem --template /etc/ocserv/certs/ca.tmpl --outfile  /etc/ocserv/ca-cert.pem
#RUN certtool --generate-privkey --outfile /etc/ocserv/server-key.pem
#RUN certtool --generate-certificate --load-privkey /etc/ocserv/server-key.pem --load-ca-certificate /etc/ocserv/ca-cert.pem --load-ca-privkey /etc/ocserv/ca-key.pem --template /etc/ocserv/certs/server.tmpl --outfile /etc/ocserv/server-cert.pem
RUN chown -R ocserv /etc/ocserv
CMD ["/etc/ocserv/bot.py"]
EXPOSE 443
