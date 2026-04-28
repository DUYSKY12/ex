FROM node:18-alpine
WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install --production

COPY . .

EXPOSE 8006
CMD ["node", "src/app.js"]
