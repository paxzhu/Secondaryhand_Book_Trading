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
    bookname varchar(100) NOT NULL,
    username varchar(50) NOT NULL,
    request varchar(50),
    loaned_to varchar(50),
    PRIMARY KEY(bookname),
    FOREIGN KEY (username)
        REFERENCES User(username)
);

CREATE TABLE Requests(
    borrower varchar(50) NOT NULL,
    bookname varchar(100) NOT NULL,
    PRIMARY KEY(borrower, bookname),
    FOREIGN KEY(borrower)
        REFERENCES User(username),
    FOREIGN KEY(bookname)
        REFERENCES Book(bookname)
);

CREATE TABLE Messages(
    ID INT NOT NULL AUTO_INCREMENT,
    sender varchar(50) NOT NULL,
    receiver varchar(50) NOT NULL,
    content varchar(1000) NOT NULL,
    time TIMESTAMP NOT NULL,
    PRIMARY KEY(ID),
    FOREIGN KEY(sender)
        REFERENCES User(username),
    FOREIGN KEY(receiver)
        REFERENCES User(username)
);

CREATE TABLE Follows(
    follower varchar(50) NOT NULL,
    followed varchar(50) NOT NULL,
    PRIMARY KEY(follower, followed),
    FOREIGN KEY(follower)
        REFERENCES User(username),
    FOREIGN KEY(followed)
        REFERENCES User(username)
);

CREATE TABLE Click(
    book varchar(100) NOT NULL,
    count INT NOT NULL,
    PRIMARY KEY(book),
    FOREIGN KEY(book)
        REFERENCES Book(bookname)
);