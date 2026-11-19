--get books by author
SELECT * FROM books 
WHERE 
author LIKE "%Kamila%";

--get books by price
SELECT * FROM books 
WHERE 
price < 50;

--get book info
SELECT * FROM books 
WHERE 
book_name LIKE "%Intro%";

--get books in collection
SELECT * FROM collection;

--get books before date t
SELECT * FROM collection 
WHERE 
DATEDIFF(purchase_date, DATE"2025-10-23")>5;

--get wishlisted
SELECT w.book_id, b.book_name 
FROM wishlist as w 
INNER JOIN 
books as b 
WHERE 
w.book_id = b.book_id;

--get wishlisted published
SELECT w.book_id, b.book_name 
FROM wishlist as w 
INNER JOIN 
books as b 
WHERE 
w.book_id = b.book_id AND w.is_published = TRUE;

--get wishlisted budget
SELECT w.book_id, b.book_name 
FROM wishlist as w 
INNER JOIN 
books as b 
WHERE 
w.book_id = b.book_id AND w.budget < 5000;

--get bookmark of book
SELECT bm.book_id, b.book_name, bm.page_no, bm.last_read 
FROM bookmarks as bm
INNER JOIN
books as b
WHERE 
bm.book_id = b.book_id AND b.book_name = "Nasza klasa";

--get review by book
SELECT r.book_id, b.book_name, r.rating, r.comment, r.review_date 
FROM 
review as r 
INNER JOIN 
books as b 
WHERE 
b.book_id = r.book_id AND b.book_name = "Nasza klasa";

SELECT t1.book_id, t1.book_name FROM 
(
    SELECT bt.book_id, b.book_name, bt.tag_num
    FROM 
    book_tags as bt 
    INNER JOIN 
    books as b
    WHERE 
    b.book_id = bt.book_id
) as t1 
INNER JOIN 
(
    SELECT bt.book_id, bt.tag_num, t.tag_name 
    FROM 
    book_tags as bt
    INNER JOIN
    tags as t
    WHERE bt.tag_num = t.tag_num
) as t2 
WHERE 
t1.tag_num = t2.tag_num AND t2.tag_name = "Horror";

--insert book -- TODO: update language
INSERT INTO books 
(book_name, author, publisher, book_language, price) 
VALUES 
("Harry Potter", "Charles Dickens", NULL, "English", 500.5);

--insert book in collection
INSERT INTO collection 
(book_id, purchase_date, purchased_from, is_physical) 
VALUES 
(12, "2024-12-31", "shipra nagar", TRUE);

--insert book in wishlist
INSERT INTO wishlist 
(book_id, budget, is_published) 
VALUES 
(13, 445, TRUE);

--update bookmark
UPDATE bookmarks
SET page_no = 34, last_read = CURDATE() 
WHERE book_id = 9780512554446;

--update review
UPDATE review 
SET comment = "this is comment", rating = 3
WHERE book_id = 9780512554446;

--create new tag
INSERT INTO book_tags (tag_num, book_id) VALUES (12, 33);

--insert book to tag
INSERT INTO tags (tag_type, tag_name) VALUES ("genre", "crime");