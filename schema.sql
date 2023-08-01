--CREATE DATABASE
DROP DATABASE IF EXISTS secondary_hand_trading_sys;
CREATE DATABASE IF NOT EXISTS secondary_hand_trading_sys
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;
USE secondary_hand_trading_sys;

-- CREATE TABLE User();

CREATE TABLE User(
    username varchar(50) NOT NULL,
    password varchar(50) NOT NULL,
    PRIMARY KEY(username)
);

CREATE TABLE Book(
    book_name varchar(100),
    username varchar(50) NOT NULL,
    request varchar(50),
    loaned_to varchar(50),
    PRIMARY KEY(book_name),
    FOREIGN KEY (username)
        REFERENCES User(username)
);

