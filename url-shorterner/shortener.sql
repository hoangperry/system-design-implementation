CREATE USER shortener_server;
ALTER ROLE shortener_server WITH PASSWORD 'secret123';
CREATE DATABASE shortener;
GRANT ALL PRIVILEGES ON DATABASE shortener TO postgres;
