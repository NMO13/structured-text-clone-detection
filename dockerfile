# Note: Install nvidia container-toolkit first, as described here:
# https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

# syntax=docker/dockerfile:1
FROM nvidia/cuda:10.2-base
CMD nvidia-smi

#set up python3
RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y curl
RUN apt-get install unzip
RUN apt-get -y install python3
RUN apt-get -y install python3-pip

WORKDIR /code
ENV FLASK_APP=api
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production
ENV DATA_PATH=/code/completeOSCAT
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN mkdir -p data
#CMD ["flask", "run"]
