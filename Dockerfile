FROM node:6

RUN npm install -g grunt
RUN mkdir -p /src
WORKDIR /src
