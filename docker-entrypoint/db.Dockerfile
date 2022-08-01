FROM postgres:11.5-alpine
COPY init_db.sql /docker-entrypoint-initdb.d/