import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLite3 connection
conn = sqlite3.connect("finance.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
db = conn.cursor()

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def portfolio():
    user_id = session["user_id"]
    db.execute("""
        SELECT symbol, SUM(shares) AS total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
    """, (user_id,))
    rows = db.fetchall()

    portfolio = []
    for row in rows:
        symbol = row["symbol"]
        shares = row["total_shares"]
        quote = lookup(symbol)
        if quote:
            price = quote["price"]
            total_value = shares * price
            portfolio.append({
                "symbol": symbol,
                "shares": shares,
                "price": usd(price),
                "total_value": usd(total_value)
            })

    total_portfolio_value = sum(float(stock["total_value"].replace('$', '').replace(',', '')) for stock in portfolio)
    db.execute("SELECT cash FROM users WHERE id = ?", (user_id,))
    cash = db.fetchone()["cash"]
    return render_template("portfolio.html", portfolio=portfolio, total=usd(total_portfolio_value), cash=usd(cash))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("enter symbol", 400)
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("shares must be positive integer", 400)

        result = lookup(symbol)
        if result is None:
            return apology("invalid symbol!", 400)

        price = result["price"]
        shares = int(shares)
        total_cost = price * shares
        user_id = session["user_id"]
        symbol = result["symbol"]

        db.execute("SELECT cash FROM users WHERE id = ?", (user_id,))
        user_cash = db.fetchone()["cash"]

        if user_cash < total_cost:
            return apology("insufficient funds", 400)

        db.execute(
            "INSERT INTO transactions (price, shares, amount_paid, user_id, symbol) VALUES (?, ?, ?, ?, ?)",
            (price, shares, total_cost, user_id, symbol)
        )
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", (user_cash - total_cost, user_id)
        )
        conn.commit()
        return redirect("/")

@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    db.execute("""
        SELECT symbol, shares, price, date
        FROM transactions
        WHERE user_id = ?
        ORDER BY date ASC
    """, (user_id,))
    rows = db.fetchall()

    transactions = []
    for row in rows:
        transactions.append({
            "symbol": row["symbol"],
            "shares": row["shares"],
            "price": usd(row["price"]),
            "date": row["date"]
        })

    return render_template("history.html", transactions=transactions)

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("must provide username", 400)
        if not password:
            return apology("must provide password", 400)

        db.execute("SELECT * FROM users WHERE username = ?", (username,))
        rows = db.fetchall()

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 400)

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")
    if request.method == "POST":
        symbol = request.form.get("symbol")
        result = lookup(symbol)
        if result is None:
            return apology("invalid symbol!", 400)
        result["price"] = usd(result["price"])
        return render_template("quoted.html", quote=result)

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)
        if not password or not confirmation:
            return apology("must provide and confirm password", 400)
        if password != confirmation:
            return apology("Passwords do not match", 400)

        hash_pw = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_pw))
            conn.commit()
        except sqlite3.IntegrityError:
            return apology("Username already exists", 400)
        return redirect("/")
    return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    user_id = session["user_id"]
    db.execute("""
        SELECT symbol, SUM(shares) AS total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
    """, (user_id,))
    rows = db.fetchall()

    portfolio = []
    for row in rows:
        symbol = row["symbol"]
        shares = row["total_shares"]
        quote = lookup(symbol)
        if quote:
            price = quote["price"]
            portfolio.append({
                "symbol": symbol,
                "shares": shares,
                "price": usd(price)
            })

    if request.method == "GET":
        return render_template("sell.html", portfolio=portfolio)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol or not shares:
            return apology("must select symbol and quantity", 400)
        try:
            shares = int(shares)
        except ValueError:
            return apology("Shares must be a valid number", 400)
        if shares < 0:
            return apology("must choose a positive number", 400)

        db.execute("""
            SELECT SUM(shares) AS total_shares
            FROM transactions
            WHERE user_id = ? AND symbol = ?
        """, (user_id, symbol))
        owned = db.fetchone()["total_shares"]
        if owned < shares:
            return apology("request to sell more shares than owned")

        quote = lookup(symbol)
        if not quote:
            return apology("Invalid stock symbol", 400)

        price = quote["price"]
        total_value = price * shares

        db.execute(
            "INSERT INTO transactions (price, shares, amount_paid, user_id, symbol) VALUES (?, ?, ?, ?, ?)",
            (price, -shares, total_value, user_id, symbol)
        )
        db.execute("SELECT cash FROM users WHERE id = ?", (user_id,))
        user_cash = db.fetchone()["cash"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?", (user_cash + total_value, user_id))
        conn.commit()
        return redirect("/")

@app.route("/funds", methods=["GET", "POST"])
@login_required
def funds():
    user_id = session["user_id"]
    if request.method == "GET":
        db.execute("SELECT cash FROM users WHERE id = ?", (user_id,))
        cash = db.fetchone()["cash"]
        return render_template("funds.html", cash=usd(cash))
    if request.method == "POST":
        action = request.form.get("action")
        amount = request.form.get("amount")

        if not action or not amount:
            return apology("must select action and amount", 400)
        try:
            amount = int(amount)
        except ValueError:
            return apology("Amount must be a valid number", 400)

        if action == "withdraw":
            amount = -amount
            db.execute("SELECT cash FROM users WHERE id = ?", (user_id,))
            user_cash = db.fetchone()["cash"]
            if user_cash < -amount:
                return apology("Must not overdraw account", 400)

        db.execute(
            "INSERT INTO transactions (symbol, price, shares, amount_paid, user_id) VALUES (?, ?, ?, ?, ?)",
            ("N/A", 0, 0, amount, user_id)
        )
        db.execute("SELECT cash FROM users WHERE id = ?", (user_id,))
        user_cash = db.fetchone()["cash"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?", (user_cash + amount, user_id))
        conn.commit()

        db.execute("SELECT cash FROM users WHERE id = ?", (user_id,))
        cash = db.fetchone()["cash"]
        return render_template("funds.html", cash=usd(cash))