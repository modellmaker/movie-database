from flask import Flask, render_template, request, make_response, redirect
from models import User, MovieDB, db
import uuid
import hashlib

app = Flask(__name__)
# db.drop_all()
db.create_all()


class Movies:
    def __init__(self, title, summary, imdb, rating, length, season, verdict):
        self.title = title
        self.summary = summary
        self.imdb = imdb
        self.rating = rating
        self.length = length
        self.season = season
        self.verdict = verdict


'''
egy = Movies("cim", "leiras", "IMDB", "1.1", "1:23:45", "1", "verdict")
ketto = Movies("cim2", "leiras2", "IMDB2", "1.2", "2:00:00", "2", "verdict2")
harom = Movies("cim3", "leiras3", "IMDB3", "1.3", "3:00:00", "3", "verdict2")
movies = [egy, ketto, harom]

for movie in movies:
    movie = MovieDB(title=movie.title, summary=movie.summary, imdb=movie.imdb, rating=movie.rating, length=movie.length,
                    season=movie.season, verdict=movie.verdict)
    db.add(movie)
    db.commit()'''


@app.route("/")
def index():
    session_token = request.cookies.get("session_token")
    if session_token:
        movies = db.query(MovieDB).all()
        user = db.query(User).filter_by(session_token=session_token).first()
        return render_template("index.html", movies=movies, name=user.username)
    else:
        return render_template("index.html")


@app.route("/delete", methods=["POST"])
def delete():
    session_token = request.cookies.get("session_token")
    if session_token:
        movie_id = request.form.get("movie_id")
        db.query(MovieDB).filter(MovieDB.id == movie_id).delete()
    return redirect("/")


@app.route("/update", methods=["POST"])
def update():
    session_token = request.cookies.get("session_token")
    if session_token:
        movie = request.form.get("movie")


@app.route("/movies/<title>")
def movielink(title):
    movie = db.query(MovieDB).filter_by(title=title).first()
    session_token = request.cookies.get("session_token")
    if session_token:
        user = db.query(User).filter_by(session_token=session_token).first()
    return render_template("movie-detail.html", movie=movie, name=user.username)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = hashlib.sha256(request.form.get("password").encode()).hexdigest()

    try:
        user = db.query(User).filter_by(username=username).first()

        if username == user.username and password == user.password:
            session_token = str(uuid.uuid4())
            user.session_token = session_token
            db.add(user)
            db.commit()
            movies = db.query(MovieDB).all()
            response = make_response(render_template("index.html", movies=movies, name=username))
            response.set_cookie("session_token", session_token, httponly=True)
        else:
            message = "We can't find You. :( Please check, that You insert the correct username and password."
            response = render_template("index.html", message=message)

        return response

    except AttributeError:
        message = "We can't find You. :( Please check, that You insert the correct username and password."
        response = render_template("index.html", message=message)

        return response


@app.route("/logout", methods=["POST"])
def logout():
    response = make_response(render_template("index.html"))
    response.set_cookie("c_username", expires=0)
    return response


@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password = hashlib.sha256(request.form.get("password").encode()).hexdigest()
    user = User(username=username, password=password, session_token=None)
    db.add(user)
    db.commit()
    message = "You have successfully registered on our page. You can now login."

    response = make_response(render_template("index.html", message=message))

    return response


@app.route("/signup-main", methods=["GET"])
def signup_main():
    response = make_response(render_template("signup.html"))

    return response


if __name__ == "__main__":
    app.run()
