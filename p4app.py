import streamlit as st
import pandas as pd
import random

# File to store book data
FILE_NAME = "library.csv"

# Initialize the library file if it doesn't exist
def initialize_file():
    try:
        df = pd.read_csv(FILE_NAME)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Title", "Author", "Genre", "Description"])
        df.to_csv(FILE_NAME, index=False)

# Function to add a new book
def add_book(title, author, genre, description):
    df = pd.DataFrame([[title, author, genre, description]], 
                      columns=["Title", "Author", "Genre", "Description"])
    try:
        existing_data = pd.read_csv(FILE_NAME)
        df = pd.concat([existing_data, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_csv(FILE_NAME, index=False)

# Function to view all books
def view_books():
    try:
        df = pd.read_csv(FILE_NAME)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Title", "Author", "Genre", "Description"])

# Function to search for books by keyword
def search_books(keyword):
    df = view_books()
    return df[df.apply(lambda row: keyword.lower() in row.to_string().lower(), axis=1)]

# Function to recommend a book based on genre
def recommend_book(genre):
    df = view_books()
    recommendations = df[df["Genre"].str.contains(genre, case=False, na=False)]
    return recommendations.sample(1) if not recommendations.empty else None

# Streamlit UI
st.title("📚 Personal Library Manager with Recommendations")
initialize_file()

menu = ["Add Book", "View Books", "Search Book", "Get Recommendation"]
choice = st.sidebar.selectbox("Select an option", menu)

if choice == "Add Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre (e.g., Fiction, Science, Mystery)")
    description = st.text_area("Brief Description")
    
    if st.button("Add Book"):
        if title and author and genre and description:
            add_book(title, author, genre, description)
            st.success(f"✅ '{title}' by {author} added successfully!")
        else:
            st.warning("⚠ Please fill in all fields.")

elif choice == "View Books":
    st.subheader("📖 Your Library Collection")
    books = view_books()
    if not books.empty:
        st.dataframe(books)
    else:
        st.write("📂 No books in your library yet!")

elif choice == "Search Book":
    st.subheader("🔎 Search for a Book")
    keyword = st.text_input("Enter title, author, or keyword")
    if st.button("Search"):
        results = search_books(keyword)
        if not results.empty:
            st.dataframe(results)
        else:
            st.warning("🚫 No matching books found.")

elif choice == "Get Recommendation":
    st.subheader("🎯 Get a Book Recommendation")
    genre = st.text_input("Enter a genre (e.g., Fiction, Mystery, Science)")
    if st.button("Recommend"):
        recommendation = recommend_book(genre)
        if recommendation is not None:
            st.success(f"📖 Recommended: **{recommendation.iloc[0]['Title']}** by {recommendation.iloc[0]['Author']}")
            st.write(f"📌 **Description:** {recommendation.iloc[0]['Description']}")
        else:
            st.warning("⚠ No recommendations available for this genre.")

