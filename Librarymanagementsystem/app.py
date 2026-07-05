from flask import Flask, render_template, request, redirect
from models import db, Book, Member

app = Flask(__name__)
print("MY APP IS RUNNING")

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            return redirect("/dashboard")

        return "Invalid Username or Password"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    total_books = Book.query.count()
    total_members = Member.query.count()

    return render_template(
        "dashboard.html",
        total_books=total_books,
        total_members=total_members,
        issued_books=0
    )


# ---------------- BOOKS ----------------

@app.route("/books")
def books():

    search = request.args.get("search")

    if search:
        books = Book.query.filter(Book.title.contains(search)).all()
    else:
        books = Book.query.all()

    return render_template("books.html", books=books)


# ---------------- ADD BOOK ----------------

@app.route("/add-book", methods=["GET", "POST"])
def add_book():

    if request.method == "POST":

        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            quantity=int(request.form["quantity"])
        )

        db.session.add(new_book)
        db.session.commit()

        return redirect("/books")

    return render_template("add_book.html")


# ---------------- EDIT BOOK ----------------

@app.route("/edit-book/<int:id>", methods=["GET", "POST"])
def edit_book(id):

    book = Book.query.get_or_404(id)

    if request.method == "POST":

        book.title = request.form["title"]
        book.author = request.form["author"]
        book.quantity = int(request.form["quantity"])

        db.session.commit()

        return redirect("/books")

    return render_template("edit_book.html", book=book)


# ---------------- DELETE BOOK ----------------

@app.route("/delete-book/<int:id>")
def delete_book(id):

    book = Book.query.get_or_404(id)

    db.session.delete(book)
    db.session.commit()

    return redirect("/books")


# ---------------- MEMBERS ----------------

@app.route("/members")
def members():

    members = Member.query.all()

    return render_template("members.html", members=members)


# ---------------- ADD MEMBER ----------------

@app.route("/add-member", methods=["GET", "POST"])
def add_member():

    if request.method == "POST":

        member = Member(
            name=request.form["name"],
            email=request.form["email"],
            phone=request.form["phone"]
        )

        db.session.add(member)
        db.session.commit()

        return redirect("/members")

    return render_template("add_member.html")


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)