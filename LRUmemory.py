"""
solution to Q1 by Seulgee Jang

"""
from functools import wraps
from collections import OrderedDict

# "object containing title, author, and language of a book"
class Book:
    def __init__(self, title, author, language):
        self.title = title
        self.author = author
        self.language = language
        


#lru_cache using ordereddict
class RecentMemory:
    # "N can be a large number"
    def __init__(self, size: int):
        self.memory = OrderedDict()
        self.size = size
    #take isbn and return book obj
    def get(self, isbn: str) -> Book:
        if isbn not in self.memory:
            return -1
        else:
            self.memory.move_to_end(isbn)
            return self.memory[isbn]
    def put(self, isbn: str, obj: Book)-> None:
        self.memory[isbn] = obj
        self.memory.move_to_end(isbn)
        if len(self.memory) > self.size:
            self.memory.popitem(last = False)



#RecentMemoryDecorator
def RMDecorator(size):
    recentMemory = RecentMemory(size)
    
    #temporary recent memory for testing purposes
    if size == 4:
        isbns = ["isbn0","isbn1","isbn2","isbn3"]
        titles = ["BadBlood", "SayNothing", "WilfulBlindness", "Caste"]
        authors = ["JohnCarreyrou", "PatrickRaddenKeefe","SamCooper","IsabelWilkerson"]
        languages=["Eng","Eng","Eng","Eng"]
        for i in range(size):
            bookEntry = Book(titles[i],authors[i],languages[i])
            recentMemory.put(isbns[i],bookEntry)
    
    #the func in this case: get_book_info(isbn)
    print(recentMemory.memory)

    def Decorator(func):
        @wraps(func)
        def Wrapper(isbn):
            #before calling get_book_info(isbn), search recentmemory first
            bookobj = recentMemory.get(isbn)
            #if not in quickmemory, grab from db, and add to quickmemory
            if bookobj == -1:                
                bookobj = func(isbn)
                recentMemory.put(isbn,bookobj)
                print("not in memory")
                print(recentMemory.memory)
                return bookobj
            else:
                print("is in memory")
                print(recentMemory.memory)
            return bookobj   
        return Wrapper
    return Decorator
    
#assume get_book_info(isbn) retrieves a book obj from db instead of user input
#size N of recentmemory for quick lookup is 3 in this testcase
@RMDecorator(size = 4)
def get_book_info(isbn):
    newBookTitle = input("Enter title of the book: ")
    newBookAuthor = input("Enter author of the book: ")
    newBookLanguage = input("Enter language of the book: ")
    
    newBook = Book(newBookTitle,newBookAuthor,newBookLanguage)
    return newBook

