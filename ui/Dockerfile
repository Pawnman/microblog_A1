FROM node:19-alpine AS build
WORKDIR /app

COPY . .
#RUN npm install
#RUN npm run build

FROM nginx:alpine
COPY nginx.conf /etc/nginx/
COPY src /usr/share/nginx/html
EXPOSE 80
