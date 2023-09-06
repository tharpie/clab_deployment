FROM ubuntu:22.04

RUN apt-get update && apt-get -y install openssh-server sudo iproute2 net-tools python3.10
RUN service ssh start
RUN useradd --system --create-home --home-dir /home/admin --shell /bin/bash \
            --gid admin --groups sudo --uid 1000 admin

RUN mkdir --mode 600 -p /home/admin/.ssh
RUN echo 'admin:admin' | chpasswd

WORKDIR /home/admin
ADD --chown admin:admin --chmod=770 exec/* /home/admin/

EXPOSE 22
