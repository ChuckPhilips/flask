FROM mysql:5.7
COPY ./flask.sql /docker-entrypoint-initdb.d/
COPY ./procedure.sql /docker-entrypoint-initdb.d/
COPY ./flask.cnf /etc/mysql/conf.d
