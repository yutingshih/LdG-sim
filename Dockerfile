FROM ubuntu:18.04
SHELL ["/bin/bash", "-c"]

ENV TZ=Asia/Taipei
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt install -y vim git ssh net-tools python3 python3-pip

WORKDIR /root/LdG-sim
RUN git clone https://github.com/tings0802/LdG-sim.git /root/LdG-sim && \
	git checkout develop && \
	pip3 install -r requirements.txt