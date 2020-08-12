FROM ubuntu:18.04
MAINTAINER vijayvenu1997@gmail.com

RUN apt-get update -y
RUN apt-get install python3-pip -y

WORKDIR /app
COPY . /app
RUN pip3 --no-cache-dir install -r requirement.txt


EXPOSE 5000
ENTRYPOINT ["sh"]
CMD ["run.sh"]


