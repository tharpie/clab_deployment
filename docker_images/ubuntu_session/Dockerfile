FROM ubuntu:22.04

RUN apt-get update && apt-get -y install openssh-server sudo
RUN apt-get install -y iproute2
RUN apt-get install -y net-tools

RUN service ssh start
EXPOSE 22
RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 admin 
RUN echo 'admin:admin' | chpasswd
COPY services.sh .
COPY server.py .
RUN chmod +x services.sh server.py
RUN chown 777 services.sh server.py
RUN apt-get install -y python3.10
#CMD ["/usr/bin/sh", "/etc/init.d/ssh", "start"]

#67c14513cad0
