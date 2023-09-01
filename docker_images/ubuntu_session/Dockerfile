FROM ubuntu:22.04

RUN apt-get update && apt-get -y install openssh-server sudo
RUN apt-get install -y iproute2
RUN apt-get install -y net-tools
RUN apt-get install -y python3.10
RUN service ssh start
EXPOSE 22
RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 admin 
RUN echo 'admin:admin' | chpasswd
COPY start_ssh.sh .
COPY sleep.py .
RUN chmod +x start_ssh.sh sleep.py
RUN chown 777 start_ssh.sh sleep.py
