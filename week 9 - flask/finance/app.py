import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from datetime import datetime

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    portfolio = db.execute("SELECT * FROM portfolio WHERE id = ?", session["user_id"])

    total_price = 0
    for i in range(len(portfolio)):
        price = lookup(portfolio[i]["symbol"])["price"]

        portfolio[i]["price"] = usd(price)
        portfolio[i]["total"] = usd(price * portfolio[i]["shares"])

        total_price += price * portfolio[i]["shares"]

    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    return render_template("index.html", portfolio = portfolio, cash = usd(user[0]["cash"]), total = usd(total_price + user[0]["cash"]))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)
        if not request.form.get("shares"):
            return apology("must provide shares", 403)
        if not request.form.get("shares").isdigit():
            return apology("You cannot purchase partial shares.", 400)

        look = lookup(request.form.get("symbol"))
        if not look:
            return apology("invalid symbol", 400)

        shares = int(request.form.get("shares"))
        price = look["price"]

        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        if user[0]["cash"] - price * shares < 0:
            return apology("can't afford", 400)

        # check exist symbol in portfolio
        portfolio = db.execute("SELECT * FROM portfolio WHERE id = ? AND symbol = ?", session["user_id"], request.form.get("symbol"))
        if len(portfolio) == 1:
            # update
            db.execute("UPDATE portfolio SET shares = ? WHERE id = ?", portfolio[0]["shares"] + shares, session["user_id"])
        else:
            # insert new
            db.execute("INSERT INTO portfolio(id, symbol, shares) VALUES(?, ?, ?)", session["user_id"], request.form.get("symbol"), shares)

        # update cash of user
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user[0]["cash"] - price * shares, user[0]["id"])
        # insert transactions
        db.execute("INSERT INTO transactions(id, symbol, shares, type, transacted) VALUES(?,?,?,?,?)", session["user_id"], request.form.get("symbol"), shares, "buy", datetime.now())

        return redirect("/")
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    portfolio = db.execute("SELECT * FROM transactions WHERE id = ?", session["user_id"])
    # for i in portfolio:
        # portfolio[i]["price"] =
    return render_template("history.html", portfolio = portfolio)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        if not lookup(request.form.get("symbol")):
            return apology("invalid symbol", 400)
        else:
            quote=lookup(request.form.get("symbol"))
            quote["price"] = usd(quote["price"])
            return render_template("quoted.html", quote= quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("must provide password and confirmation same value", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username not exists and password is correct
        if len(rows) == 1 :
            return apology("username is exit", 400)

        _ = db.execute("INSERT INTO users(username, hash) VALUES(?, ?)",
                              request.form.get("username"),
                              generate_password_hash(request.form.get("password")))

        new_user = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = new_user[0]["id"]
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")




@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide sumbol", 403)
        elif not request.form.get("shares"):
            return apology("must provide shares", 403)

        shares = int(request.form.get("shares"))

        portfolio = db.execute("SELECT * FROM portfolio WHERE id = ? AND symbol = ?", session["user_id"], request.form.get("symbol"))
        if portfolio[0]["shares"] < shares:
            return apology("can't afford", 400)

        look = lookup(request.form.get("symbol"))
        if portfolio == shares:
            # remove portfolio
            db.execute("DELETE FROM portfolio WHERE id = ? AND symbol = ?", session["user_id"], request.form.get("symbol"))
        else:
            # remove shares portfolio
            db.execute("UPDATE portfolio SET shares = ? WHERE id = ? AND symbol = ?", portfolio[0]["shares"] - shares, session["user_id"], request.form.get("symbol"))

        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        # update user
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user[0]["cash"] + look["price"] * shares, session["user_id"])
        # insert transactions
        db.execute("INSERT INTO transactions(id, symbol, shares, type, transacted) VALUES(?,?,?,?,?)", session["user_id"],request.form.get("symbol"), shares, "sell", datetime.now())

        return redirect("/")
    else:
        portfolio = db.execute("SELECT * FROM portfolio WHERE id = ?", session["user_id"])
        return render_template("sell.html", portfolio = portfolio)
