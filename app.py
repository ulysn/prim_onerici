from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "gizli_anahtar"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Kullanıcı Modeli
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

# Anket Sonucu Modeli
class SurveyResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="survey_results")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Bu kullanıcı adı zaten alınmış.")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        flash("Kayıt başarılı! Şimdi giriş yapabilirsin.")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            if user.username == "admin":
                return redirect(url_for("admin"))
            else:
                return redirect(url_for("survey"))
        else:
            flash("Hatalı kullanıcı adı veya şifre.")

    return render_template("login.html")


@app.route("/survey", methods=["GET", "POST"])
@login_required
def survey():
    if request.method == "POST":
        total = 0
        for i in range(1, 14):
            cevap = int(request.form.get(f"q{i}", 0))
            total += cevap

        # Veritabanına kaydet
        result = SurveyResult(user_id=current_user.id, score=total)
        db.session.add(result)
        db.session.commit()

        # Prim önerisi
        if total >= 50:
            prim = "Yüksek prim indirimi önerilir (%20-30)."
        elif total >= 35:
            prim = "Orta düzey prim indirimi önerilir (%10-15)."
        elif total >= 20:
            prim = "Düşük seviye prim indirimi önerilir (%5)."
        else:
            prim = "Prim indirimi önerilmez, gelişim planı tavsiye edilir."

        return render_template("result.html", score=total, suggestion=prim)

    return render_template("survey.html")

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():

    if current_user.username != "admin":
        flash("Bu sayfaya yalnızca admin erişebilir.")
        return redirect(url_for("survey"))

    if request.method == "POST":
        search_name = request.form.get("search")
        user = User.query.filter_by(username=search_name).first()
        if user:
            results = SurveyResult.query.filter_by(user_id=user.id).order_by(SurveyResult.date.desc()).all()
            return render_template("admin.html", user=user, results=results)
        else:
            flash("Kullanıcı bulunamadı.")
            return redirect(url_for("admin"))
    return render_template("admin.html")

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        current_password = request.form["current_password"]
        new_password = request.form["new_password"]

        if not check_password_hash(current_user.password, current_password):
            flash("Mevcut şifre yanlış.")
        else:
            hashed_new = generate_password_hash(new_password)
            current_user.password = hashed_new
            db.session.commit()
            flash("Şifre başarıyla değiştirildi!")

    results = SurveyResult.query.filter_by(user_id=current_user.id).order_by(SurveyResult.date.desc()).all()
    return render_template("profile.html", results=results)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Çıkış yapıldı.")
    return redirect(url_for("login"))
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


# İlk çalıştırma için veritabanı oluşturma
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
