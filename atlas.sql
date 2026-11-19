DROP DATABASE IF EXISTS atlas;
CREATE DATABASE atlas;
USE atlas;    

CREATE TABLE books (
    book_id             BIGINT,
    book_name           VARCHAR(256) NOT NULL,
    author_first_name   VARCHAR(256),
    author_second_name    VARCHAR(256),
    publication_date    DATE,
    publisher           VARCHAR(256),
    price               NUMERIC(12, 3),

    CONSTRAINT books_book_id_pk PRIMARY KEY (book_id)
);

CREATE TABLE collection ( 
    book_id         BIGINT,
    purchase_date   DATE,
    purchased_from  VARCHAR(256),
    is_physical     BOOLEAN,

    CONSTRAINT collection_book_id_pk PRIMARY KEY (book_id),
    CONSTRAINT collection_book_id_fk FOREIGN KEY (book_id) REFERENCES books(book_id)
);

CREATE TABLE wishlist ( 
    book_id         BIGINT,
    budget          NUMERIC(12, 3),
    is_published    BOOLEAN,

    CONSTRAINT wishlist_book_id_pk PRIMARY KEY (book_id),
    CONSTRAINT wishlist_book_id_fk FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
);

CREATE TABLE bookmarks (
    book_id     BIGINT,
    page_no     INT,
    last_read   DATE,
    recap       TEXT,
    CONSTRAINT bookmarks_book_id_pk PRIMARY KEY (book_id),
    CONSTRAINT bookmarks_book_id_fk FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
);

CREATE TABLE review (
    book_id     BIGINT,   
    rating      NUMERIC(4, 2) DEFAULT 0,
    comment     TEXT,
    review_date DATE,

    CONSTRAINT review_book_id_pk PRIMARY KEY (book_id),
    CONSTRAINT review_book_id_fk FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
);

CREATE TABLE tags (
    tag_type    VARCHAR(256),
    tag_name    VARCHAR(256),
    tag_num     INT AUTO_INCREMENT,

    CONSTRAINT tags_tag_num_pk PRIMARY KEY (tag_num)
);

CREATE TABLE book_tags (
    tag_num     INT,
    book_id     BIGINT,

    CONSTRAINT book_tags_book_id_tag_num_pk PRIMARY KEY (book_id, tag_num),
    CONSTRAINT book_tags_tag_num_fk FOREIGN KEY (tag_num) REFERENCES tags(tag_num),
    CONSTRAINT book_tags_book_id_fk FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
);

