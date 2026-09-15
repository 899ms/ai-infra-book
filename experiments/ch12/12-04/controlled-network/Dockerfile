FROM python:3.11-slim
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends iproute2 iputils-ping iperf3 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir aioquic==1.3.0 h11==0.16.0 Pillow==12.1.1
WORKDIR /experiment
