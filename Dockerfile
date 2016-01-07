FROM ubuntu:14.04
MAINTAINER Alexey Kaytaz
RUN apt-get update
RUN apt-get install xvfb python-pip vim firefox git --yes
RUN pip install pyvirtualdisplay
RUN pip install selenium
