FROM ubuntu:22.04

RUN apt-get update && apt-get -y install openssh-server sudo iproute2 net-tools python3.10 sshpass
RUN service ssh start
RUN useradd --system --create-home --home-dir /home/admin --shell /bin/bash \
            --gid root --groups sudo --uid 1000 admin

RUN echo 'admin:admin' | chpasswd
RUN mkdir -p /home/admin/.ssh
RUN chown admin:root /home/admin/.ssh

WORKDIR /home/admin
ADD --chown=admin:root --chmod=770 exec/* /home/admin/

EXPOSE 22
