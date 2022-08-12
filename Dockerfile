FROM home/misha/PycharmProjects/pythonProject
MAINTAINER Nagnalov M
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
RUN python3 main.py
