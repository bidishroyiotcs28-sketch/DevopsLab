from flask import Flask, redirect, url_for, render_template, request,session,flash
from datetime import timedelta
#from flask_sqlalchemy import SQLAlchemy
#import webbrowser

#webbrowser.open("http://127.0.0.1:5000", new = 1)

app = Flask("__main__")
app.secret_key = "bidish"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days = 5)


#db = SQLAlchemy(app)

# class users(db.Model):
#     _id = db.Column("id",db.Integer, primary_key=True)
#     name = db.Column("name",db.String(100))
#     roll = db.Column("roll",db.String(100))
#     email = db.Column("email",db.String(100))

#     def __init__(self,name, email):
#         self.name = name
#         self.email = email

@app.route('/')
def home():
    return render_template("index.html")

#@app.route("/home")
#def user():
#    return f"Hello home"

@app.route("/admin")
def admin(): 
    return redirect(url_for("home", name = "Admin!"))

@app.route("/user", methods = ["POST","GET"])
def user1():
    #return render_template("user.html", details = usr)
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("Email entered successfully")
        else:
            if "email" in session:
                email = session["email"]
        roll = session["roll"]
        #return f"<h1>{user}\n{roll}</h1>"
        return render_template("user.html", user = user, roll = roll, email = email)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))

@app.route("/login", methods = ["POST","GET"])
def login():
    if request.method == "POST":
        #session.permanent = True
        user = request.form["nm"]
        roll = request.form["roll"]
        session["user"] = user
        session["roll"] = roll
        flash("Login Successful")
        return redirect(url_for("user1"))
    else:
        if "user" in session:
            flash("You are already logged in!")
            return redirect(url_for("user1"))
        else:
            return render_template("login.html")
    
@app.route("/logout")
def logout():
    flash(f"Logged out succesfully","info")
    session.pop("user", None)
    session.pop("email",None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    #db.create_all()
    app.run(host = '0.0.0.0', port = 5000, debug=True)