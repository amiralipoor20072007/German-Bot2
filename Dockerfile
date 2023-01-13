FROM ubuntu:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

COPY requirements.txt .
RUN apt-get update
RUN apt-get install python3 -y
RUN pip3 install --no-cache-dir -r requirements.txt -y

COPY . .

CMD ["bash", "start.sh"]
