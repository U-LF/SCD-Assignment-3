import tkinter as tk
from tkinter import messagebox
from book_library import Book, EBook, Library, BookNotAvailableError

# Step 1: Create main app window and library instance
library = Library()
root = tk.Tk()
root.title("Library Management System")
root.geometry("500x500")

# Step 2: Add book function
def add_book():
    title = title_entry.get()
    author = author_entry.get()
    isbn = isbn_entry.get()
    is_ebook = ebook_var.get()
    size = size_entry.get()

    if not title or not author or not isbn:
        messagebox.showerror("Error", "Title, Author, and ISBN are required.")
        return

    if is_ebook and not size:
        messagebox.showerror("Error", "Download size required for eBooks.")
        return

    if is_ebook:
        book = EBook(title, author, isbn, size)
    else:
        book = Book(title, author, isbn)

    library.add_book(book)
    messagebox.showinfo("Success", f"Book '{title}' added!")
    update_book_list()

# Step 3: Update book list display
def update_book_list():
    listbox.delete(0, tk.END)
    for book in library:
        listbox.insert(tk.END, str(book))

# Step 4: UI elements
tk.Label(root, text="Title:").pack()
title_entry = tk.Entry(root)
title_entry.pack()

tk.Label(root, text="Author:").pack()
author_entry = tk.Entry(root)
author_entry.pack()

tk.Label(root, text="ISBN:").pack()
isbn_entry = tk.Entry(root)
isbn_entry.pack()

# Checkbox to choose eBook
ebook_var = tk.BooleanVar()
tk.Checkbutton(root, text="eBook?", variable=ebook_var).pack()

tk.Label(root, text="Download Size (MB):").pack()
size_entry = tk.Entry(root)
size_entry.pack()

tk.Button(root, text="Add Book", command=add_book).pack(pady=5)

# Display list of available books
tk.Label(root, text="Available Books:").pack()
listbox = tk.Listbox(root, width=60)
listbox.pack(pady=10)

update_book_list()

root.mainloop()
