FROM node:12.16-alpine3.9

EXPOSE 8080

RUN apk add git

USER node

COPY --chown=node:node frontend /app/

WORKDIR /app
RUN yarn install
ENTRYPOINT ["yarn", "start"]
