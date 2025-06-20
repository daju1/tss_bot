CREATE DATABASE tss;
use tss;

CREATE TABLE tss_messages (
    msg_id integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
    date TIMESTAMP,
    username VARCHAR(20),
    first_name VARCHAR(20),
    msg VARCHAR(255)
) DEFAULT CHARACTER SET=utf8;
