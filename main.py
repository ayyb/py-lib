from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db' # 데이터베이스 이름
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

all_books = []


##CREATE TABLE 테이블 만들기
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'


db.create_all()

@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", all_books=all_books)


@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        all_books.append(request.form.to_dict()) # obj 형태로 변환
        # CREATE RECORD
        new_book = Book(title=request.form.to_dict()["title"], author=request.form.to_dict()["author"], rating=request.form.to_dict()["rating"])  # 기본키 필드는 선택사항
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home')) # hoem으로 redirect


    return render_template("add.html")

@app.route("/edit/<int:book_id>", methods=["GET","POST"])
def edit(book_id):
    book = Book.query.filter_by(id=book_id).first()
    print(book)
    if request.method == "POST":
        new_rating = request.form.to_dict()["new_rating"]
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = new_rating
        db.session.commit()
        return redirect(url_for('home')) # hoem으로 redirect


    return render_template("edit.html",book=book)

@app.route("/delete/<int:book_id>")
def delete(book_id):
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))  # hoem으로 redirect


if __name__ == "__main__":
    app.run(debug=True)

