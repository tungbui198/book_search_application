import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

from onto_query import search_book
from field_extraction import extract_fields


def main():
    st.set_page_config(
        page_title="Book Search Application", page_icon=":bulb:", layout="wide"
    )

    # Custom styles to improve the appearance
    st.markdown(
        """
    <style>
    .app-banner {
        background-image: url('https://i.imgur.com/fuOTlT3.jpg');
        background-size: cover;
        padding: 50px;
        text-align: center;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Custom header with background
    st.markdown(
        '<div class="app-banner"><h1 style="color:white;">Book Search Application</h1></div>',
        unsafe_allow_html=True,
    )

    if "full_data" not in st.session_state:
        books_info = search_book()
        full_data = pd.DataFrame(books_info)
        st.session_state["full_data"] = full_data

    data_changed = False
    with st.container():
        selected = option_menu(
            menu_title=None,
            options=[
                "Quick Search",
                "Advanced Search",
                "Semantic Search",
            ],
            icons=[
                "clipboard-data",
                "laptop",
            ],
            orientation="horizontal",
        )
        if selected == "Quick Search":
            keyword = st.text_input("Keyword")
            keytype = st.selectbox(
                "Select type to search: ",
                options=[
                    "Category",
                    "Title",
                    "Author",
                    "Publisher",
                    "Language",
                    "Extension",
                    "NumberPage",
                    "PublishYear",
                ],
            )
            search = st.button("Search")
            if search:
                if keytype == "Title":
                    books_info = search_book(title=keyword)
                elif keytype == "Category":
                    books_info = search_book(category=keyword)
                elif keytype == "Author":
                    books_info = search_book(author=keyword)
                elif keytype == "Publisher":
                    books_info = search_book(publisher=keyword)
                elif keytype == "Language":
                    books_info = search_book(language=keyword)
                elif keytype == "Extension":
                    books_info = search_book(extension=keyword)
                elif keytype == "NumberPage":
                    books_info = search_book(page=keyword)
                elif keytype == "PublishYear":
                    books_info = search_book(year=keyword)
                data = pd.DataFrame(books_info)
                data_changed = True
        elif selected == "Advanced Search":
            _, row1, _, row2, _ = st.columns((0.1, 1, 0.1, 1, 0.1))
            with row1:
                category = st.text_input("Category")
                title = st.text_input("Title")
                author = st.text_input("Author")
                publisher = st.text_input("Publisher")
            with row2:
                language = st.text_input("Language")
                extension = st.text_input("Extension")
                number_page = st.text_input("Number of pages")
                publish_year = st.text_input("Publish year")
            search = st.button("Search")
            if search:
                books_info = search_book(
                    category=category,
                    title=title,
                    author=author,
                    publisher=publisher,
                    year=publish_year,
                    page=number_page,
                    language=language,
                    extension=extension,
                )
                data = pd.DataFrame(books_info)
                data_changed = True
        elif selected == "Semantic Search":
            input = st.text_area("Describe the book you want to find")
            search = st.button("Search")
            if search:
                fields = extract_fields(input)
                print(fields)
                books_info = search_book(
                    category=fields.get("category", None),
                    title=fields.get("title", None),
                    author=fields.get("author", None),
                    publisher=fields.get("publisher", None),
                    year=fields.get("year", None),
                    page=fields.get("page", None),
                    language=fields.get("language", None),
                    extension=fields.get("extension", None),
                )
                data = pd.DataFrame(books_info)
                data_changed = True

        table = st.dataframe()
        small_column = st.column_config.TextColumn(width="small")
        medium_column = st.column_config.TextColumn(width="medium")
        large_column = st.column_config.TextColumn(width="large")

        if data_changed:
            table.dataframe(
                data,
                height=915,
                use_container_width=True,
                column_config={
                    "ID": small_column,
                    "Author": medium_column,
                    "Title": medium_column,
                    "Description": large_column,
                    "Publisher": medium_column,
                    "Publish Year": small_column,
                    "Number Pages": small_column,
                    "Language": small_column,
                },
            )
        else:
            table.dataframe(
                st.session_state["full_data"],
                height=915,
                use_container_width=True,
                column_config={
                    "ID": small_column,
                    "Author": medium_column,
                    "Title": medium_column,
                    "Description": large_column,
                    "Publisher": medium_column,
                    "Publish Year": small_column,
                    "Number Pages": small_column,
                    "Language": small_column,
                },
            )


if __name__ == "__main__":
    main()
