from fastapi import FastAPI,Body

Books = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

app = FastAPI()

#GET -> READ
@app.get('/all_books')
async def all_books():
    return Books

#Path Parameter
@app.get('/book/{book_title}')
async def book_by_title(book_title):
    for book in Books:
        if book['title'].lower() == book_title.lower():
            return book

#Query Parameter        
@app.get('/books/')
async def book_by_category(category):
    for book in Books:
        if book['category'].lower() == category.lower():
            return book
        
#Path and #Query Parameter
@app.get('/books/title/{title}/')
async def books_by_both(title,author):
    for i in range(len(Books)):
        if Books[i]['title'].lower() == title.lower() and \
        Books[i]['author'].lower() == author.lower():
            return Books[i]
        
#POST -> CREATE
@app.post('/post')
async def post(new_book = Body()):
    Books.append(new_book)

#PUT -> UPDATE
@app.put('/put')
async def update(upd_book = Body()):
    for i in range(len(Books)):
        if Books[i]['title'].lower == upd_book['title'].lower():
            Books[i] = upd_book
            break

#DELETE -> DELETE
@app.delete('/delete/{title_del}')
async def delete(title_del):
    for i in range(len(Books)):
        if Books[i]['title'].lower() == title_del.lower():
            Books.pop(i)
            break