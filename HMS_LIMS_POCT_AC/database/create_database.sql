-- Run as a PostgreSQL administrator. Adjust passwords before use.
CREATE USER poct_user WITH PASSWORD 'change_me';
CREATE DATABASE poct_management OWNER poct_user;
GRANT ALL PRIVILEGES ON DATABASE poct_management TO poct_user;