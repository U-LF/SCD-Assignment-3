from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QCheckBox, QPushButton, QMessageBox, QTabWidget,
    QListWidget, QInputDialog, QGroupBox
)
from PyQt5.QtCore import Qt
from book_library import Book, EBook, Library, BookNotAvailableError
import sys

class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.library = Library()
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 700, 550)

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        self.layout = QVBoxLayout()
        main_widget.setLayout(self.layout)

        self.form_group = QGroupBox("Add Book")
        self.form_layout = QFormLayout()
        self.form_group.setLayout(self.form_layout)

        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.isbn_input = QLineEdit()
        self.ebook_check = QCheckBox("Is this an eBook?")
        self.ebook_check.stateChanged.connect(self.toggle_size_field)
        self.size_input = QLineEdit()
        self.size_input.setDisabled(True)

        self.form_layout.addRow("Title:", self.title_input)
        self.form_layout.addRow("Author:", self.author_input)
        self.form_layout.addRow("ISBN:", self.isbn_input)
        self.form_layout.addRow(self.ebook_check)
        self.form_layout.addRow("Download Size (MB):", self.size_input)

        self.layout.addWidget(self.form_group)

        # Buttons row
        self.button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Book")
        self.lend_btn = QPushButton("Lend Book")
        self.return_btn = QPushButton("Return Book")
        self.remove_btn = QPushButton("Remove Book")
        self.search_btn = QPushButton("Search by Author")

        self.add_btn.clicked.connect(self.add_book)
        self.lend_btn.clicked.connect(self.lend_book)
        self.return_btn.clicked.connect(self.return_book)
        self.remove_btn.clicked.connect(self.remove_book)
        self.search_btn.clicked.connect(self.view_books_by_author)

        for btn in [self.add_btn, self.lend_btn, self.return_btn, self.remove_btn, self.search_btn]:
            self.button_layout.addWidget(btn)

        self.layout.addLayout(self.button_layout)

        # Tabs
        self.tabs = QTabWidget()
        self.available_list = QListWidget()
        self.lent_list = QListWidget()
        self.tabs.addTab(self.available_list, "Available Books")
        self.tabs.addTab(self.lent_list, "Lent Books")
        self.layout.addWidget(self.tabs)

        self.update_book_list()

    def toggle_size_field(self):
        self.size_input.setDisabled(not self.ebook_check.isChecked())
        if not self.ebook_check.isChecked():
            self.size_input.clear()

    def clear_inputs(self):
        self.title_input.clear()
        self.author_input.clear()
        self.isbn_input.clear()
        self.ebook_check.setChecked(False)
        self.size_input.clear()

    def update_book_list(self):
        self.available_list.clear()
        self.lent_list.clear()
        for book in self.library.books:
            if book.is_lent:
                self.lent_list.addItem(str(book))
            else:
                self.available_list.addItem(str(book))

    def add_book(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        isbn = self.isbn_input.text().strip()
        is_ebook = self.ebook_check.isChecked()
        size = self.size_input.text().strip()

        if not title or not author or not isbn:
            QMessageBox.warning(self, "Error", "Title, Author, and ISBN are required.")
            return

        if is_ebook:
            if not size:
                QMessageBox.warning(self, "Error", "Download size required for eBooks.")
                return
            if not size.isdigit():
                QMessageBox.warning(self, "Error", "Download size must be a number.")
                return
            book = EBook(title, author, isbn, size)
        else:
            book = Book(title, author, isbn)

        self.library.add_book(book)
        QMessageBox.information(self, "Success", f"Book '{title}' added.")
        self.update_book_list()
        self.clear_inputs()

    def lend_book(self):
        isbn, ok = QInputDialog.getText(self, "Lend Book", "Enter ISBN to lend:")
        if ok and isbn:
            try:
                self.library.lend_book(isbn.strip())
                QMessageBox.information(self, "Success", "Book lent successfully.")
                self.update_book_list()
            except BookNotAvailableError as e:
                QMessageBox.warning(self, "Error", str(e))

    def return_book(self):
        isbn, ok = QInputDialog.getText(self, "Return Book", "Enter ISBN to return:")
        if ok and isbn:
            try:
                self.library.return_book(isbn.strip())
                QMessageBox.information(self, "Success", "Book returned successfully.")
                self.update_book_list()
            except BookNotAvailableError as e:
                QMessageBox.warning(self, "Error", str(e))

    def remove_book(self):
        isbn, ok = QInputDialog.getText(self, "Remove Book", "Enter ISBN to remove:")
        if ok and isbn:
            self.library.remove_book(isbn.strip())
            QMessageBox.information(self, "Success", "Book removed.")
            self.update_book_list()

    def view_books_by_author(self):
        author, ok = QInputDialog.getText(self, "Search by Author", "Enter author's name:")
        if ok and author:
            books = list(self.library.books_by_author(author.strip()))
            self.available_list.clear()
            self.lent_list.clear()

            if books:
                self.available_list.addItem(f"Books by {author}:")
                for book in books:
                    if book.is_lent:
                        self.lent_list.addItem(str(book))
                    else:
                        self.available_list.addItem(str(book))
            else:
                QMessageBox.information(self, "Not Found", "No books found by this author.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())
