from fastapi import FastAPI, status, HTTPException, Request, Response
from pydantic import BaseModel
# from fastapi.exceptions import HTTPException
from datetime import datetime, time


books = [
    {
        "id" : 1, 
        "title" : "The Alchemist", 
        "author" : "Paulo Coelho", 
        "publish_date" : "1988-01-01"
    },
    {
        "id" : 2, 
        "title" : "The God of Small Things", 
        "author" : "Arundhati Roy", 
        "publish_date" : "1997-04-04"
    },
    {
        "id" : 3, 
        "title" : "The White Tiger", 
        "author" : "Aravind Adiga", 
        "publish_date" : "2008-01-01"
    },
    {
        "id" : 4, 
        "title" : "The Palace of Illusions", 
        "author" : "Chitra Banerjee Divakaruni", 
        "publish_date" : "2008-02-12"
    },
]


app = FastAPI()


class Book(BaseModel):
    id: int
    title: str
    author: str
    publish_date: str



@app.get("/books")
def get_books():
    return books


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
def get_book(book_id: int):
    book = next((book for book in books if book["id"] == book_id), None)
    if book:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    

@app.post('/books', status_code=status.HTTP_201_CREATED)
def create_book(book: Book):
    books.append(book.dict())
    return book


@app.put('/books/{book_id}', status_code=status.HTTP_200_OK)
def update_book(book_id: int, book: Book):
    book_index = next((i for i, b in enumerate(books) if b["id"] == book_id), None)

    if book_index is not None:
        books[book_index] = book.dict()
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.delete('/books/{book_id}', status_code=status.HTTP_200_OK)
def delete_book(book_id: int):
    global books
    for book in books:
        if book["id"] == book_id:
            # books.remove(book) 
            print(books[books.index(book)])
            del books[books.index(book)]
            break
    return {"detail": "Book deleted"}