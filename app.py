import logging
import sqlite3
import sys
from threading import Lock

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for


class BelowErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.ERROR


formatter = logging.Formatter(
    "%(levelname)s:%(name)s:%(asctime)s, %(message)s",
    datefmt="%m/%d/%Y, %H:%M:%S",
)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.addFilter(BelowErrorFilter())
stdout_handler.setFormatter(formatter)

stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.ERROR)
stderr_handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[stdout_handler, stderr_handler],
    force=True,
)

# Track successful database connections for the /metrics endpoint.
db_connection_count = 0
db_connection_lock = Lock()


def get_db_connection():
    """Create a database connection and update the connection metric."""
    global db_connection_count

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row

    with db_connection_lock:
        db_connection_count += 1

    return connection


def get_post(post_id):
    """Retrieve one post by ID."""
    connection = get_db_connection()
    try:
        return connection.execute(
            "SELECT * FROM posts WHERE id = ?", (post_id,)
        ).fetchone()
    finally:
        connection.close()


app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"
app.logger.setLevel(logging.DEBUG)


@app.route("/")
def index():
    connection = get_db_connection()
    try:
        posts = connection.execute("SELECT * FROM posts").fetchall()
    finally:
        connection.close()
    return render_template("index.html", posts=posts)


@app.route("/healthz")
def healthz():
    """Report whether the application can query the required posts table."""
    try:
        connection = get_db_connection()
        try:
            connection.execute("SELECT 1 FROM posts LIMIT 1").fetchone()
        finally:
            connection.close()
        return jsonify(result="OK - healthy"), 200
    except sqlite3.Error as error:
        app.logger.error(
            "Health check failed: database or posts table unavailable: %s", error
        )
        return jsonify(result="ERROR - unhealthy"), 500


@app.route("/metrics")
def metrics():
    """Return current post and database-connection counts."""
    connection = get_db_connection()
    try:
        post_count = connection.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    finally:
        connection.close()

    with db_connection_lock:
        connection_count = db_connection_count

    return jsonify(
        db_connection_count=connection_count,
        post_count=post_count,
    ), 200


@app.route("/<int:post_id>")
def post(post_id):
    post_record = get_post(post_id)
    if post_record is None:
        app.logger.error(
            "Non-existing article with ID %s accessed; 404 page returned!", post_id
        )
        return render_template("404.html"), 404

    app.logger.info('Article "%s" retrieved!', post_record["title"])
    return render_template("post.html", post=post_record)


@app.route("/about")
def about():
    app.logger.info('"About Us" page retrieved!')
    return render_template("about.html")


@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required!")
        else:
            connection = get_db_connection()
            try:
                connection.execute(
                    "INSERT INTO posts (title, content) VALUES (?, ?)",
                    (title, content),
                )
                connection.commit()
            finally:
                connection.close()

            app.logger.info('Article "%s" created!', title)
            return redirect(url_for("index"))

    return render_template("create.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3111)
