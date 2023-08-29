const db = db.

db.Books.insertMany([
{
    name: "book_a",
    belong_to: "li",
    request: [],
    loaned_to: "",
},
{
    name: "book_b",
    belong_to: "jo",
    request: [],
    loaned_to: "",
},
{
    name: "book_c",
    belong_to: "li",
    request: [],
    loaned_to: "jo",
},
{
    name: "book_d",
    belong_to: "jo",
    request: [],
    loaned_to: "li",
},
])

db.User.insertMany([
    {
        username: 'li',
        password: 'li',
        books: ['book_a', 'book_c']
    },
    {
        username: 'jo',
        password: 'jo',
        books: ['book_b', 'book_d']
    }

])


INSERT INTO User(username, password) VALUES
('li', 'li'),
('jo', 'jo'),
('leo', 'leo'),
('tony', 'tony'),
('lily', 'lily'),
('white', 'white'),
('cerly', 'cerly'),
('SHTS', 'SHTS'),
('Mike', 'Mike');