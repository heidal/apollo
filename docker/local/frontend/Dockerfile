FROM node:12.16-alpine3.9

EXPOSE 19000
EXPOSE 19001
EXPOSE 19002
EXPOSE 19006

RUN apk add python3 py3-pip bash
RUN npm install -g expo-cli

COPY frontend /app
WORKDIR /app
ENTRYPOINT ["yarn", "start", "--lan", "--web"]