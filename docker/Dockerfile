FROM ubuntu:14.04

RUN apt-get update --fix-missing && apt-get install -y python-pygame
RUN useradd -m -U -s /bin/bash pygame

USER pygame
WORKDIR /home/pygame
ENV SHELL /bin/bash

CMD /bin/bash
