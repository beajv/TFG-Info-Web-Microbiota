# nginx state for serving content
FROM nginx
RUN rm -f /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/

COPY ser.key /etc/nginx/
COPY ser.pem /etc/nginx/

COPY nginx.conf /etc/nginx/

WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY dist .


RUN chown -R nginx:nginx /usr/share/nginx/html && chmod -R 755 /usr/share/nginx/html && \
        chown -R nginx:nginx /var/cache/nginx && \
        chown -R nginx:nginx /var/log/nginx && \
        chown nginx:nginx /etc/nginx/ser.key && \
        chown nginx:nginx /etc/nginx/ser.pem


RUN touch /var/run/nginx.pid && \
        chown -R nginx:nginx /var/run/nginx.pid && \
        chmod -R 755 /var/run/nginx.pid 
                          
USER nginx



ENTRYPOINT ["nginx", "-g", "daemon off;"]
