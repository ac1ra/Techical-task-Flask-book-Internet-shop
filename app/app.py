from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "supersecretkey"

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    surname = db.Column(db.String(250), unique=True, nullable=False)

    email = db.Column(db.String(250), unique=True, nullable=False)
    phone = db.Column(db.String(250), unique=True, nullable=False)

    password = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        surname = request.form.get("surname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        if Users.query.filter_by(email=email).first():
            return render_template("signup.html", error="Email already taken!")
        hashed_password = generate_password_hash(
            password, method="pbkdf2:sha256")
        new_user = Users(username=username.capitalize(), surname=surname.capitalize(),
                         email=email, phone=phone, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = Users.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid username and password")
    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
