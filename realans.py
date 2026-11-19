import streamlit as st
import pandas as pd
import numpy as np
import base64
from sqlalchemy import text
import time

def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        return base64.b64encode(f.read()).decode()
def set_png_as_page_bg(images):
    img1 = get_base64_of_bin_file(images[0])
    img2 = get_base64_of_bin_file(images[1])
    img3 = get_base64_of_bin_file(images[2])

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background: transparent !important;
        }}

        [data-testid="stAppViewContainer"]::before {{
            content: "";
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;

            animation: bgChange 20s infinite;
        }}

        [data-testid="stAppViewContainer"] > .main {{
            position: relative;
            z-index: 1;
        }}

        @keyframes bgChange {{
            0%, 30% {{
                background-image: url("data:image/png;base64,{img1}");
            }}
            33%, 63% {{
                background-image: url("data:image/png;base64,{img2}");
            }}
            66%, 96% {{
                background-image: url("data:image/png;base64,{img3}");
            }}
            100% {{
                background-image: url("data:image/png;base64,{img1}");
            }}
        }}

        [data-testid="stHeader"] {{
            background: transparent !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def helper_click():
        if st.session_state['temporary'] == True:
            st.session_state['temporary'] = False
        else:  
            st.session_state['temporary'] = True

background = ["ag.png", "ag2.png", "background.png"]

set_png_as_page_bg(background)

conn = st.connection("my_database")
st.header("Book management System")

if 'temporary' not in st.session_state:
    st.session_state['temporary'] = False

if 'text_box' not in st.session_state:
    st.session_state.text_box = False

if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

if 'insert_book' not in st.session_state:
    st.session_state.insert_book = True

option = st.selectbox(
    "What do you want to query?",
    ("get book info by author", 
    "get books where price less than x", 
    "get book info by book_name",
    "get all connections",
    "get wishlisted by budget",
    "get bookmark of specified book",
    "get books by genre",
    "get review of book",
    "insert book with data",
    "delete book by name",
    "insert new tag",
    "insert bookmark of book",
    "insert review of book"),
)
temp = ""
if st.session_state['temporary']:
    if option in [
        "get book info by author", 
        "get books where price less than x", 
        "get book info by book_name",
        "get wishlisted by budget",
        "get bookmark of specified book",
        "get books by genre", 
        "delete book by name",
        "get review of book"]:
        st.session_state.text_box = True
        temp = st.text_input("Enter input", "")

    
# if st.session_state.text_box:
#     st.write(temp)
if option in ["insert book with data"]:
    st.session_state.insert_book = True
    t1 = st.text_input("insert id", "")
    t2 = st.text_input("insert name", "")
    t3 = st.text_input("insert author_first_name", "")
    t4 = st.text_input("insert author_second_name", "")
    t5 = st.text_input("insert date", "")
    t6 = st.text_input("insert price", "")

if option in ["insert new tag"]:
    text_box1 = st.text_input("Enter tag name", "")
    text_box2 = st.text_input("Enter book name", "")

if option in ["insert bookmark of book"]:
    text_box1 = st.text_input("Book name")
    text_box2 = st.text_input("Current page number")
    text_box3 = st.date_input("Last read date")
    text_box4 = st.text_area("Recap")

if option in ["insert review of book"]:
    text_box1 = st.text_input("Book name")
    text_box2 = st.number_input("Rating (0-10)", min_value=0.0, max_value=10.0, step=0.5)
    text_box3 = st.text_area("Review comment")
    text_box4 = st.date_input("Review date")

st.button("Enter", on_click= helper_click)
st.write(st.session_state['temporary']) 

if st.session_state.temporary:
    if option == "get book info by author":
        df = conn.query(
            "select * from books where author_first_name like :pattern or author_second_name like :pattern",
            params={"pattern": f"%{temp}%"}
        )
        st.dataframe(df)
        # Wicktor, Kerolina

    elif option == "get books where price less than x":
        if temp == "": temp = "10000.0"
        df = conn.query(
            "select * from books where price < :price",
            params={"price": float(temp)}
        )
        st.dataframe(df)

    elif option == "get book info by book_name":
        df = conn.query(
            "select * from books where book_name LIKE :name",
            params={"name": f"%{temp}%"}
        )
        st.dataframe(df)
    elif option == "get all connections":
        df = conn.query(
            "select * from collection"
        )
        st.dataframe(df)
    elif option == "get wishlisted by budget":
        if temp == "": temp = "100000.0"
        df = conn.query(
            "select w.book_id, b.book_name, w.budget from wishlist as w inner join books as b where w.book_id = b.book_id and budget < :budget",
            params={ "budget": float(temp)}
        )
        st.dataframe(df)
    elif option == "get bookmark of specified book":
        df= conn.query(
            "select bm.book_id, b.book_name, bm.page_no, bm.last_read, bm.recap from bookmarks as bm inner join books as b where bm.book_id = b.book_id and b.book_name like :name",
            params={"name": f"%{temp}%"}
        )
        st.dataframe(df)
   
    elif option == "get books by genre":
        df = conn.query(
            """
            SELECT t.tag_name, t.tag_type, b.book_id, b.book_name
            FROM tags AS t
            INNER JOIN book_tags AS bt
                ON t.tag_num = bt.tag_num
            INNER JOIN books AS b
                ON bt.book_id = b.book_id
            WHERE t.tag_name LIKE :genre
            """,
            params={"genre": f"%{temp}%"}
        )

        if df.empty:
            st.warning("No books found for this genre.")
        else:
            st.dataframe(df, use_container_width=True)
    
    elif option == "insert book with data":
        with conn.session as session:
            if t1 != "" and t2 != "" and t3 != "" and t4 != "" and t5 != "" and t6!="":
                session.execute(
                    text("INSERT INTO books (book_id, book_name, author_first_name, author_second_name, publication_date, price) VALUES (:id, :name, :a1, :a2, :date, :price)"),
                    params={"id": int(t1), "name": t2, "a1": t3, "a2": t4, "date": t5, "price": float(t6)}
                )
                session.commit()
    
    elif option == "delete book by name":
        with conn.session as session:
            if temp!="":
                session.execute(
                    text("DELETE FROM books where book_name LIKE :id"),
                    params={"id": f"%{temp}%"}
                )
                session.commit()

    elif option == "insert new tag":
        with conn.session as session:
            if text_box1.strip() != "" and text_box2.strip() != "":

                tag = session.execute( #check tag exist
                    text("""
                        select tag_num from tags
                        where tag_type = :type and tag_name = :name
                    """),
                    {"type": "genre", "name": text_box1.strip()}
                ).fetchone()

                if tag is None:
                    session.execute(
                        text("""
                            insert into tags (tag_type, tag_name)
                            values (:type, :name)
                        """),
                        {"type": "genre", "name": text_box1.strip()}
                    )

                    tag = session.execute(
                        text("""
                            select tag_num from tags
                            where tag_type = :type and tag_name = :name
                        """),
                        {"type": "genre", "name": text_box1.strip()}
                    ).fetchone()

                tag_num = tag[0]

                books = session.execute( #debug check 1
                    text("""
                        select book_id, book_name from books
                        where book_name like :name
                    """),
                    {"name": f"%{text_box2.strip()}%"}
                ).fetchall()

                st.write("Matching books:", books)

                if len(books) == 0: # debug check 1
                    st.error("No matching book found!")
                else:
                    result = session.execute(
                        text("""
                            insert ignore INTO book_tags (tag_num, book_id)
                            select :tag_num, book_id
                            from books
                            where book_name like :name
                        """),
                        {
                            "tag_num": tag_num,
                            "name": f"%{text_box2.strip()}%"
                        }
                    )

                    session.commit()

                    st.write("Rows inserted:", result.rowcount)

                    if result.rowcount > 0:
                        st.success("Tag associated with book!")
                    else:
                        st.warning("Relationship already exists!")

            else:
                st.warning("Enter both tag and book name.")
    elif option == "insert bookmark of book":
        if text_box1.strip() != "" and text_box2.strip() != "":
            with conn.session as session:
                result = session.execute(
                    text("""
                        insert into bookmarks (book_id, page_no, last_read, recap)
                        select book_id, :page_no, :last_read, :recap
                        from books
                        where book_name = :book_name
                        on duplicate key update
                            page_no = VALUES(page_no),
                            last_read = VALUES(last_read),
                            recap = VALUES(recap)
                    """),
                    {
                        "book_name": text_box1.strip(),
                        "page_no": int(text_box2),
                        "last_read": text_box3,
                        "recap": text_box4.strip()
                    }
                )

                session.commit()

                if result.rowcount > 0:
                    st.success("Bookmark saved successfully!")
                else:
                    st.warning("No matching book found!")
        else:
            st.warning("Enter book name, page number and last read date.")

    elif option == "insert review of book":
        if text_box1.strip() != "":
            with conn.session as session:
                result = session.execute(
                    text("""
                        insert into review (book_id, rating, comment, review_date)
                        select book_id, :rating, :comment, :review_date
                        from books
                        where book_name = :book_name
                        on duplicate key update
                            rating = VALUES(rating),
                            comment = VALUES(comment),
                            review_date = VALUES(review_date)
                    """),
                    {
                        "book_name": text_box1.strip(),
                        "rating": text_box2,
                        "comment": text_box3.strip(),
                        "review_date": text_box4
                    }
                )

                session.commit()

                if result.rowcount > 0:
                    st.success("Review saved successfully!")
                else:
                    st.warning("No matching book found!")
        else:
            st.warning("Enter a book name.")

    elif option == "get review of book":
        if temp != "":
            df = conn.query("""
            SELECT b.book_name, r.rating, r.comment, r.review_date
            FROM books AS b
            INNER JOIN review AS r
            ON b.book_id = r.book_id
            WHERE b.book_name LIKE :name""", params={"name": f"%{temp}%"})
            st.write(df)

    else:
        st.text("unknown error")

    time.sleep(3)
# insert into books (book_id, book_name, author_first_name, author_second_name, publication_date, price) values (1234, "raj", "vardhan", "singh", '2024-10-23', 1220.2);

     