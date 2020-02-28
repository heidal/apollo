FROM node:12.16-alpine3.9

EXPOSE 3000

RUN apk add python3 py3-pip bash git

COPY frontend /app
WORKDIR /app
RUN yarn install
ENTRYPOINT ["yarn", "start"]