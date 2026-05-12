import json
from datetime import datetime

class BaseClass:
    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        data = self.__dict__
        with open(self.filename(), 'w') as f:
            json.dump(data, f, default=str, indent=2)
    def touch(self):
        self.updated_at = datetime.now()
        self.save()


class Book(BaseClass):
    def __init__(self, title, author, year, genre):
        super().__init__()
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.available = True
        self.save()

    def filename(self):
        return f"{self.title.replace(' ', '_')}.json"    

class User(BaseClass):
    def __init__(self, name, id):
        super().__init__()
        self.name = name
        self.id = id
        self.save()

    def filename(self):
        return f"{self.name.replace(' ', '_')}_{self.id}.json"    

    def borrow_book(self, book):
        if book.available:
            book.available = False
            book.touch()
        else:
            print(f"'{book.title}' is already borrowed")

Book1 = Book("The lord of the rings", "J.R.R. Tolkien", 1954, "Fantasy")
alice = User("Alice", 1)
alice.borrow_book(Book1)
print(Book1.available)

