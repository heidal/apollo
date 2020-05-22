FROM node:latest as build-stage
WORKDIR /app
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn install
COPY ./frontend .
RUN yarn build

FROM nginx as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx/nginx.conf /etc/nginx/nginx.conf
