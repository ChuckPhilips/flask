FROM mysql:5.7
ENV MYSQL_DATABASE=BucketList
ENV MYSQL_ROOT_PASSWORD=password
ENV MYSQL_USER=jay
ENV MYSQL_PASSWORD=jay
COPY ./flask.sql /docker-entrypoint-initdb.d/
COPY ./procedure.sql /docker-entrypoint-initdb.d/
