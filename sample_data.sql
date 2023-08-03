Use secondary_hand_trading_sys;
INSERT INTO User(username, password) VALUES
('li', 'li'),
('jo', 'jo'),
('leo', 'leo'),
('tony', 'tony'),
('lily', 'lily'),
('white', 'white'),
('cerly', 'cerly'),
('Mike', 'Mike');

INSERT INTO Book(bookname, username, request, loaned_to) VALUES
('book_a', 'li', NULL, NULL),
('book_b', 'jo', NULL, NULL),
('book_c', 'li', NULL, 'jo'),
('book_d', 'jo', NULL, 'li');

INSERT INTO Messages(ID, sender, receiver, content, time) VALUES
(1, 'leo', 'tony', 'one', from_unixtime(1691043000)),
(2, 'leo', 'tony', 'two', from_unixtime(1691043100)),
(3, 'leo', 'tony', 'three', from_unixtime(1691043200)),
(4, 'leo', 'tony', 'six', from_unixtime(1691043600)),
(5, 'tony', 'leo', 'four', from_unixtime(1691043400)),
(6, 'tony', 'leo', 'five', from_unixtime(1691043500)),
(7, 'leo', 'lily', 'good morning', from_unixtime(1691043100)),
(8, 'leo', 'Mike', 'hahahaha', from_unixtime(1691043200)),
(9, 'white', 'tony', 'get up!', from_unixtime(1691040000)),
(10, 'cerly', 'lily', 'go school', from_unixtime(1691041000));
