from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId  # To handle MongoDB ObjectIds
import os

# Flask application
app = Flask(__name__)
app.secret_key = "secret_key"  # Required for flash messages

# MongoDB connection configuration
#MONGO_URI = "mongodb://localhost:27017/"
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["BOOKSTORE"]  # Database name
collection = db["books"]  # Collection name


# Home page to list all books
@app.route("/", methods=["GET"])
@app.route("/books", methods=["GET"])
def get_books():
    active_books = list(collection.find({"$or": [{"deleted": False}, {"deleted": {"$exists": False}}]}))
    marked_books = list(collection.find({"deleted": True}))

    for book in active_books + marked_books:
        book["_id"] = str(book["_id"])  # Convert ObjectId to string for rendering

    return render_template("index.html", active_books=active_books, marked_books=marked_books)


# Form to add a new book
@app.route("/books/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        data = {}
        title = request.form.get("title")
        if title:
            data["title"] = title
        for field in ["isbn", "year", "price", "page", "category", "author_first", "author_last", "publisher_name"]:
            value = request.form.get(field)
            if value:
                if field in ["year", "price", "page"]:
                    data[field] = int(value) if value.isdigit() else float(value)
                else:
                    data[field] = value
        if "author_first" in data or "author_last" in data:
            data["author"] = {
                "firstName": data.pop("author_first", None),
                "lastName": data.pop("author_last", None)
            }
        if "publisher_name" in data:
            data["publisher"] = {"name": data.pop("publisher_name", None)}
        data["deleted"] = False
        collection.insert_one(data)
        return redirect(url_for("get_books"))
    return render_template("form.html")


# Search for books
@app.route("/books/search", methods=["POST"])
def search_books():
    search_by = request.form.get("search_by")
    query = request.form.get("query")

    search_filter = {}
    if search_by == "isbn":
        search_filter = {"isbn": query}
    elif search_by == "title":
        search_filter = {"title": {"$regex": query, "$options": "i"}}
    elif search_by == "author":
        search_filter = {
            "$or": [
                {"author.firstName": {"$regex": query, "$options": "i"}},
                {"author.lastName": {"$regex": query, "$options": "i"}}
            ]
        }

    books = list(collection.find(search_filter))
    for book in books:
        book["_id"] = str(book["_id"])
    return render_template("search_results.html", books=books)


# Book details
@app.route("/books/<string:id>", methods=["GET"])
def book_details(id):
    book = collection.find_one({"_id": ObjectId(id)})
    if book:
        book["_id"] = str(book["_id"])
        return render_template("book_details.html", book=book)
    else:
        flash("Book not found!", "error")
        return redirect(url_for("get_books"))


# Update book details
@app.route("/books/update/<string:id>", methods=["GET", "POST"])
def update_book(id):
    if request.method == "POST":
        updated_data = {
            "title": request.form.get("title"),
            "isbn": request.form.get("isbn"),
            "year": int(request.form.get("year")) if request.form.get("year") else None,
            "price": float(request.form.get("price")) if request.form.get("price") else None,
            "page": int(request.form.get("page")) if request.form.get("page") else None,
            "category": request.form.get("category"),
            "author": {
                "firstName": request.form.get("author_first"),
                "lastName": request.form.get("author_last")
            },
            "publisher": {
                "name": request.form.get("publisher_name")
            }
        }
        updated_data = {k: v for k, v in updated_data.items() if v is not None}
        collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
        flash("Book updated successfully!", "success")
        return redirect(url_for("book_details", id=id))

    book = collection.find_one({"_id": ObjectId(id)})
    if book:
        book["_id"] = str(book["_id"])
        return render_template("update_book.html", book=book)
    else:
        flash("Book not found!", "error")
        return redirect(url_for("get_books"))


# Mark a book as deleted
@app.route("/books/delete/<string:id>", methods=["POST"])
def delete_book(id):
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": {"deleted": True}})
    if result.matched_count > 0:
        flash("Book marked as deleted.", "success")
    else:
        flash("Book not found!", "error")
    return redirect(url_for("get_books"))


# Restore deleted book
@app.route("/books/restore/<string:id>", methods=["POST"])
def restore_book(id):
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": {"deleted": False}})
    if result.matched_count > 0:
        flash("Book restored successfully!", "success")
    else:
        flash("Book not found!", "error")
    return redirect(url_for("get_books"))


# Permanently delete a book
@app.route("/books/permanent_delete/<string:id>", methods=["POST"])
def permanent_delete_book(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        flash("Book permanently deleted.", "success")
    else:
        flash("Book not found!", "error")
    return redirect(url_for("get_books"))


# Run the Flask application
if __name__ == "__main__":
    app.run(port=5000, debug=True)
