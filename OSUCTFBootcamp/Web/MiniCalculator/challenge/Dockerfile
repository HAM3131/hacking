from mhart/alpine-node:12

WORKDIR /app
COPY src .


RUN npm install

RUN chown root:root .
# Set permissions for directories
RUN find . -type d -print0 | xargs -0 chmod 755

RUN adduser -D -g '' server
USER server
EXPOSE 8080
ENV NODE_ENV=production
CMD [ "npx", "pm2-runtime", "index.js"]
