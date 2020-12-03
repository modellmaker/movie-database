from flask import Flask, render_template, request, make_response
from models import User, db

app = Flask(__name__)
db.create_all()


class Movies:
    def __init__(self, title, summary, imdb):
        self.title = title
        self.summary = summary
        self.imdb = imdb


egy = Movies("cim", "leiras", "IMDB")
ketto = Movies("cim2", "leiras2", "IMDB2")
harom = Movies("cim3", "leiras3", "IMDB3")
movies = [egy, ketto, harom]
my_dict = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    while True:
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            user = db.query(User).filter_by(username=username).first()

            if username == user.username and password == user.password:
                response = make_response(render_template("index.html", movies=movies, name=username))
                response.set_cookie("c_username", username)
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
    password = request.form.get("password")
    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    # writefile(username, password)
    # print(my_dict)
    message = "You have successfully registered on our page. You can now login."

    response = make_response(render_template("index.html", message=message))

    return response


@app.route("/signup-main", methods=["GET"])
def signup_main():
    response = make_response(render_template("signup.html"))

    return response


if __name__ == "__main__":
    app.run()
