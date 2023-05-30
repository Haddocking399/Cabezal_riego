CREATE DATABASE IF NOT EXISTS sprinkler_head;
CREATE USER IF NOT EXISTS 'sprinkler_user'@'%' IDENTIFIED BY 'P455w0rd';
GRANT ALL ON `sprinkler_head`.* TO 'sprinkler_user'@'%' IDENTIFIED BY 'P455w0rd';
FLUSH PRIVILEGES;