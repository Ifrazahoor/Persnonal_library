import streamlit as st
import json
import os

# File to store library data
LIBRARY_FILE = "library.json"

# Load library from file
def load_library():
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Set Streamlit page configuration
st.set_page_config(page_title="Personal Library Manager", page_icon="📚", layout="wide")

# Background image styling
background_image = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://www.freepik.com/free-photo/books-with-blue-background_1092452.htm#from_element=detail_alsolike');
    background-size: cover;
    background-position: center;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
</style>
"""
st.markdown(background_image, unsafe_allow_html=True)

# App Title
st.title("📚 Personal Library Manager")

# Load existing library
library = load_library()

# Sidebar Navigation
menu = st.sidebar.radio("📌 Select an Option", ["Add a Book", "Remove a Book", "Search a Book", "Display All Books", "Library Statistics"])

# Add a Book
if menu == "Add a Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Enter Book Title")
    author = st.text_input("Enter Author")
    year = st.number_input("Enter Publication Year", min_value=0, step=1)
    genre = st.text_input("Enter Genre")
    read_status = st.checkbox("Have you read this book?")

    if st.button("Add Book"):
        if title and author and year and genre:
            book = {
                "Title": title,
                "Author": author,
                "Year": int(year),
                "Genre": genre,
                "Read": read_status
            }
            library.append(book)
            save_library(library)
            st.success("✅ Book added successfully!")
        else:
            st.warning("⚠ Please fill all fields.")

# Remove a Book
elif menu == "Remove a Book":
    st.subheader("🗑 Remove a Book")
    book_titles = [book["Title"] for book in library]

    if book_titles:
        book_to_remove = st.selectbox("Select a book to remove", book_titles)
        if st.button("Remove Book"):
            library = [book for book in library if book["Title"] != book_to_remove]
            save_library(library)
            st.success("✅ Book removed successfully!")
    else:
        st.warning("⚠ No books available to remove.")

# Search a Book
elif menu == "Search a Book":
    st.subheader("🔍 Search for a Book")
    search_query = st.text_input("Enter book title or author")

    if search_query:
        results = [book for book in library if search_query.lower() in book["Title"].lower() or search_query.lower() in book["Author"].lower()]
        if results:
            st.write("📚 **Matching Books:**")
            for book in results:
                st.write(f"✔ **{book['Title']}** by *{book['Author']}* ({book['Year']}) - {book['Genre']} - {'✅ Read' if book['Read'] else '❌ Unread'}")
        else:
            st.warning("❌ No matching books found.")

# Display All Books
elif menu == "Display All Books":
    st.subheader("📖 Your Library")
    if library:
        st.write("Here are all the books in your collection:")
        st.table(library)
    else:
        st.warning("⚠ Your library is empty.")

# Library Statistics
elif menu == "Library Statistics":
    st.subheader("📊 Library Statistics")
    total_books = len(library)
    if total_books == 0:
        st.warning("⚠ No books in library.")
    else:
        read_books = sum(1 for book in library if book["Read"])
        percentage_read = (read_books / total_books) * 100
        st.write(f"📚 **Total Books:** {total_books}")
        st.write(f"✅ **Books Read:** {read_books} ({percentage_read:.1f}%)")

# Run Streamlit App
if __name__ == "__main__":
    st.markdown("---")
    st.write("📌 **Developed with ❤️ using Streamlit**")