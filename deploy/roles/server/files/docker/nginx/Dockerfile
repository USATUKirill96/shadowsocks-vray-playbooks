FROM nginx
 
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
 
ADD ./nginx/default.conf /etc/nginx/conf.d/default.conf