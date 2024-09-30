FROM mysql:latest
WORKDIR /mysql
COPY create_database.sql /docker-entrypoint-initdb.d/
RUN chmod -R 755 /docker-entrypoint-initdb.d/