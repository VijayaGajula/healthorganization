from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Required for flash messages

# --- MongoDB Configuration ---
# Replace with your actual MongoDB URI
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["HealthTips"]  # Replace with your DB name
contacts_collection = db["contacts"]  # Collection for contact messages
users_collection = db["users"]       # Optional: Collection for login users

@app.route("/")
def home():
    return render_template("index.html")

# Contact form handling
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("contactName")
    email = request.form.get("contactEmail")
    message = request.form.get("contactMsg")

    # Save contact to MongoDB
    contact_data = {
        "name": name,
        "email": email,
        "message": message
    }
    contacts_collection.insert_one(contact_data)

    flash(f"Thanks {name}, your message has been sent successfully!")
    return redirect(url_for("home"))

# Login handling (simple version - hardcoded)
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("loginUser")
    password = request.form.get("loginPass")

    # Save login attempt to MongoDB (like contact form)
    login_data = {
        "username": username,
        "password": password
    }
    users_collection.insert_one(login_data)

    flash(f"Login info saved for user: {username}")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
