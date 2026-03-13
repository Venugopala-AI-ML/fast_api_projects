from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from database import get_db, engine
from sqlalchemy.orm import Session
import model
from pydantic import BaseModel


app = FastAPI()

class BooksStore(BaseModel):
    id: int
    title: str
    author: str 
    publish_date: str

@app.post('/books', status_code=status.HTTP_201_CREATED)
def create_book(books: BooksStore, db: Session = Depends(get_db)):
    try: 
        new_book = model.Book(**books.dict())
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating book")


@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    return db.query(model.Book).all()


@app.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(model.Book).filter(model.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@app.delete('/books/{book_id}')
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(model.Book).filter(model.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}


@app.get("/")
def read_root(books: BooksStore, db: Session = Depends(get_db)):
    return {"Hello": "World"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
