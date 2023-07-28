--CREATE DATABASE
DROP DATABASE IF EXISTS secondary_hand_trading_sys;
CREATE DATABASE IF NOT EXISTS secondary_hand_trading_sys
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;
USE secondary_hand_trading_sys;

-- CREATE TABLE User();

CREATE TABLE Book(
    book_name varchar(100)
);

CREATE TABLE User(
    username varchar(50) NOT NULL,
    password varchar(50) NOT NULL
);