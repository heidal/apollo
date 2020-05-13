FROM node:12.16-alpine3.9

EXPOSE 8080

RUN apk add python3 py3-pip bash git

USER node

COPY --chown=node:node frontend /app/
COPY --chown=node:node apollo-crypto /apollo-crypto

WORKDIR /app
RUN yarn install
ENTRYPOINT ["yarn", "start"]
