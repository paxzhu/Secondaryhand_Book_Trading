Use secondary_hand_trading_sys;
INSERT INTO User(username, password) VALUES
('li', 'li'),
('jo', 'jo');

INSERT INTO Book(book_name, username, request, loaned_to) VALUES
('book_a', 'li', NULL, NULL),
('book_b', 'jo', NULL, NULL),
('book_c', 'li', NULL, 'jo'),
('book_d', 'jo', NULL, 'li');



