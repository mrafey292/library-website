from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy, session

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Bootstrap(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
 
    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'

# class BookForm(FlaskForm):
#     name = StringField("Book name", validators=[DataRequired()])
#     author = StringField("Book author", validators=[DataRequired()])
#     rating = StringField("Rating", validators=[DataRequired()])
#     submit = SubmitField("Submit")


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", data=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(title=request.form["name"], author=request.form["author"], rating=request.form["rating"],)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    book_to_update = Book.query.get(id)
    if request.method == "POST":
        book_to_update.rating = request.form["rating"]
        all_books = db.session.query(Book).all()
        return render_template("index.html", data=all_books)
    return render_template("edit.html", book_to_update=book_to_update)


@app.route("/delete/<id>")
def delete(id):
    book_to_delete = Book.query.get(id)
    db.session.delete(book_to_delete)
    db.session.commit()
    all_books = db.session.query(Book).all()
    return render_template("index.html", data=all_books)


if __name__ == "__main__":
    app.run(debug=True)

