import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from book_library import Book, EBook, Library, BookNotAvailableError

library = Library()
root = tk.Tk()
root.title("Library Management System")
root.geometry("700x550")

style = ttk.Style()
style.theme_use("vista")

PAD_X, PAD_Y = 10, 6

# ================= UI Handlers =================

def toggle_ebook_size_field():
    if ebook_var.get():
        size_entry.config(state="normal")
    else:
        size_entry.delete(0, tk.END)
        size_entry.config(state="disabled")

def add_book():
    title = title_entry.get()
    author = author_entry.get()
    isbn = isbn_entry.get()
    is_ebook = ebook_var.get()
    size = size_entry.get()

    if not title or not author or not isbn:
        messagebox.showerror("Error", "Title, Author, and ISBN are required.")
        return

    if is_ebook:
        if not size:
            messagebox.showerror("Error", "Download size required for eBooks.")
            return
        if not size.isdigit():
            messagebox.showerror("Error", "Download size must be a number.")
            return
        book = EBook(title, author, isbn, size)
    else:
        book = Book(title, author, isbn)

    library.add_book(book)
    messagebox.showinfo("Success", f"Book '{title}' added.")
    update_book_list()
    clear_inputs()

def lend_book():
    isbn = simpledialog.askstring("Lend Book", "Enter ISBN to lend:")
    if isbn:
        try:
            library.lend_book(isbn)
            messagebox.showinfo("Success", "Book lent successfully.")
            update_book_list()
        except BookNotAvailableError as e:
            messagebox.showerror("Error", str(e))

def return_book():
    isbn = simpledialog.askstring("Return Book", "Enter ISBN to return:")
    if isbn:
        try:
            library.return_book(isbn)
            messagebox.showinfo("Success", "Book returned successfully.")
            update_book_list()
        except BookNotAvailableError as e:
            messagebox.showerror("Error", str(e))

def remove_book():
    isbn = simpledialog.askstring("Remove Book", "Enter ISBN to remove:")
    if isbn:
        library.remove_book(isbn)
        messagebox.showinfo("Success", "Book removed.")
        update_book_list()

def view_books_by_author():
    author = simpledialog.askstring("Search by Author", "Enter author's name:")
    if author:
        books = list(library.books_by_author(author))
        if books:
            available_listbox.delete(0, tk.END)
            lent_listbox.delete(0, tk.END)
            available_listbox.insert(tk.END, f"Books by {author}:")
            for book in books:
                if book.is_lent:
                    lent_listbox.insert(tk.END, str(book))
                else:
                    available_listbox.insert(tk.END, str(book))
        else:
            messagebox.showinfo("Not Found", "No books found by this author.")

def update_book_list():
    available_listbox.delete(0, tk.END)
    lent_listbox.delete(0, tk.END)

    for book in library.books:
        if not book.is_lent:
            available_listbox.insert(tk.END, str(book))
        else:
            lent_listbox.insert(tk.END, str(book))

def clear_inputs():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    isbn_entry.delete(0, tk.END)
    ebook_var.set(False)
    toggle_ebook_size_field()

# ================= UI Layout =================

frame = ttk.Frame(root, padding=15)
frame.pack(fill="x")

# Title
ttk.Label(frame, text="Title").grid(row=0, column=0, sticky="e", padx=PAD_X, pady=PAD_Y)
title_entry = ttk.Entry(frame)
title_entry.grid(row=0, column=1, pady=PAD_Y, sticky="we")

# Author
ttk.Label(frame, text="Author").grid(row=1, column=0, sticky="e", padx=PAD_X, pady=PAD_Y)
author_entry = ttk.Entry(frame)
author_entry.grid(row=1, column=1, pady=PAD_Y, sticky="we")

# ISBN
ttk.Label(frame, text="ISBN").grid(row=2, column=0, sticky="e", padx=PAD_X, pady=PAD_Y)
isbn_entry = ttk.Entry(frame)
isbn_entry.grid(row=2, column=1, pady=PAD_Y, sticky="we")

# eBook checkbox
ebook_var = tk.BooleanVar()
ebook_check = ttk.Checkbutton(frame, text="Is this an eBook?", variable=ebook_var, command=toggle_ebook_size_field)
ebook_check.grid(row=3, column=0, columnspan=2, pady=PAD_Y)

# eBook size
ttk.Label(frame, text="Download Size (MB)").grid(row=4, column=0, sticky="e", padx=PAD_X, pady=PAD_Y)
size_entry = ttk.Entry(frame, state="disabled")
size_entry.grid(row=4, column=1, pady=PAD_Y, sticky="we")

# Buttons
button_frame = ttk.Frame(frame)
button_frame.grid(row=5, column=0, columnspan=2, pady=PAD_Y)

ttk.Button(button_frame, text="Add Book", command=add_book).grid(row=0, column=0, padx=5)
ttk.Button(button_frame, text="Lend Book", command=lend_book).grid(row=0, column=1, padx=5)
ttk.Button(button_frame, text="Return Book", command=return_book).grid(row=0, column=2, padx=5)
ttk.Button(button_frame, text="Remove Book", command=remove_book).grid(row=0, column=3, padx=5)
ttk.Button(button_frame, text="Search by Author", command=view_books_by_author).grid(row=0, column=4, padx=5)

# ========== Notebook Tabs ==========
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# Available Books Tab
available_tab = ttk.Frame(notebook)
notebook.add(available_tab, text="Available Books")

available_listbox = tk.Listbox(available_tab, height=10, font=("Segoe UI", 10))
available_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)

available_scroll = ttk.Scrollbar(available_tab, orient="vertical", command=available_listbox.yview)
available_scroll.pack(side="right", fill="y")
available_listbox.config(yscrollcommand=available_scroll.set)

# Lent Books Tab
lent_tab = ttk.Frame(notebook)
notebook.add(lent_tab, text="Lent Books")

lent_listbox = tk.Listbox(lent_tab, height=10, font=("Segoe UI", 10), fg="gray")
lent_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)

lent_scroll = ttk.Scrollbar(lent_tab, orient="vertical", command=lent_listbox.yview)
lent_scroll.pack(side="right", fill="y")
lent_listbox.config(yscrollcommand=lent_scroll.set)

# Resize config
frame.columnconfigure(1, weight=1)

update_book_list()
root.mainloop()